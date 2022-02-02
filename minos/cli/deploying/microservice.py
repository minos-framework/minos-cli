import subprocess
from pathlib import (
    Path,
)
from typing import (
    Optional,
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
        current = self.path
        while current != current.parent:
            if (current / ".minos-microservice.yaml").exists():
                return current

            if (current / ".minos-project.yaml").exists():
                target = current / "microservices" / self._name
                if (target / ".minos-microservice.yaml").exists():
                    return target
            current = current.parent

        raise ValueError(f"Unable to find the target directory from {self.path} origin.")

    def deploy(self) -> None:
        """Deploy target.

        :return: This method does not return anything.
        """
        subprocess.run("ansible-playbook playbooks/deploy.yaml", shell=True, cwd=str(self.target_directory))
