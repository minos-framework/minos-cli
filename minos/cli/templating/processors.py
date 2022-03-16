from __future__ import (
    annotations,
)

import logging
from collections.abc import (
    Callable,
)
from pathlib import (
    Path,
)
from typing import (
    Any,
    Optional,
    Union,
)

import copier
import yaml
from cached_property import (
    cached_property,
)
# noinspection PyProtectedMember
from copier.config.factory import (
    filter_config,
)
from copier.config.objects import (
    EnvOps,
)
from copier.config.user_data import (
    load_config_data,
)
# noinspection PyProtectedMember
from copier.tools import (
    get_jinja_env,
)
from jinja2 import (
    Environment,
)

from ..consoles import (
    console,
)
from ..importlib import (
    FunctionLoader,
)
from ..pathlib import (
    get_project_target_directory,
)
from ..wizards import (
    Form,
)
from .fetchers import (
    TemplateFetcher,
)

logger = logging.getLogger(__name__)


class TemplateProcessor:
    """Template Processor class.

    This class generates a scaffolding structure on a given directory.
    """

    def __init__(
        self,
        source: Union[Path, str],
        destination: Union[Path, str],
        context: Optional[dict[str, Any]] = None,
        defaults: Optional[dict[str, Any]] = None,
    ):
        if not isinstance(source, Path):
            source = Path(source)
        if not isinstance(destination, Path):
            destination = Path(destination)
        if context is None:
            context = dict()
        self.source = source
        self.destination = destination
        self.context = context
        self.defaults = defaults

    @classmethod
    def from_fetcher(
        cls,
        fetcher: TemplateFetcher,
        *args,
        context: Optional[dict[str, Any]] = None,
        defaults: Optional[dict[str, Any]] = None,
        **kwargs,
    ) -> TemplateProcessor:
        """Build a new instance from a fetcher.

        :param fetcher: The template fetcher instance.
        :param args: Additional positional arguments.
        :param context: A mapping containing already answered questions and environment variables for rendering.
        :param defaults: A mapping containing additional default values for questions.
        :param kwargs: Additional named arguments.
        :return: A new ``TemplateProcessor`` instance.
        """
        if context is None:
            context = dict()
        if defaults is None:
            defaults = dict()
        return cls(fetcher.path, context=fetcher.metadata | context, defaults=defaults, *args, **kwargs)

    @cached_property
    def linked_template_fetchers(self) -> list[TemplateFetcher]:
        """Get the list of linked template fetchers.

        :return: A list of ``TemplateFetcher`` instances.
        """
        return [
            TemplateFetcher(uri)
            for uri in self.form.get_template_uris(self._new_answers, context=self.answers, env=self.env)
        ]

    @property
    def linked_questions(self) -> list[str]:
        """Get the list of questions that are links.

        :return: A list of ``str`` values.
        """
        return self.form.links

    @cached_property
    def _new_answers(self) -> dict[str, Any]:
        return {k: v for k, v in self.answers.items() if k not in self._previous_answers}

    @cached_property
    def answers(self) -> dict[str, Any]:
        """Get the answers of the form.

        :return: A mapping from question name to the answer value.
        """
        answers = self.context
        answers |= self._previous_answers_without_template_registry

        answers = self.form.ask(context=answers, env=self.env)
        self._store_new_answers(answers)
        return answers

    @cached_property
    def _previous_answers(self) -> dict[str, str]:
        answers = dict()
        if self._answers_file_path.exists():
            with self._answers_file_path.open() as file:
                answers |= yaml.safe_load(file)

        if self._project_answers_file_path is not None and self._project_answers_file_path.exists():
            with self._project_answers_file_path.open() as file:
                answers |= yaml.safe_load(file)

        return answers

    @cached_property
    def _previous_answers_without_template_registry(self):
        previous_answers_without_registry = self._previous_answers.copy()
        previous_answers_without_registry.pop("template_registry", None)
        previous_answers_without_registry.pop("template_version", None)

        return previous_answers_without_registry

    def _store_new_answers(self, answers) -> None:
        with self._answers_file_path.open("w") as file:
            yaml.dump(answers, file)

    @property
    def _answers_file_path(self) -> Path:
        return self.destination / ".minos-answers.yml"

    @cached_property
    def _project_answers_file_path(self) -> Optional[Path]:
        try:
            return get_project_target_directory(self.destination) / ".minos-answers.yml"
        except ValueError:
            return None

    @cached_property
    def form(self) -> Form:
        """Get the form.

        :return: A ``Form`` instance.
        """
        questions = list()
        for name, question in filter_config(self._config_data)[1].items():
            if name in self.defaults:
                question["default"] = self.defaults[name]
            question["name"] = name
            questions.append(question)
        return Form.from_raw({"questions": questions})

    @cached_property
    def env(self) -> Environment:
        """Get the Jinja's environment.

        :return:
        """
        return get_jinja_env(EnvOps(**self._config_data.get("_envops", {})))

    @cached_property
    def _config_data(self):
        return load_config_data(self.source)

    def render(self, **kwargs) -> None:
        """Performs the template building.

        :param kwargs: Additional named arguments.
        :return: This method does not return anything.
        """
        if not self.source.exists():
            raise ValueError(f"The source {self.source!r} does not exits!")

        if not self.destination.exists():
            self.destination.mkdir(parents=True, exist_ok=True)

        if not self.destination.is_dir():
            raise ValueError(f"{self.destination!r} is not a directory!")

        context = self.answers | self.functions | {"destination": self.destination}
        self.render_copier(self.source, self.destination, context, **kwargs)

        for fetcher in self.linked_template_fetchers:
            TemplateProcessor.from_fetcher(fetcher, self.destination, context=self.answers).render()

    @cached_property
    def functions(self) -> dict[str, Callable]:
        """Get custom functions to be used by template rendering.

        :return: A mapping from function name to function itself.
        """
        names = self._config_data.get("_functions", list())
        return FunctionLoader.load_many_from_directory(names, self.source)

    @staticmethod
    def render_copier(
        source: Union[Path, str], destination: Union[Path, str], answers: dict[str, Any], **kwargs
    ) -> None:
        """Render a template using ``copier`` as the file orchestrator.

        :param source: The template path.
        :param destination: The destination path.
        :param answers: The answers to the template questions.
        :param kwargs: Additional named arguments.
        :return: This method does not return anything.
        """
        if not isinstance(source, str):
            source = str(source)
        if not isinstance(destination, str):
            destination = str(destination)
        with console.status(f"Rendering template into {destination!r}!...", spinner="moon"):
            logger.debug(f"Rendering a template located at {source!r} to {destination!r} with {answers!r} context...")
            copier.copy(
                src_path=source,
                dst_path=destination,
                data=answers,
                quiet=True,
                force=True,
                extra_paths=["/"],
                cleanup_on_error=False,
                **kwargs,
            )
        console.print(f":moon: Rendered template into {destination!r}!\n")
