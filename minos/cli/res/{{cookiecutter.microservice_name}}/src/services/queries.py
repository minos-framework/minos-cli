from minos.cqrs import (
    QueryService,
)


class {{ cookiecutter.aggregate_name }}QueryService(QueryService):
    """{{ cookiecutter.aggregate_name }}QueryService class."""
