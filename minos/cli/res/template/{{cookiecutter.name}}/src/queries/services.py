from minos.common import (
    AggregateDiff,
)
from minos.cqrs import (
    QueryService,
)
from minos.networks import (
    Request,
    Response,
    ResponseException,
    enroute,
)


class {{ cookiecutter.aggregate }}QueryService(QueryService):
    """{{ cookiecutter.aggregate }}QueryService class."""

    @enroute.rest.query("/{{ cookiecutter.aggregate.lower() }}s", "GET")
    async def get_{{ cookiecutter.aggregate.lower() }}(self, request: Request) -> Response:
        """Get a {{ cookiecutter.aggregate }} instance.

        :param request: A request instance..
        :return: A response exception.
        """
        raise ResponseException("Not implemented yet!")

    @enroute.broker.event("{{ cookiecutter.aggregate }}Created")
    async def {{ cookiecutter.aggregate.lower() }}_created(self, request: Request) -> None:
        """Handle the {{ cookiecutter.aggregate }} creation events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        print(diff)

    @enroute.broker.event("{{ cookiecutter.aggregate }}Updated")
    async def {{ cookiecutter.aggregate.lower() }}_updated(self, request: Request) -> None:
        """Handle the {{ cookiecutter.aggregate }} update events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        print(diff)

    @enroute.broker.event("{{ cookiecutter.aggregate }}Deleted")
    async def {{ cookiecutter.aggregate.lower() }}_deleted(self, request: Request) -> None:
        """Handle the {{ cookiecutter.aggregate }} deletion events.

        :param request: A request instance containing the aggregate difference.
        :return: This method does not return anything.
        """
        diff: AggregateDiff = await request.content()
        print(diff)
