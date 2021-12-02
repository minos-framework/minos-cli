import unittest
from pathlib import (
    Path,
)
from tempfile import (
    TemporaryDirectory,
)
from unittest.mock import (
    PropertyMock,
    call,
    patch,
)

from jinja2 import (
    Environment,
)

from minos.cli import (
    MICROSERVICE_INIT,
    Form,
    TemplateProcessor,
)


class TestTemplateProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fetcher = MICROSERVICE_INIT

    def test_constructor(self):
        with TemporaryDirectory() as tmp_dir_name:
            source = Path(tmp_dir_name) / "source"
            target = Path(tmp_dir_name) / "target"

            processor = TemplateProcessor(str(source), str(target))

        self.assertEqual(source, processor.source)
        self.assertEqual(target, processor.target)

    def test_destination(self):
        with TemporaryDirectory() as tmp_dir_name:
            source = Path(tmp_dir_name) / "source"
            target = Path(tmp_dir_name) / "target"
            processor = TemplateProcessor(source, target)
            self.assertEqual(target.parent, processor.destination)

    def test_from_fetcher(self):
        with TemporaryDirectory() as tmp_dir_name:
            target = Path(tmp_dir_name)
            processor = TemplateProcessor.from_fetcher(self.fetcher, target)
            self.assertEqual(self.fetcher.path, processor.source)

    def test_env(self):
        with TemporaryDirectory() as tmp_dir_name:
            target = Path(tmp_dir_name)
            processor = TemplateProcessor.from_fetcher(self.fetcher, target)
            self.assertIsInstance(processor.env, Environment)

    def test_form(self):
        with TemporaryDirectory() as tmp_dir_name:
            target = Path(tmp_dir_name)
            processor = TemplateProcessor.from_fetcher(self.fetcher, target)
            self.assertIsInstance(processor.form, Form)
            self.assertGreater(len(processor.form.questions), 0)

    def test_answers(self):
        with TemporaryDirectory() as tmp_dir_name:
            target = Path(tmp_dir_name)
            processor = TemplateProcessor.from_fetcher(self.fetcher, target)
            with patch("minos.cli.Form.ask", return_value={"foo": "bar"}) as mock:
                self.assertEqual({"foo": "bar"}, processor.answers)
                self.assertEqual([call(env=processor.env)], mock.call_args_list)

    def test_render(self):
        with TemporaryDirectory() as tmp_dir_name:
            source = Path(tmp_dir_name) / "source"
            target = Path(tmp_dir_name) / "target"
            processor = TemplateProcessor(source, target)
            with patch("minos.cli.TemplateProcessor.render_copier") as render_mock, patch(
                "minos.cli.TemplateProcessor.answers", new_callable=PropertyMock, return_value={"foo": "bar"}
            ):
                processor.render()
            self.assertEqual([call(source, target.parent, {"foo": "bar"})], render_mock.call_args_list)

    def test_render_raises(self):
        with TemporaryDirectory() as tmp_dir_name:
            source = Path(tmp_dir_name) / "source"
            target = Path(tmp_dir_name) / "target"
            target.touch()
            processor = TemplateProcessor(source, target)
            with self.assertRaises(ValueError):
                processor.render()

    def test_render_copier(self):
        with TemporaryDirectory() as tmp_dir_name:
            source = Path(tmp_dir_name) / "source"
            destination = Path(tmp_dir_name) / "destination"
            with patch("copier.copy") as mock:
                TemplateProcessor.render_copier(source, destination, {"foo": "bar"})

            self.assertEqual(
                [call(src_path=str(source), dst_path=str(destination), data={"foo": "bar"}, quiet=True)],
                mock.call_args_list,
            )


if __name__ == "__main__":
    unittest.main()
