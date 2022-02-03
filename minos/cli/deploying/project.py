import subprocess
from pathlib import (
    Path,
)

from ..pathlib import (
    get_project_target_directory,
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
        return get_project_target_directory(self.path)

    def deploy(self) -> None:
        """Deploy target.

        :return: This method does not return anything.
        """
        subprocess.run("ansible-playbook playbooks/deploy.yaml", shell=True, cwd=str(self.target_directory))
