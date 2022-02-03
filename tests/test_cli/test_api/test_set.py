import unittest
from pathlib import (
    Path,
)
from tempfile import (
    TemporaryDirectory,
)
from unittest.mock import (
    patch,
)

import yaml
from typer.testing import (
    CliRunner,
)

from minos.cli import (
    __main__,
    app,
    main,
)
from minos.cli.api.set import (
    set_service,
)


class TestSet(unittest.TestCase):
    def test_main(self):
        self.assertEqual(__main__.main, main)

    def test_set_service(self):
        service = "database"
        backend = "postgres"

        with TemporaryDirectory() as tmp_dir_name:
            tmp_config_file: Path = Path(tmp_dir_name) / ".minos-project.yaml"
            with open(tmp_config_file, "w") as config:
                data = {"services": None}
                yaml.dump(data, config)

            with patch("pathlib.Path.cwd", return_value=Path(tmp_dir_name)):
                with patch("minos.cli.TemplateProcessor.render"):
                    set_service(service, backend)

                    with open(tmp_config_file, "r") as result_config_file:
                        data = yaml.safe_load(result_config_file)

        self.assertEqual(backend, data["services"][service])

    def minos_set(self, service: str, backend: str):
        with TemporaryDirectory() as tmp_dir_name:
            tmp_config_file: Path = Path(tmp_dir_name) / ".minos-project.yaml"
            with open(tmp_config_file, "w") as config:
                data = {"services": None}
                yaml.dump(data, config)

            with patch("pathlib.Path.cwd", return_value=Path(tmp_dir_name)):
                with patch("minos.cli.TemplateProcessor.render") as mock:
                    result = CliRunner().invoke(app, ["set", service, backend])

                    self.assertEqual(0, result.exit_code)

                    self.assertEqual(1, mock.call_count)

    def test_set_database_postgres(self) -> None:
        self.minos_set("database", "postgres")

    def test_set_broker_kafka(self) -> None:
        self.minos_set("broker", "kafka")

    def test_set_api_gateway_minos(self) -> None:
        self.minos_set("api-gateway", "minos")

    def test_set_discovery_minos(self) -> None:
        self.minos_set("discovery", "minos")

    def test_no_config_file(self):
        with TemporaryDirectory() as tmp_dir_name:
            with patch("pathlib.Path.cwd", return_value=Path(tmp_dir_name)):
                with patch("minos.cli.TemplateProcessor.render"):
                    result = CliRunner().invoke(app, ["set", "database", "postgres"])

                    self.assertEqual(1, result.exit_code)

    def test_service_already_set(self):
        with TemporaryDirectory() as tmp_dir_name:
            tmp_config_file: Path = Path(tmp_dir_name) / ".minos-project.yaml"
            with open(tmp_config_file, "w") as config:
                data = {"services": {"database": "postgres"}}
                yaml.dump(data, config)

            with patch("pathlib.Path.cwd", return_value=Path(tmp_dir_name)):
                with patch("minos.cli.TemplateProcessor.render"):
                    result = CliRunner().invoke(app, ["set", "database", "postgres"])

                    self.assertEqual(1, result.exit_code)


if __name__ == "__main__":
    unittest.main()
