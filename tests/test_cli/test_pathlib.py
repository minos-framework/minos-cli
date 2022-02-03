import unittest
from pathlib import (
    Path,
)
from tempfile import (
    TemporaryDirectory,
)

from minos.cli import (
    get_microservice_target_directory,
    get_project_target_directory,
)


class TestPathLib(unittest.TestCase):
    def test_get_project_target_directory(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)
            (path / ".minos-project.yaml").touch()
            self.assertEqual(path, get_project_target_directory(path))

    def test_get_project_target_directory_raises(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)
            with self.assertRaises(ValueError):
                get_project_target_directory(path)

    def test_get_microservice_target_directory_microservice(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)
            (path / ".minos-microservice.yaml").touch()

            self.assertEqual(path, get_microservice_target_directory(path, "foo"))

    def test_get_microservice_target_directory_project(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)
            (path / ".minos-project.yaml").touch()
            (path / "microservices" / "foo").mkdir(parents=True)
            (path / "microservices" / "foo" / ".minos-microservice.yaml").touch()

            self.assertEqual(path / "microservices" / "foo", get_microservice_target_directory(path, "foo"))

    def test_get_microservice_target_directory_raises(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)
            with self.assertRaises(ValueError):
                get_microservice_target_directory(path, "foo")

            (path / ".minos-project.yaml").touch()

            with self.assertRaises(ValueError):
                get_microservice_target_directory(path, "foo")


if __name__ == "__main__":
    unittest.main()
