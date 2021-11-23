from __future__ import (
    annotations,
)

from typing import (
    Any,
    Optional,
)

from .console import (
    console,
)


class Question:
    """TODO"""

    def __init__(self, name: str, type_: str, help_: Optional[str], choices: Optional, default: Optional):
        self.name = name
        self.type_ = type_
        self.help_ = help_
        self.choices = choices
        self.default = default

    @classmethod
    def from_raw(cls, name: str, raw: dict[str, Any]) -> Question:
        """TODO"""
        return cls(
            name,
            type_=raw.get("type", None),
            help_=raw.get("help", None),
            choices=raw.get("choices", None),
            default=raw.get("default", None),
        )

    def ask(self) -> str:
        """TODO"""
        answer = console.input(self.title)

        return answer

    @property
    def title(self) -> str:
        """TODO"""
        if self.help_ is not None:
            return self.help_
        return self.name
