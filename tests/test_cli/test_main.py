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

from minos.cli import __main__ as module_main
from minos.cli import (
    app,
    main,
)


class TestMain(unittest.TestCase):
    def test_init(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name) / "product"
            with patch("pathlib.Path.cwd", return_value=path):
                with patch("minos.cli.MicroserviceGenerator.build") as mock:
                    result = CliRunner().invoke(app, ["init"])

                    self.assertEqual(0, result.exit_code)

                    self.assertEqual(1, mock.call_count)

    def test_new(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name) / "product"
            with patch("minos.cli.MicroserviceGenerator.build") as mock:
                result = CliRunner().invoke(app, ["new", str(path)])

                self.assertEqual(0, result.exit_code)

                self.assertEqual(1, mock.call_count)

    def test_main(self):
        self.assertEqual(module_main.main, main)


if __name__ == "__main__":
    unittest.main()
