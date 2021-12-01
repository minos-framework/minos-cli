from pathlib import (
    Path,
)
from typing import (
    Any,
)

from cached_property import (
    cached_property,
)
from copier import (
    copy,
)
from copier.config.objects import (
    EnvOps,
)
from copier.config.user_data import (
    load_config_data,
)
from copier.tools import (
    get_jinja_env,
)
from jinja2.sandbox import (
    SandboxedEnvironment,
)

from ..consoles import (
    console,
)
from ..wizards import (
    Wizard,
)
from .fetchers import (
    TemplateFetcher,
)


class TemplateGenerator:
    """Template Generator class.

    This class generates a scaffolding structure on a given directory.
    """

    def __init__(self, target: Path, fetcher: TemplateFetcher):
        self.target = target
        self.fetcher = fetcher

    def build(self, **kwargs) -> None:
        """Performs the microservice building.

        :return: This method does not return anything.
        """
        if not self.target.exists():
            self.target.mkdir(parents=True, exist_ok=True)

        if not self.target.is_dir():
            raise ValueError(f"{self.target!r} is not a directory!")

        self._render()

    def _render(self) -> None:
        src_path = str(self._src_path)
        dst_path = str(self._dst_path)
        answers = self._answers
        with console.status("Rendering template...", spinner="moon"):
            copy(src_path=src_path, dst_path=dst_path, data=answers, quiet=True)
        console.print(":moon: Rendered template!\n")

    @cached_property
    def _answers(self) -> dict[str, Any]:
        return self._wizard.ask(env=self._env)

    @cached_property
    def _wizard(self) -> Wizard:
        questions = list()
        for name, question in self._config_data.items():
            if name.startswith("_"):
                continue

            if not isinstance(question, dict):
                question = {"default": question}

            if name == "name" and question.get("default", None) is None:
                question["default"] = self._name

            question["name"] = name

            questions.append(question)
        raw = dict()
        raw["questions"] = questions
        return Wizard.from_raw(raw)

    @cached_property
    def _env(self) -> SandboxedEnvironment:
        return get_jinja_env(EnvOps(**self._config_data.get("_envops", {})))

    @cached_property
    def _config_data(self):
        return load_config_data(self._src_path)

    @property
    def _src_path(self) -> Path:
        return self.fetcher.path

    @property
    def _name(self) -> str:
        return self.target.name

    @property
    def _dst_path(self) -> Path:
        return self.target.parent
