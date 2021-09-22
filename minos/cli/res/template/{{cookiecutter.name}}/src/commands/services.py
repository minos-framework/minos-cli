from minos.cqrs import (
    CommandService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)

from ..aggregates import (
    {{ cookiecutter.aggregate }},
)


class {{ cookiecutter.aggregate }}CommandService(CommandService):
    """{{ cookiecutter.aggregate }}CommandService class."""

    @enroute.rest.command("/{{ cookiecutter.aggregate.lower() }}s", "POST")
    @enroute.broker.command("Create{{ cookiecutter.aggregate }}")
    async def create_{{ cookiecutter.aggregate.lower() }}(self, request: Request) -> Response:
        """Create a new ``{{ cookiecutter.aggregate }}`` instance.

        :param request: The ``Request`` instance.
        :return: A ``Response`` instance.
        """
        try:
            content = await request.content()
            obj = {{ cookiecutter.aggregate }}(**content)
            return Response(obj)
        except Exception:
            raise ResponseException("An error occurred during order creation.")
