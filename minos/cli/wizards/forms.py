from __future__ import (
    annotations,
)

from typing import (
    Any,
    Optional,
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

    def ask(self, context: Optional[dict[str, Any]] = None, **kwargs) -> dict[str, Any]:
        """Perform the asking process.

        :param context: TODO
        :param kwargs: Additional named arguments to be passed to each question.
        :return: A mapping from the question names to the obtained answers.
        """
        answers = dict() if context is None else context.copy()

        for question in self.questions:
            if question.name not in answers:
                answers[question.name] = question.ask(answers, **kwargs)

        return answers

    @property
    def links(self) -> list[str]:
        """TODO"""
        return [question.name for question in self.questions if question.link]

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.questions == other.questions
