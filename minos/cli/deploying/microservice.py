import subprocess
from pathlib import (
    Path,
)
from typing import (
    Optional,
)

from ..pathlib import (
    get_microservice_target_directory,
)
from .abc import (
    Deployer,
)


class MicroserviceDeployer(Deployer):
    """Microservice Deployer class."""

    def __init__(self, path: Path, name: Optional[str], **kwargs):
        super().__init__(path, **kwargs)
        self._name = name

    @property
    def target_directory(self) -> Path:
        """Get the target directory.

        :return: A ``Path`` instance.
        """
        return get_microservice_target_directory(self.path, self._name)

    def deploy(self) -> None:
        """Deploy target.

        :return: This method does not return anything.
        """
        subprocess.run("ansible-playbook playbooks/deploy.yaml", shell=True, cwd=str(self.target_directory))
