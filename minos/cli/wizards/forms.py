from __future__ import (
    annotations,
)

from typing import (
    Any,
)

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

    def ask(self, **kwargs) -> dict[str, Any]:
        """Perform the asking process.

        :param kwargs: Additional named arguments to be passed to each question.
        :return: A mapping from the question names to the obtained answers.
        """
        answers = dict()
        for question in self.questions:
            answers[question.name] = question.ask(answers, **kwargs)
        return answers

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.questions == other.questions
