from __future__ import (
    annotations,
)

from typing import (
    Any,
)

from .questions import (
    Question,
)


class Wizard:
    """TODO"""

    def __init__(self, questions: list[Question]):
        self.questions = questions

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> Wizard:
        """TODO"""
        questions = [Question.from_raw(v) for v in raw["questions"]]
        return cls(questions)

    def ask(self, **kwargs) -> dict[str, Any]:
        """TODO"""
        answers = dict()
        for question in self.questions:
            answers[question.name] = question.ask(answers, **kwargs)
        return answers
