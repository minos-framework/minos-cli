from abc import (
    ABC,
    abstractmethod,
)
from pathlib import (
    Path,
)


class Deployer(ABC):
    """Deployer class."""

    def __init__(self, path: Path):
        self._path = path

    @abstractmethod
    def deploy(self) -> None:
        """Deploy target.

        :return: This method does not return anything.
        """
