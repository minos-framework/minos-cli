from pathlib import Path
from cookiecutter.main import cookiecutter

TEMPLATE_PATH = Path(__file__).parent / "res" / "template"


def generate_microservice(output_dir: Path) -> None:
    """TODO

    :param output_dir: TODO
    :return: TODO
    """
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    cookiecutter(template=str(TEMPLATE_PATH), output_dir=output_dir)
