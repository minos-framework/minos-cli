from pathlib import (
    Path,
)
from typing import (
    Any,
)

from copier import (
    copy,
)
from copier.config.user_data import (
    load_config_data,
)
from copier.vcs import (
    clone,
)

from .questions import (
    Question,
)


class MicroserviceGenerator:
    """Microservice Generator class.

    This class generates the microservice project structure on a given directory.
    """

    def __init__(
        self,
        target: Path,
        templates: str = "git@github.com:Clariteia/minos-templates.git",
        template_name: str = "microservice",
    ):
        self.target = target
        self.templates = templates
        self.template_name = template_name

    def build(self, **kwargs) -> None:
        """Performs the microservice building.

        :return: This method does not return anything.
        """
        if not self.target.exists():
            self.target.mkdir(parents=True, exist_ok=True)

        if not self.target.is_dir():
            raise ValueError(f"{self.target!r} is not a directory!")

        answers = self._ask_questions()

        self._run_copier(answers)

    def _ask_questions(self) -> dict[str, Any]:
        questions = self._get_questions()
        answers = {question.name: question.ask() for question in questions}
        return answers

    def _get_questions(self) -> list[Question]:
        data = load_config_data(self._src_path)
        questions = list()
        for k, v in data.items():
            if k.startswith("_"):
                continue
            # Transform simplified questions format into complex
            if not isinstance(v, dict):
                v = {"default": v}
            questions.append(Question.from_raw(k, v))
        return questions

    @property
    def _name(self) -> str:
        return self.target.name

    def _run_copier(self, answers: dict[str, Any]) -> None:
        copy(
            src_path=str(self._src_path), dst_path=str(self._dst_path), data=answers,
        )

    @property
    def _src_path(self) -> Path:
        return self.clone_repository() / self.template_name

    def clone_repository(self) -> Path:
        """TODO"""
        location = clone(self.templates)
        return Path(location)

    @property
    def _dst_path(self) -> Path:
        return self.target.parent
