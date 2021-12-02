import unittest

from rich.console import (
    Console,
)

from minos.cli import (
    console,
    error_console,
)


class TestConsoles(unittest.TestCase):
    def test_console(self):
        self.assertIsInstance(console, Console)

    def test_error_console(self):
        self.assertIsInstance(error_console, Console)


if __name__ == "__main__":
    unittest.main()
