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
    """Question class."""

    def __init__(
        self,
        name: str,
        type_: str,
        help_: Optional[str] = None,
        choices: Optional = None,
        default: Optional = None,
        secret: bool = False,
        link: bool = False,
    ):
        self.name = name
        self.type_ = type_
        self.help_ = help_
        self.choices = choices
        self.default = default
        self.secret = secret
        self.link = link

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> Question:
        """Build a new instance from raw.

        :param raw: A dictionary containing the question attributes.
        :return: A new ``Question`` instance.
        """
        return cls(
            name=raw.get("name"),
            type_=raw.get("type", None),
            help_=raw.get("help", None),
            choices=raw.get("choices", None),
            default=raw.get("default", None),
            secret=raw.get("secret", False),
            link=raw.get("link", False),
        )

    def ask(self, context: dict[str, Any] = None, env: Optional[Environment] = None) -> str:
        """Perform the ask.

        :param context: An optional context dictionary containing the variables to be used for question rendering.
        :param env: An optional Jinja's environment to be used for question rendering.
        :return: The obtained answer.
        """
        if context is None:
            context = dict()

        title = self.title
        default = self.default_title
        choices = self.choices

        if env is not None:
            with suppress(TypeError):
                title = env.from_string(title).render(**context)

            with suppress(TypeError):
                default = env.from_string(default).render(**context)

            if choices is not None:
                if isinstance(choices, dict):
                    new = dict()
                    for k, v in choices.items():
                        with suppress(TypeError):
                            k = env.from_string(k).render(**context)
                        with suppress(TypeError):
                            v = env.from_string(v).render(**context)
                        new[k] = v
                    choices = new

                else:
                    new = list()
                    for choice in choices:
                        with suppress(TypeError):
                            choice = env.from_string(choice).render(**context)
                        new.append(choice)
                    choices = new

        answer = self._ask(f":question: {title}\n", default, choices)
        if isinstance(answer, str):
            answer = answer.strip()
        console.print()
        return answer

    def _ask(self, title: str, default: Any, choices) -> Any:
        answer = self._ask_fn(title, default=default, choices=choices)
        if choices is not None and isinstance(choices, dict):
            answer = choices[answer]
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
        return partial(fn, console=console, password=self.secret)

    @property
    def title(self) -> str:
        """Get the title text to be shown during the asking process.

        :return: A ``str`` value.
        """
        if self.help_ is not None:
            return self.help_
        return self.name

    @property
    def default_title(self) -> Any:
        """TODO"""
        if self.default is None:
            return None

        if self.choices is not None and isinstance(self.choices, dict):
            for key, value in self.choices.items():
                if value == self.default:
                    return key
            raise Exception("TODO")

        return self.default

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, type(self))
            and self.name == other.name
            and self.type_ == other.type_
            and self.help_ == other.help_
            and self.choices == other.choices
            and self.default == other.default
        )
