from abc import (
    ABC,
    abstractmethod,
)
from pathlib import (
    Path,
)


class Deployer(ABC):
    """Deployer class."""

    def __init__(self, path: Path, *args, **kwargs):
        self._path = path

    @property
    def path(self) -> Path:
        """Get the path.

        :return: A ``Path`` instance.
        """
        return self._path

    @abstractmethod
    def deploy(self) -> None:
        """Deploy target.

        :return: This method does not return anything.
        """
