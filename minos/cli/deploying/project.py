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
        current = self.path
        while current != current.parent:
            if (current / ".minos-project.yaml").exists():
                return current
            current = current.parent

        raise ValueError(f"Unable to find the target directory from {self.path} origin.")

    def deploy(self) -> None:
        """Deploy target.

        :return: This method does not return anything.
        """
        subprocess.run("ansible-playbook playbooks/deploy.yaml", shell=True, cwd=str(self.target_directory))
