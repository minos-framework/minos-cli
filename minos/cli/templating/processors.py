from __future__ import (
    annotations,
)

import logging
from pathlib import (
    Path,
)
from typing import (
    Any,
    Optional,
    Union,
)

import copier
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
        self, source: Union[Path, str], destination: Union[Path, str], context: Optional[dict[str, Any]] = None
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

    @classmethod
    def from_fetcher(
        cls, fetcher: TemplateFetcher, *args, context: Optional[dict[str, Any]] = None, **kwargs
    ) -> TemplateProcessor:
        """Build a new instance from a fetcher.

        :param fetcher: The template fetcher instance.
        :param args: Additional positional arguments.
        :param context: A mapping containing already answered questions and environment variables for rendering.
        :param kwargs: Additional named arguments.
        :return: A new ``TemplateProcessor`` instance.
        """
        if context is None:
            context = dict()
        return cls(fetcher.path, context=fetcher.metadata | context, *args, **kwargs)

    @cached_property
    def linked_template_fetchers(self) -> list[TemplateFetcher]:
        """Get the list of linked template fetchers.

        :return: A list of ``TemplateFetcher`` instances.
        """
        urls = map(lambda name: self.answers[name], self.linked_questions)
        urls = filter(lambda url: url != "", urls)
        fetchers = map(TemplateFetcher, urls)
        return list(fetchers)

    @property
    def linked_questions(self) -> list[str]:
        """Get the list of questions that are links.

        :return: A list of ``str`` values.
        """
        return self.form.links

    @cached_property
    def answers(self) -> dict[str, Any]:
        """Get the answers of the form.

        :return: A mapping from question name to the answer value.
        """
        return self.form.ask(context=self.context, env=self.env)

    @cached_property
    def form(self) -> Form:
        """Get the form.

        :return: A ``Form`` instance.
        """
        questions = list()
        for name, question in filter_config(self._config_data)[1].items():
            question["name"] = name
            if question["name"] == "name" and question.get("default", None) is None:
                question["default"] = self.destination.name
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

        context = self.answers | {"destination": self.destination}
        self.render_copier(self.source, self.destination, context, **kwargs)

        for fetcher in self.linked_template_fetchers:
            TemplateProcessor.from_fetcher(fetcher, self.destination, context=self.answers).render()

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
