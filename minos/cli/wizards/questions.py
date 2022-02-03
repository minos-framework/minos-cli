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
    Union,
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
        choices: Optional[Union[list[Any], dict[str, Any]]] = None,
        default: Optional[Any] = None,
        secret: bool = False,
        link: dict[Any, str] = None,
    ):
        if link is None:
            link = dict()

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
            link=raw.get("link", None),
        )

    def get_template_uri(self, answer: Any, *args, **kwargs) -> Optional[str]:
        """Get template uri for the given answer.

        :param answer: The answer value.
        :return: The template uri. It can be ``None`` if the given response does not have any associated template.
        """
        template = self.link.get(answer)
        return self._render_value(template, *args, **kwargs)

    def ask(self, *args, **kwargs) -> str:
        """Perform the ask.

        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: The obtained answer.
        """
        title = self.render_title(*args, **kwargs)
        default = self.render_default(*args, **kwargs)
        choices = self.render_choices(*args, **kwargs)

        answer = self._ask(f":question: {title}\n", default, choices)

        console.print()
        return answer

    def render_title(self, *args, **kwargs) -> str:
        """Render the title value.

        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A ``str`` value.
        """
        return self._render_value(self.title, *args, **kwargs)

    def render_default(self, *args, **kwargs) -> Any:
        """Render the default value.

        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A ``str`` value.
        """
        if self.default is None:
            return None

        if self.choices is None or not isinstance(self.choices, dict):
            return self._render_value(self.default, *args, **kwargs)

        for key, value in self.choices.items():
            if value == self.default:
                return str(self._render_value(key, *args, **kwargs))

        raise ValueError("The default attribute must match with one of the choices.")

    def render_choices(self, *args, **kwargs) -> Optional[Union[list[Any], dict[Any]]]:
        """Render the choices value.

        :param args: Additional positional arguments.
        :param kwargs: Additional named arguments.
        :return: A ``str`` value.
        """
        if not self.choices:
            return self.choices

        if isinstance(self.choices, dict):
            rendered = self._render_dict(self.choices, *args, **kwargs)
            rendered = {str(k): v for k, v in rendered.items()}
        else:
            rendered = self._render_list(self.choices, *args, **kwargs)
            rendered = [str(v) for v in rendered]

        return rendered

    def _render_dict(self, data: dict[str, Any], *args, **kwargs) -> dict[str, Any]:
        return {self._render_value(k, *args, **kwargs): self._render_value(v, *args, **kwargs) for k, v in data.items()}

    def _render_list(self, data: list[str], *args, **kwargs) -> list[Any]:
        return [self._render_value(value, *args, **kwargs) for value in data]

    # noinspection PyUnusedLocal

    @staticmethod
    def _render_value(
        value: Any, env: Optional[Environment] = None, context: Optional[dict[str, Any]] = None, **kwargs
    ) -> Any:
        if env and context:
            with suppress(TypeError):
                value = env.from_string(value).render(**context)
        return value

    def _ask(self, title: str, default: Any, choices: Union[list[Any], dict[str, Any]]) -> Any:
        answer = self._ask_fn(title, default=default, choices=choices)
        if choices is not None and isinstance(choices, dict):
            answer = choices[answer]
        if isinstance(answer, str):
            answer = answer.strip()
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

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, type(self))
            and self.name == other.name
            and self.type_ == other.type_
            and self.help_ == other.help_
            and self.choices == other.choices
            and self.default == other.default
        )
