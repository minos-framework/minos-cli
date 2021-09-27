from pathlib import (
    Path,
)

from cookiecutter import main as ccm

from .constants import (
    MICROSERVICE_TEMPLATE_PATH,
)


class MicroserviceGenerator:
    """Microservice Generator class.

    This class generates the microservice project structure on a given directory.
    """

    def __init__(self, target: Path):
        self.target = target

    def build(self, **kwargs) -> None:
        """Performs the microservice building.

        :return: This method does not return anything.
        """
        if not self.target.exists():
            self.target.mkdir(parents=True, exist_ok=True)

        if not self.target.is_dir():
            raise ValueError(f"{self.target!r} is not a directory!")

        name = self.target.name
        output_dir = self.target.parent
        extra_context = {"name": name}

        ccm.cookiecutter(
            template=str(MICROSERVICE_TEMPLATE_PATH),
            output_dir=str(output_dir),
            extra_context=extra_context,
            overwrite_if_exists=True,
            skip_if_file_exists=True,
            **kwargs,
        )
