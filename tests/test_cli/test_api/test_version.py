import unittest

from typer.testing import (
    CliRunner,
)

from minos.cli import (
    __main__,
    __version__,
    app,
    main,
)


class TestVersion(unittest.TestCase):
    def test_main(self):
        self.assertEqual(__main__.main, main)

    def test_version(self) -> None:
        result = CliRunner().invoke(app, ["version"])
        self.assertIn(__version__, result.output)


if __name__ == "__main__":
    unittest.main()
