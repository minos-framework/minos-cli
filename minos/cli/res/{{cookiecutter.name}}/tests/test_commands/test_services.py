import sys
import unittest

from src import (
    {{ cookiecutter.aggregate }}CommandService,
)
from tests.utils import (
    build_dependency_injector,
)


class Test{{cookiecutter.aggregate}}CommandService(unittest.IsolatedAsyncioTestCase):
    """Test {{cookiecutter.aggregate}}"""

    def setUp(self) -> None:
        self.injector = build_dependency_injector()

    async def asyncSetUp(self) -> None:
        await self.injector.wire(modules=[sys.modules[__name__]])

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    def test_constructor(self):
        obj = {{ cookiecutter.aggregate }}CommandService()
        self.assertIsInstance(obj, {{cookiecutter.aggregate}}CommandService)

if __name__ == '__main__':
    unittest.main()
