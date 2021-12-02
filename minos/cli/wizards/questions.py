from __future__ import (
    annotations,
)

from contextlib import (
    suppress,
)
from functools import (
    partial,
)
from typing import (
    Any,
    Callable,
    Optional,
)

from jinja2 import (
    Environment,
)
from rich.prompt import (
    Confirm,
    FloatPrompt,
    IntPrompt,
    Prompt,
)

from ..consoles import (
    console,
)


class Question:
    """TODO"""

    def __init__(
        self,
        name: str,
        type_: str,
        help_: Optional[str] = None,
        choices: Optional = None,
        default: Optional = None,
        secret: bool = False,
    ):
        self.name = name
        self.type_ = type_
        self.help_ = help_
        self.choices = choices
        self.default = default
        self.secret = secret

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> Question:
        """TODO"""
        return cls(
            name=raw.get("name"),
            type_=raw.get("type", None),
            help_=raw.get("help", None),
            choices=raw.get("choices", None),
            default=raw.get("default", None),
            secret=raw.get("secret", False),
        )

    def ask(self, context: dict[str, Any] = None, env: Optional[Environment] = None) -> str:
        """TODO"""
        if context is None:
            context = dict()

        title = self.title
        default = self.default

        if env is not None:
            with suppress(TypeError):
                title = env.from_string(title).render(**context)

            with suppress(TypeError):
                default = env.from_string(default).render(**context)

        answer = self._ask(f":question: {title}\n", default)
        console.print()
        return answer

    def _ask(self, title: str, default: Any) -> Any:
        answer = self._ask_fn(title, default=default)
        return answer

    @property
    def _ask_fn(self) -> Callable:
        if self.type_ == "int":
            fn = IntPrompt.ask
        elif self.type_ == "float":
            fn = FloatPrompt.ask
        elif self.type_ == "bool":
            fn = Confirm.ask
        else:
            fn = Prompt.ask
        return partial(fn, console=console, choices=self.choices, password=self.secret)

    @property
    def title(self) -> str:
        """TODO"""
        if self.help_ is not None:
            return self.help_
        return self.name

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, type(self))
            and self.name == other.name
            and self.type_ == other.type_
            and self.help_ == other.help_
            and self.choices == other.choices
            and self.default == other.default
        )
