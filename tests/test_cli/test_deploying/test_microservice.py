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
    MicroserviceDeployer,
)


class TestMicroserviceDeployer(unittest.TestCase):
    def test_target_directory_microservice(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)
            (path / ".minos-microservice.yaml").touch()
            deployer = MicroserviceDeployer(path, "foo")
            self.assertEqual(path, deployer.target_directory)

    def test_target_directory_project(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)
            (path / ".minos-project.yaml").touch()
            (path / "microservices" / "foo").mkdir(parents=True)
            (path / "microservices" / "foo" / ".minos-microservice.yaml").touch()

            deployer = MicroserviceDeployer(path, "foo")
            self.assertEqual(path / "microservices" / "foo", deployer.target_directory)

    def test_target_directory_raises(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)
            deployer = MicroserviceDeployer(path, "foo")
            with self.assertRaises(ValueError):
                deployer.target_directory

            (path / ".minos-project.yaml").touch()
            deployer = MicroserviceDeployer(path, "foo")
            with self.assertRaises(ValueError):
                deployer.target_directory

    def test_build(self):
        with TemporaryDirectory() as tmp_dir_name:
            path = Path(tmp_dir_name)
            (path / ".minos-microservice.yaml").touch()
            deployer = MicroserviceDeployer(path, "foo")

            with patch.object(subprocess, "run") as mock:
                deployer.deploy()

            self.assertEqual(
                [call("ansible-playbook playbooks/deploy.yaml", shell=True, cwd=str(path))], mock.call_args_list
            )


if __name__ == "__main__":
    unittest.main()
