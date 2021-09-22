from pathlib import (
    Path,
)

from cookiecutter.main import (
    cookiecutter,
)

TEMPLATE_PATH = Path(__file__).parent / "res" / "template"


def generate_microservice(output_dir: Path) -> None:
    """TODO

    :param output_dir: TODO
    :return: TODOcd
    """
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    if not output_dir.is_dir():
        raise ValueError(f"{output_dir!r} is not a directory!")

    name = output_dir.name
    output_dir = output_dir.parent
    extra_context = {"name": name}

    cookiecutter(
        template=str(TEMPLATE_PATH),
        output_dir=output_dir,
        extra_context=extra_context,
        overwrite_if_exists=True,
        skip_if_file_exists=True,
    )
