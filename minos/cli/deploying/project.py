import subprocess
from pathlib import (
    Path,
)

from .abc import (
    Deployer,
)


class ProjectDeployer(Deployer):
    """TODO"""

    @property
    def target_directory(self) -> Path:
        """TODO"""

        current = self._path
        while current != current.parent:
            if (current / "minos-project.lock").exists():
                return current
            current = current.parent

        raise ValueError("TODO")

    def deploy(self) -> None:
        """TODO"""
        subprocess.run("ansible-playbook playbooks/deploy.yaml", shell=True, cwd=str(self.target_directory))
