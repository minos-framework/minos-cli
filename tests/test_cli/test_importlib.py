import builtins
import unittest
from pathlib import (
    Path,
)
from tempfile import (
    TemporaryDirectory,
)
from unittest.mock import (
    MagicMock,
    call,
    patch,
)

from minos.cli import (
    FunctionLoader,
)


class TestFunctionLoader(unittest.TestCase):
    def test_load_many_from_directory(self):
        with TemporaryDirectory() as tmp_dir_name:
            directory_path = Path(tmp_dir_name)
            with patch("minos.cli.importlib.FunctionLoader.load_one_from_directory", side_effect={int, float}) as mock:
                observed = FunctionLoader.load_many_from_directory(["builtins.int", "builtins.float"], directory_path)

                self.assertEqual({"int": int, "float": float}, observed)
                self.assertEqual(
                    [call("builtins.int", directory_path), call("builtins.float", directory_path)], mock.call_args_list,
                )

    def test_load_one_from_directory(self):
        with TemporaryDirectory() as tmp_dir_name:
            directory_path = Path(tmp_dir_name)
            with patch("minos.cli.importlib.FunctionLoader.load_module_from_file", return_value=builtins) as mock:
                observed = FunctionLoader.load_one_from_directory("builtins.int", directory_path)

                self.assertEqual(int, observed)
                self.assertEqual([call(directory_path / "builtins.py")], mock.call_args_list)

    def test_load_module_from_file(self):
        with TemporaryDirectory() as tmp_dir_name:
            directory_path = Path(tmp_dir_name)
            with patch("importlib.util.spec_from_file_location") as mock:
                observed = FunctionLoader.load_module_from_file(directory_path / "builtins.py")

                self.assertIsInstance(observed, MagicMock)
                self.assertEqual([call("builtins", str(directory_path / "builtins.py"))], mock.call_args_list)


if __name__ == "__main__":
    unittest.main()
