import subprocess
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
    MICROSERVICE_TEMPLATE_PATH,
    TemplateGenerator,
)

runner = CliRunner()


class TestGenerate(unittest.TestCase):
    def test_build(self) -> None:
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name) / "product"
            generator = TemplateGenerator(path)
            with patch("cookiecutter.main.cookiecutter") as mock:
                generator.build()
                self.assertEqual(1, mock.call_count)
                call_args = call(
                    template=str(MICROSERVICE_TEMPLATE_PATH),
                    output_dir=str(path.parent),
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
                TemplateGenerator(path).build()

    def test_template(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name) / "product"
            TemplateGenerator(path).build(no_input=True)

            result = subprocess.Popen(["make", "install", "reformat", "lint", "coverage"], cwd=path)
            result.wait()
            self.assertEqual(0, result.returncode)


if __name__ == "__main__":
    unittest.main()
