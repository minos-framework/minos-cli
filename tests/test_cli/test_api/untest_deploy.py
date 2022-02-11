import unittest
from unittest.mock import (
    patch,
)

from typer.testing import (
    CliRunner,
)

from minos.cli import (
    app,
)
from minos.cli.deploying import (
    MicroserviceDeployer,
    ProjectDeployer,
)


class TestDeployAPI(unittest.TestCase):
    def test_microservice(self) -> None:
        with patch.object(MicroserviceDeployer, "deploy") as mock:
            result = CliRunner().invoke(app, ["deploy", "microservice"])

            self.assertEqual(0, result.exit_code)

            self.assertEqual(1, mock.call_count)

    def test_project(self) -> None:
        with patch.object(ProjectDeployer, "deploy") as mock:
            result = CliRunner().invoke(app, ["deploy", "project"])

            self.assertEqual(0, result.exit_code)

            self.assertEqual(1, mock.call_count)


if __name__ == "__main__":
    unittest.main()
