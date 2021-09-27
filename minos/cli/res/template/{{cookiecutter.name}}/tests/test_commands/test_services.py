import sys
import unittest

from src import (
    {{ cookiecutter.aggregate }},
    {{ cookiecutter.aggregate }}CommandService,
)

from minos.networks import (
    Response,
)
from tests.utils import (
    _FakeRequest,
    build_dependency_injector,
)


class Test{{cookiecutter.aggregate}}CommandService(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.injector = build_dependency_injector()

    async def asyncSetUp(self) -> None:
        await self.injector.wire(modules=[sys.modules[__name__]])

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    def test_constructor(self):
        service = {{ cookiecutter.aggregate }}CommandService()
        self.assertIsInstance(service, {{cookiecutter.aggregate}}CommandService)

    async def test_create_{{ cookiecutter.aggregate.lower() }}(self):
        service = {{ cookiecutter.aggregate }}CommandService()

        request = _FakeRequest({})
        response = await service.create_{{ cookiecutter.aggregate.lower() }}(request)

        self.assertIsInstance(response, Response)

        observed = await response.content()
        expected = {{ cookiecutter.aggregate }}(
            created_at=observed.created_at,
            updated_at=observed.updated_at,
            uuid=observed.uuid,
            version=observed.version,
        )

        self.assertEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
