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


class TestInit(unittest.TestCase):
    def test_main(self):
        self.assertEqual(__main__.main, main)

    def test_init_project(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name) / "ecommerce"
            with patch("pathlib.Path.cwd", return_value=path):
                with patch("minos.cli.TemplateProcessor.render") as mock:
                    result = CliRunner().invoke(app, ["init", "project"])

                    self.assertEqual(0, result.exit_code)

                    self.assertEqual(1, mock.call_count)

    def test_init_microservice(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name) / "product"
            with patch("pathlib.Path.cwd", return_value=path):
                with patch("minos.cli.TemplateProcessor.render") as mock:
                    result = CliRunner().invoke(app, ["init", "microservice"])

                    self.assertEqual(0, result.exit_code)

                    self.assertEqual(1, mock.call_count)


if __name__ == "__main__":
    unittest.main()
