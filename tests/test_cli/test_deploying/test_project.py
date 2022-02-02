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

from minos.cli.deploying import (
    ProjectDeployer,
)


class TestProjectDeployer(unittest.TestCase):
    def test_target_directory(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)
            (path / ".minos-project.yaml").touch()
            deployer = ProjectDeployer(path)
            self.assertEqual(path, deployer.target_directory)

    def test_target_directory_raises(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)
            deployer = ProjectDeployer(path)
            with self.assertRaises(ValueError):
                deployer.target_directory

    def test_build(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)
            (path / ".minos-project.yaml").touch()
            deployer = ProjectDeployer(path)

            with patch.object(subprocess, "run") as mock:
                deployer.deploy()

            self.assertEqual(
                [call("ansible-playbook playbooks/deploy.yaml", shell=True, cwd=str(path))], mock.call_args_list
            )


if __name__ == "__main__":
    unittest.main()
