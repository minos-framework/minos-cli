import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from typer.testing import CliRunner

from minos.cli import (
    __main__,
    app,
    main,
)


class TestUtils(unittest.TestCase):
    def test_main(self):
        self.assertEqual(__main__.main, main)

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


if __name__ == "__main__":
    unittest.main()
