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

from jinja2.sandbox import (
    SandboxedEnvironment,
)
from rich.prompt import (
    Confirm,
    FloatPrompt,
    IntPrompt,
    Prompt,
)

from ..consoles import (
    console,
    error_console,
)


class Question:
    """TODO"""

    def __init__(
        self, name: str, type_: str, help_: Optional[str], choices: Optional, default: Optional,
    ):
        self.name = name
        self.type_ = type_
        self.help_ = help_
        self.choices = choices
        self.default = default

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> Question:
        """TODO"""
        return cls(
            name=raw.get("name"),
            type_=raw.get("type", None),
            help_=raw.get("help", None),
            choices=raw.get("choices", None),
            default=raw.get("default", None),
        )

    def ask(self, context: dict[str, Any] = None, env: Optional[SandboxedEnvironment] = None) -> str:
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

        return self._ask(title, default)

    def _ask(self, title, default):
        answer = self._ask_fn(title, default=default)
        while not self.valid(answer):
            error_console.print(f"{answer!r} is invalid!")
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
        return partial(fn, console=console)

    @property
    def title(self) -> str:
        """TODO"""
        if self.help_ is not None:
            return self.help_
        return self.name

    def valid(self, value: Any) -> bool:
        """TODO"""
        return True
