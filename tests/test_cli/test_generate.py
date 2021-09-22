import unittest
from pathlib import (
    Path,
)
from tempfile import (
    TemporaryDirectory,
)
from unittest.mock import (
    call,
    patch,
)

from typer.testing import (
    CliRunner,
)

from minos.cli import (
    TEMPLATE_PATH,
    MicroserviceGenerator,
)

runner = CliRunner()


class TestGenerate(unittest.TestCase):
    def test_build(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name) / "product"
            generator = MicroserviceGenerator(path)
            with patch("cookiecutter.main.cookiecutter") as mock:
                generator.build()
                self.assertEqual(1, mock.call_count)
                call_args = call(
                    template=TEMPLATE_PATH,
                    output_dir=path.parent,
                    extra_context={"name": "product"},
                    overwrite_if_exists=True,
                    skip_if_file_exists=True,
                )
                self.assertEqual(call_args, mock.call_args)

    def test_build_raises(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name) / "product"
            path.touch()
            with self.assertRaises(ValueError):
                MicroserviceGenerator(path).build()


if __name__ == "__main__":
    unittest.main()
