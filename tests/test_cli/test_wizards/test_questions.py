import pathlib
import unittest
from unittest.mock import (
    call,
    patch,
)

from jinja2 import (
    BaseLoader,
    Environment,
)

from minos.cli import (
    Question,
    console,
)


class TestQuestion(unittest.TestCase):
    def tearDown(self) -> None:
        answers_file_path = pathlib.Path.cwd() / ".minos-answers.yml"
        if answers_file_path.exists():
            answers_file_path.unlink()

    def test_constructor(self) -> None:
        question = Question("foo", "str")

        self.assertIsInstance(question, Question)
        self.assertEqual("foo", question.name)
        self.assertEqual("str", question.type_)
        self.assertEqual(None, question.help_)
        self.assertEqual(None, question.choices)
        self.assertEqual(None, question.default)
        self.assertEqual(False, question.secret)
        self.assertEqual(dict(), question.link)

    def test_constructor_extended(self) -> None:
        question = Question("foo", "str", "bar", ["one", "two", "three"], "one", True, {"one": "/path/to/template"})

        self.assertIsInstance(question, Question)
        self.assertEqual("foo", question.name)
        self.assertEqual("str", question.type_)
        self.assertEqual("bar", question.help_)
        self.assertEqual(["one", "two", "three"], question.choices)
        self.assertEqual("one", question.default)
        self.assertEqual(True, question.secret)
        self.assertEqual({"one": "/path/to/template"}, question.link)

    def test_from_raw(self):
        expected = Question("foo", "str", "bar", ["one", "two", "three"], "one", True, {"one": "/path/to/template"})
        observed = Question.from_raw(
            {
                "name": "foo",
                "type": "str",
                "help": "bar",
                "choices": ["one", "two", "three"],
                "default": "one",
                "secret": True,
                "link": {"one": "/path/to/template"},
            }
        )
        self.assertEqual(expected, observed)

    def test_ask_int(self):
        question = Question("foo", "int")
        with patch("rich.prompt.IntPrompt.ask", return_value=1) as mock:
            self.assertEqual(1, question.ask())
        self.assertEqual(
            [call(":question: foo\n", console=console, choices=None, password=False, default=None)], mock.call_args_list
        )

    def test_ask_float(self):
        question = Question("foo", "float")
        with patch("rich.prompt.FloatPrompt.ask", return_value=1.5) as mock:
            self.assertEqual(1.5, question.ask())
        self.assertEqual(
            [call(":question: foo\n", console=console, choices=None, password=False, default=None)], mock.call_args_list
        )

    def test_ask_bool(self):
        question = Question("foo", "bool")
        with patch("rich.prompt.Confirm.ask", return_value=True) as mock:
            self.assertEqual(True, question.ask())
        self.assertEqual(
            [call(":question: foo\n", console=console, choices=None, password=False, default=None)], mock.call_args_list
        )

    def test_ask_str(self):
        question = Question("foo", "str")
        with patch("rich.prompt.Prompt.ask", return_value="one") as mock:
            self.assertEqual("one", question.ask())
        self.assertEqual(
            [call(":question: foo\n", console=console, choices=None, password=False, default=None)], mock.call_args_list
        )

    def test_ask_with_env(self):
        context = {"bar": "two"}

        env = Environment(loader=BaseLoader)

        question = Question("foo", "str", help_="What is {{bar}}?", default="{{bar}}")
        with patch("rich.prompt.Prompt.ask", return_value="one") as mock:
            self.assertEqual("one", question.ask(env, context))
        self.assertEqual(
            [call(":question: What is two?\n", console=console, choices=None, password=False, default="two")],
            mock.call_args_list,
        )

    def test_ask_with_choices_dict(self):
        question = Question("foo", "str", choices={"one": "two", "three": "four"}, default="two")
        with patch("rich.prompt.Prompt.ask", return_value="three"):
            self.assertEqual("four", question.ask())

    def test_render_title(self):
        context = {"bar": "two"}
        env = Environment(loader=BaseLoader)
        expected = "What is two?"
        question = Question("foo", "str", help_="What is {{bar}}?")
        observed = question.render_title(env, context)
        self.assertEqual(expected, observed)

    def test_render_choices_list(self):
        context = {"bar": "two"}
        env = Environment(loader=BaseLoader)
        expected = ["one", "two"]
        question = Question("foo", "str", choices=["one", "{{bar}}"])
        observed = question.render_choices(env, context)
        self.assertEqual(expected, observed)

    def test_render_choices_dict(self):
        context = {"bar": "two"}
        env = Environment(loader=BaseLoader)
        expected = {"one": "two", "two": "three"}
        question = Question("foo", "str", choices={"one": "{{ bar }}", "{{ bar }}": "three"})
        observed = question.render_choices(env, context)
        self.assertEqual(expected, observed)

    def test_render_default(self):
        context = {"bar": "two"}
        env = Environment(loader=BaseLoader)
        expected = "two"
        question = Question("foo", "str", default="{{bar}}")
        observed = question.render_default(env, context)
        self.assertEqual(expected, observed)

    def test_render_default_with_choices_dict(self):
        question = Question("foo", "str", default="two", choices={"one": "two", "three": "four"})
        self.assertEqual("one", question.render_default())

    def test_render_default_with_choices_dict_raises(self):
        question = Question("foo", "str", default="three", choices={"one": "two", "three": "four"})
        with self.assertRaises(ValueError):
            question.render_default()

    def test_title_with_name(self):
        question = Question("foo", "str")
        self.assertEqual("foo", question.title)

    def test_title_with_help(self):
        question = Question("foo", "str", "bar")
        self.assertEqual("bar", question.title)


if __name__ == "__main__":
    unittest.main()
