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

import yaml
from jinja2 import (
    Environment,
)

from minos.cli import (
    Form,
    TemplateFetcher,
    TemplateProcessor,
)
from minos.cli.templating.fetchers import (
    TEMPLATE_URL,
    TEMPLATE_VERSION,
)


class TestTemplateProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fetcher = TemplateFetcher.from_name("microservice-init")

    def test_constructor(self):
        with TemporaryDirectory() as tmp_dir_name:
            source = Path(tmp_dir_name) / "source"
            destination = Path(tmp_dir_name) / "destination"

            processor = TemplateProcessor(str(source), str(destination))

        self.assertEqual(source, processor.source)
        self.assertEqual(destination, processor.destination)

    def test_from_fetcher(self):
        with TemporaryDirectory() as tmp_dir_name:
            destination = Path(tmp_dir_name)
            processor = TemplateProcessor.from_fetcher(self.fetcher, destination)
            self.assertEqual(self.fetcher.path, processor.source)

    def test_env(self):
        with TemporaryDirectory() as tmp_dir_name:
            destination = Path(tmp_dir_name)
            processor = TemplateProcessor.from_fetcher(self.fetcher, destination)
            self.assertIsInstance(processor.env, Environment)

    def test_form(self):
        with TemporaryDirectory() as tmp_dir_name:
            destination = Path(tmp_dir_name)
            processor = TemplateProcessor.from_fetcher(self.fetcher, destination)
            self.assertIsInstance(processor.form, Form)
            self.assertGreater(len(processor.form.questions), 0)

    def test_form_with_defaults(self):
        with TemporaryDirectory() as tmp_dir_name:
            destination = Path(tmp_dir_name)
            processor = TemplateProcessor.from_fetcher(self.fetcher, destination, defaults={"name": "foo"})
            form = processor.form
            question = next((q for q in form.questions if q.name == "name"), None)
            self.assertIsNotNone(question)
            self.assertEqual("foo", question.default)

    def test_answers(self):
        with TemporaryDirectory() as tmp_dir_name:
            destination = Path(tmp_dir_name)
            processor = TemplateProcessor.from_fetcher(self.fetcher, destination)
            with patch("minos.cli.Form.ask", return_value={"foo": "bar"}) as mock:
                self.assertEqual({"foo": "bar"}, processor.answers)
                self.assertEqual(
                    [
                        call(
                            context={
                                "template_registry": f"{TEMPLATE_URL}/{TEMPLATE_VERSION}",
                                "template_version": TEMPLATE_VERSION,
                                "template_name": "microservice-init",
                            },
                            env=processor.env,
                        )
                    ],
                    mock.call_args_list,
                )

    def test_answers_with_previous_answers(self):
        expected_answers = {"foo": "foo_answer", "bar": "bar_answer"}
        with TemporaryDirectory() as tmp_dir_name:
            project_destination = Path(tmp_dir_name)
            (project_destination / ".minos-project.yaml").touch()

            with (project_destination / ".minos-answers.yml").open("w") as file:
                yaml.dump({"foo": "foo_answer"}, file)

            microservice_destination = project_destination / "microservices" / "foo"
            microservice_destination.mkdir(parents=True)

            processor = TemplateProcessor.from_fetcher(self.fetcher, microservice_destination)

            with (microservice_destination / ".minos-answers.yml").open("w") as file:
                yaml.dump({"bar": "bar_answer"}, file)

            with patch("minos.cli.Form.ask", return_value=expected_answers) as mock:
                self.assertEqual(expected_answers, processor.answers)

            self.assertEqual(
                [call(context=processor.context | expected_answers, env=processor.env)], mock.call_args_list,
            )

            with (microservice_destination / ".minos-answers.yml").open() as file:
                answers = yaml.safe_load(file)
                self.assertEqual(expected_answers, answers)

    def test_answers_without_previous_answers(self):
        with TemporaryDirectory() as tmp_dir_name:
            destination = Path(tmp_dir_name)
            processor = TemplateProcessor.from_fetcher(self.fetcher, destination)

            with patch("minos.cli.Form.ask", return_value={"foo": "bar"}) as mock:
                self.assertEqual({"foo": "bar"}, processor.answers)

            self.assertEqual([call(context=processor.context, env=processor.env)], mock.call_args_list)

            with (destination / ".minos-answers.yml").open() as file:
                answers = yaml.safe_load(file)
                self.assertEqual({"foo": "bar"}, answers)

    def test_linked_questions(self):
        with TemporaryDirectory() as tmp_dir_name:
            destination = Path(tmp_dir_name)
            processor = TemplateProcessor.from_fetcher(self.fetcher, destination)
            with patch("minos.cli.Form.links", new_callable=PropertyMock, return_value=["foo", "bar"]):
                self.assertEqual(["foo", "bar"], processor.linked_questions)

    def test_linked_template_fetchers(self):
        with TemporaryDirectory() as tmp_dir_name:
            destination = Path(tmp_dir_name)
            processor = TemplateProcessor.from_fetcher(self.fetcher, destination)

            expected = [TemplateFetcher("/microservice-python-init.tar.gz")]
            with patch(
                "minos.cli.TemplateProcessor.linked_questions", new_callable=PropertyMock, return_value=["foo", "bar"]
            ), patch(
                "minos.cli.TemplateProcessor.answers",
                new_callable=PropertyMock,
                return_value={"language": "python", "name": "foo"},
            ):
                self.assertEqual(expected, processor.linked_template_fetchers)

    def test_render(self):
        with TemporaryDirectory() as tmp_dir_name:
            source = Path(tmp_dir_name) / "source"
            source.mkdir()
            destination = Path(tmp_dir_name) / "destination"
            processor = TemplateProcessor(source, destination)
            with patch("minos.cli.TemplateProcessor.render_copier") as render_mock, patch(
                "minos.cli.TemplateProcessor.answers", new_callable=PropertyMock, return_value={"foo": "bar"}
            ):
                processor.render()
            self.assertEqual(
                [call(source, destination, {"foo": "bar", "destination": destination})], render_mock.call_args_list
            )

    def test_functions(self):
        with TemporaryDirectory() as tmp_dir_name:
            source = Path(tmp_dir_name) / "source"
            source.mkdir()
            destination = Path(tmp_dir_name) / "destination"
            processor = TemplateProcessor(source, destination)
            with patch(
                "minos.cli.TemplateProcessor._config_data",
                new_callable=PropertyMock,
                return_value={"_functions": ["builtins.int"]},
            ), patch(
                "minos.cli.importlib.FunctionLoader.load_many_from_directory", return_value={"int": int}
            ) as load_functions_mock:
                observed = processor.functions

            self.assertEqual({"int": int}, observed)
            self.assertEqual([call(["builtins.int"], source)], load_functions_mock.call_args_list)

    def test_render_linked_templates(self):
        with TemporaryDirectory() as tmp_dir_name:
            destination = Path(tmp_dir_name) / "destination"
            processor = TemplateProcessor.from_fetcher(self.fetcher, destination)
            context = {"language": "python", "name": "foo"}
            with patch("minos.cli.TemplateProcessor.render_copier"), patch(
                "minos.cli.TemplateProcessor.linked_questions", new_callable=PropertyMock, return_value=["foo", "bar"]
            ), patch("minos.cli.TemplateProcessor.answers", new_callable=PropertyMock, return_value=context), patch(
                "minos.cli.TemplateProcessor.from_fetcher"
            ) as from_fetcher_mock:
                processor.render()
            expected = [
                call(TemplateFetcher("/microservice-python-init.tar.gz"), destination, context=context),
            ]
            self.assertEqual(expected, from_fetcher_mock.call_args_list)

    def test_render_raises_source(self):
        with TemporaryDirectory() as tmp_dir_name:
            source = Path(tmp_dir_name) / "source"
            destination = Path(tmp_dir_name) / "destination"
            processor = TemplateProcessor(source, destination)
            with self.assertRaises(ValueError):
                processor.render()

    def test_render_raises_destination(self):
        with TemporaryDirectory() as tmp_dir_name:
            source = Path(tmp_dir_name) / "source"
            source.mkdir()
            destination = Path(tmp_dir_name) / "destination"
            destination.touch()
            processor = TemplateProcessor(source, destination)
            with self.assertRaises(ValueError):
                processor.render()

    def test_render_copier(self):
        with TemporaryDirectory() as tmp_dir_name:
            source = Path(tmp_dir_name) / "source"
            destination = Path(tmp_dir_name) / "destination"
            with patch("copier.copy") as mock:
                TemplateProcessor.render_copier(source, destination, {"foo": "bar"})

            self.assertEqual(
                [
                    call(
                        src_path=str(source),
                        dst_path=str(destination),
                        data={"foo": "bar"},
                        quiet=True,
                        force=True,
                        extra_paths=["/"],
                        cleanup_on_error=False,
                    )
                ],
                mock.call_args_list,
            )


if __name__ == "__main__":
    unittest.main()
