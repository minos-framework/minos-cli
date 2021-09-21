from minos.cqrs import (
    CommandService,
)


class {{ cookiecutter.aggregate_name }}CommandService(CommandService):
    """{{ cookiecutter.aggregate_name }}CommandService class."""
