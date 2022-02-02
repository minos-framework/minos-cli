import unittest
from pathlib import (
    Path,
)
from tempfile import (
    TemporaryDirectory,
)

from minos.cli.deploying.abc import (
    Deployer,
)


class _Deployer(Deployer):
    """For testing purposes."""

    def deploy(self) -> None:
        """For Testing purposes."""


class TestDeployer(unittest.TestCase):
    def test_abstract(self):
        # noinspection PyUnresolvedReferences
        self.assertEqual({"deploy"}, set(Deployer.__abstractmethods__))

    def test_path(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)

            deployer = _Deployer(path)
            self.assertEqual(path, deployer.path)


if __name__ == "__main__":
    unittest.main()
