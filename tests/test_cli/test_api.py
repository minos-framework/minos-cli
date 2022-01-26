import unittest
from pathlib import (
    Path,
)
from tempfile import (
    TemporaryDirectory,
)
from unittest.mock import (
    patch,
)

from typer.testing import (
    CliRunner,
)

from minos.cli import (
    __main__,
    app,
    main,
)


class TestAPI(unittest.TestCase):
    def test_main(self):
        self.assertEqual(__main__.main, main)

    def test_microservice_init(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name) / "product"
            with patch("pathlib.Path.cwd", return_value=path):
                with patch("minos.cli.TemplateProcessor.render") as mock:
                    result = CliRunner().invoke(app, ["microservice", "init"])

                    self.assertEqual(0, result.exit_code)

                    self.assertEqual(1, mock.call_count)

    def test_microservice_new(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name) / "product"
            with patch("minos.cli.TemplateProcessor.render") as mock:
                result = CliRunner().invoke(app, ["microservice", "new", str(path)])

                self.assertEqual(0, result.exit_code)

                self.assertEqual(1, mock.call_count)

    def test_project_init(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name) / "ecommerce"
            with patch("pathlib.Path.cwd", return_value=path):
                with patch("minos.cli.TemplateProcessor.render") as mock:
                    result = CliRunner().invoke(app, ["project", "init"])

                    self.assertEqual(0, result.exit_code)

                    self.assertEqual(1, mock.call_count)

    def test_project_new(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name) / "ecommerce"
            with patch("minos.cli.TemplateProcessor.render") as mock:
                result = CliRunner().invoke(app, ["project", "new", str(path)])

                self.assertEqual(0, result.exit_code)

                self.assertEqual(1, mock.call_count)

    def test_utils_render_template_path(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            template_path = Path(tmp_dir_name) / "template"
            destination = Path(tmp_dir_name) / "destination"
            with patch("minos.cli.TemplateProcessor.render") as render_mock, patch(
                "minos.cli.TemplateFetcher.from_path"
            ) as fetcher_mock:
                result = CliRunner().invoke(
                    app, ["utils", "render-template", "--path", str(template_path), str(destination)]
                )

            self.assertEqual(0, result.exit_code)
            self.assertEqual(1, fetcher_mock.call_count)
            self.assertEqual(1, render_mock.call_count)

    def test_utils_render_template_url(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            template_path = "www.foo.com/template"
            destination = Path(tmp_dir_name) / "destination"
            with patch("minos.cli.TemplateProcessor.render") as render_mock, patch(
                "minos.cli.TemplateFetcher.from_url"
            ) as fetcher_mock:
                result = CliRunner().invoke(
                    app, ["utils", "render-template", "--url", str(template_path), str(destination)]
                )

            self.assertEqual(0, result.exit_code)
            self.assertEqual(1, fetcher_mock.call_count)
            self.assertEqual(1, render_mock.call_count)

    def test_utils_render_template_raises(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            destination = Path(tmp_dir_name) / "destination"
            result = CliRunner().invoke(app, ["utils", "render-template", str(destination)])

            self.assertEqual(2, result.exit_code)

    def test_set_database_postgres(self) -> None:
        with patch("minos.cli.TemplateProcessor.render") as mock:
            result = CliRunner().invoke(app, ["set", "database", "postgres"])

            self.assertEqual(0, result.exit_code)

            self.assertEqual(1, mock.call_count)

    def test_set_broker_kafka(self) -> None:
        with patch("minos.cli.TemplateProcessor.render") as mock:
            result = CliRunner().invoke(app, ["set", "broker", "kafka"])

            self.assertEqual(0, result.exit_code)

            self.assertEqual(1, mock.call_count)

    def test_set_apigateway_minos(self) -> None:
        with patch("minos.cli.TemplateProcessor.render") as mock:
            result = CliRunner().invoke(app, ["set", "api-gateway", "minos"])

            self.assertEqual(0, result.exit_code)

            self.assertEqual(1, mock.call_count)

    def stest_set_discovery_minos(self) -> None:
        with patch("minos.cli.TemplateProcessor.render") as mock:
            result = CliRunner().invoke(app, ["set", "discovery", "minos"])

            self.assertEqual(0, result.exit_code)

            self.assertEqual(1, mock.call_count)


if __name__ == "__main__":
    unittest.main()
