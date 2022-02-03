from pathlib import (
    Path,
)


def get_project_target_directory(path: Path) -> Path:
    """Get the target directory for a project.

    :return: A ``Path`` instance.
    """
    current = path
    while current != current.parent:
        if (current / ".minos-project.yaml").exists():
            return current
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
        if (current / ".minos-microservice.yaml").exists():
            return current

        if (current / ".minos-project.yaml").exists():
            target = current / "microservices" / name
            if (target / ".minos-microservice.yaml").exists():
                return target
        current = current.parent

    raise ValueError(f"Unable to find the target directory for {name} from {path} origin.")
