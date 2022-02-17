from pathlib import (
    Path,
)

MINOS_PROJECT_FILENAME = ".minos-project.yaml"
MINOS_MICROSERVICE_FILENAME = ".minos-microservice.yaml"
MICROSERVICES_DIRECTORY = "microservices"


def get_project_target_directory(path: Path) -> Path:
    """Get the target directory for a project.

    :return: A ``Path`` instance.
    """
    current = path
    while current != current.parent:
        if (current / MINOS_PROJECT_FILENAME).exists():
            return current
        else:
            current = current.parent

    raise ValueError(f"Unable to find the target directory from {path} origin.")


def get_microservice_target_directory(path: Path, name: str) -> Path:
    """Get the target directory for a microservice.

    :param path: The starting path.
    :param name: The name of the microservice.
    :return: A ``Path`` instance.
    """
    current = path
    while current != current.parent:
        if (current / MINOS_MICROSERVICE_FILENAME).exists():
            return current

        if (current / MINOS_PROJECT_FILENAME).exists():
            target = current / MICROSERVICES_DIRECTORY / name
            if (target / MINOS_MICROSERVICE_FILENAME).exists():
                return target
        current = current.parent

    raise ValueError(f"Unable to find the target directory for {name} from {path} origin.")


def get_microservices_directory(path: Path) -> Path:
    project_directory = get_project_target_directory(path)
    return project_directory / MICROSERVICES_DIRECTORY
