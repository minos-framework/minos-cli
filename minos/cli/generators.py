from pathlib import (
    Path,
)

from cookiecutter import main as ccm

TEMPLATE_PATH = Path(__file__).parent / "res" / "template"


class MicroserviceGenerator:
    """TODO"""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def build(self) -> None:
        """TODO

        :return: TODO
        """
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True, exist_ok=True)

        if not self.output_dir.is_dir():
            raise ValueError(f"{self.output_dir!r} is not a directory!")

        name = self.output_dir.name
        output_dir = self.output_dir.parent
        extra_context = {"name": name}

        ccm.cookiecutter(
            template=TEMPLATE_PATH,
            output_dir=output_dir,
            extra_context=extra_context,
            overwrite_if_exists=True,
            skip_if_file_exists=True,
        )
