import subprocess
from pathlib import (
    Path,
)

from .abc import (
    Deployer,
)


class ProjectDeployer(Deployer):
    """Project Deployer class."""

    @property
    def target_directory(self) -> Path:
        """Get the target directory.

        :return: A ``Path`` instance.
        """
        current = self._path
        while current != current.parent:
            if (current / ".minos-project.yaml").exists():
                return current
            current = current.parent

        raise ValueError("TODO")

    def deploy(self) -> None:
        """Deploy target.

        :return: This method does not return anything.
        """
        subprocess.run("ansible-playbook playbooks/deploy.yaml", shell=True, cwd=str(self.target_directory))
