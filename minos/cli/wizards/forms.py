from __future__ import (
    annotations,
)

import pathlib
from typing import (
    Any,
    Optional,
)

import yaml

from .questions import (
    Question,
)


class Form:
    """Form class."""

    def __init__(self, questions: list[Question]):
        self.questions = questions

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> Form:
        """Build a new instance from raw.

        :param raw: A dictionary containing the form attributes.
        :return: A new ``Form`` instance.
        """
        questions = [Question.from_raw(v) for v in raw["questions"]]
        return cls(questions)

    def ask(self, context: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        """Perform the asking process.

        :param context: A mapping containing already answered questions and environment variables for rendering.
        :param kwargs: Additional named arguments to be passed to each question.
        :return: A mapping from the question names to the obtained answers.
        """
        answers = dict() if context is None else context.copy()
        previous_answers = self._read_previous_answers()
        answers.update(previous_answers)

        for question in self.questions:
            if question.name not in answers:
                answers[question.name] = question.ask(context=answers, **kwargs)

        return answers

    def _read_previous_answers(self) -> dict[str, str]:
        answers_file_path = pathlib.Path.cwd() / ".minos-answers.yml"

        previous_answers = dict()
        if answers_file_path.exists():
            with answers_file_path.open("r") as answers_file:
                previous_answers = yaml.safe_load(answers_file)

        return previous_answers

    @property
    def links(self) -> list[str]:
        """Get the list of question names that are links to another templates.

        :return: A list of ``str`` values.
        """
        return [question.name for question in self.questions if question.link]

    def get_template_uris(self, answers: dict[str, Any], *args, **kwargs) -> list[str]:
        """Get template uris.

        :param answers: A mapping from question name to answer value.
        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A list of strings representing template uris.
        """
        uris = (
            question.get_template_uri(answers[question.name], context=answers, *args, **kwargs)
            for question in self.questions
        )
        uris = filter(lambda uri: uri is not None, uris)
        return list(uris)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.questions == other.questions
