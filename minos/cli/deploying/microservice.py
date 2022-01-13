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
    """TODO"""

    def __init__(self, name: Optional[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name

    @property
    def target_directory(self) -> Path:
        """TODO"""

        current = self._path
        while current != current.parent:
            if (current / "minos-microservice.lock").exists():
                return current

            if (current / "minos-project.lock").exists():
                target = current / "microservices" / self._name
                if (target / "minos-microservice.lock").exists():
                    return target
                break
            current = current.parent

        raise ValueError("TODO")

    def deploy(self) -> None:
        """TODO"""
        subprocess.run("ansible-playbook playbooks/deploy.yaml", shell=True, cwd=str(self.target_directory))
