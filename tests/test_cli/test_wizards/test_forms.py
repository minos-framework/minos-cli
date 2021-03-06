import unittest
from unittest.mock import (
    call,
    patch,
)

from minos.cli import (
    Form,
    Question,
)


class TestForm(unittest.TestCase):
    def setUp(self) -> None:
        self.questions = [
            Question("foo", "int"),
            Question("bar", "str", link={"one": "/path/to/template"}),
        ]
        self.form = Form(self.questions)

    def test_constructor(self):
        self.assertIsInstance(self.form, Form)
        self.assertEqual(self.questions, self.form.questions)

    def test_from_raw(self):
        raw = {"questions": [{"name": "foo", "type": "int"}, {"name": "bar", "type": "str", "link": True}]}
        observed = Form.from_raw(raw)
        self.assertEqual(self.form, observed)

    def test_links(self):
        self.assertEqual(["bar"], self.form.links)

    def test_get_template_uris(self):
        self.assertEqual(["/path/to/template"], self.form.get_template_uris(answers={"bar": "one"}))

    def test_ask(self):
        with patch("minos.cli.Question.ask", side_effect=["one", "two"]) as mock:
            observed = self.form.ask()

        self.assertEqual({"foo": "one", "bar": "two"}, observed)
        self.assertEqual([call(context=observed), call(context=observed)], mock.call_args_list)


if __name__ == "__main__":
    unittest.main()
