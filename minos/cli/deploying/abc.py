from abc import (
    ABC,
    abstractmethod,
)
from pathlib import (
    Path,
)


class Deployer(ABC):
    """TODO"""

    def __init__(self, path: Path):
        self._path = path

    @abstractmethod
    def deploy(self) -> None:
        """TODO"""
