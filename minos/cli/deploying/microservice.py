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

    def __init__(self, name: Optional[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name

    @property
    def target_directory(self) -> Path:
        """Get the target directory.

        :return: A ``Path`` instance.
        """
        current = self._path
        while current != current.parent:
            if (current / ".minos-microservice.yaml").exists():
                return current

            if (current / ".minos-project.yaml").exists():
                target = current / "microservices" / self._name
                if (target / ".minos-microservice.yaml").exists():
                    return target
                break
            current = current.parent

        raise ValueError("Cannot be found the target directory.")

    def deploy(self) -> None:
        """Deploy target.

        :return: This method does not return anything.
        """
        subprocess.run("ansible-playbook playbooks/deploy.yaml", shell=True, cwd=str(self.target_directory))
