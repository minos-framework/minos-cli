import unittest
from pathlib import (
    Path,
)
from tempfile import (
    TemporaryDirectory,
)
from unittest.mock import (
    MagicMock,
    call,
    patch,
)

from minos.cli import (
    TemplateFetcher,
)


class TestTemplateFetcher(unittest.TestCase):
    def setUp(self) -> None:
        self.fetcher = TemplateFetcher.from_name("foo", "0.1.0")

    def test_url(self):
        self.assertEqual(
            "https://github.com/Clariteia/minos-templates/releases/download/0.1.0/foo.tar.gz", self.fetcher.url
        )

    def test_tmp(self):
        mock = MagicMock()
        self.fetcher.fetch_tar = mock

        observed = self.fetcher.tmp

        self.assertIsInstance(observed, TemporaryDirectory)

        self.assertEqual([call(self.fetcher.url, self.fetcher._tmp.name)], mock.call_args_list)

    def test_path(self):
        self.fetcher.fetch_tar = MagicMock()

        path = self.fetcher.path

        self.assertIsInstance(path, Path)
        self.assertEqual(self.fetcher.tmp.name, str(path))
        self.assertEqual(True, path.exists())

    def test_fetch_tar(self):
        with patch("urllib.request.urlopen", return_value="file") as url_mock, patch("tarfile.open") as tar_mock:
            TemplateFetcher.fetch_tar("foo", "bar")

        self.assertEqual([call("foo")], url_mock.call_args_list)
        self.assertEqual([call(fileobj="file", mode="r|gz")], tar_mock.call_args_list)
        self.assertEqual([call(path="bar")], tar_mock.return_value.extractall.call_args_list)


if __name__ == "__main__":
    unittest.main()
