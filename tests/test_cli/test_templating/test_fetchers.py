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
        self.uri = "https://github.com/minos-framework/minos-templates/releases/download/0.1.0/foo.tar.gz"
        self.metadata = {
            "template_name": "foo",
            "template_registry": "https://github.com/minos-framework/minos-templates/releases/download/0.1.0",
            "template_version": "0.1.0",
        }
        self.fetcher = TemplateFetcher(self.uri, self.metadata)

    def test_uri(self):
        self.assertEqual(self.uri, self.fetcher.uri)

    def test_metadata(self):
        self.assertEqual(self.metadata, self.fetcher.metadata)

    def test_from_url(self):
        fetcher = TemplateFetcher.from_url(
            "https://github.com/minos-framework/minos-templates/releases/download/0.1.0/foo.tar.gz"
        )
        self.assertEqual(
            "https://github.com/minos-framework/minos-templates/releases/download/0.1.0/foo.tar.gz", fetcher.uri
        )
        self.assertEqual(
            {
                "template_name": "foo",
                "template_registry": "https://github.com/minos-framework/minos-templates/releases/download/0.1.0",
            },
            fetcher.metadata,
        )

    def test_from_path(self):
        fetcher = TemplateFetcher.from_path(Path("/path/to/registry/template.tar.gz"))
        self.assertEqual("file:///path/to/registry/template.tar.gz", fetcher.uri)
        self.assertEqual(
            {"template_name": "template", "template_registry": "file:///path/to/registry"}, fetcher.metadata,
        )

    def test_from_name(self):
        fetcher = TemplateFetcher.from_name("foo", "0.1.0")
        self.assertEqual(
            "https://github.com/minos-framework/minos-templates/releases/download/0.1.0/foo.tar.gz", fetcher.uri
        )
        self.assertEqual(
            {
                "template_name": "foo",
                "template_registry": "https://github.com/minos-framework/minos-templates/releases/download/0.1.0",
                "template_version": "0.1.0",
            },
            fetcher.metadata,
        )

    def test_tmp(self):
        mock = MagicMock()
        self.fetcher.fetch_tar = mock

        observed = self.fetcher.tmp

        self.assertIsInstance(observed, TemporaryDirectory)

        self.assertEqual([call(self.fetcher.uri, self.fetcher._tmp.name)], mock.call_args_list)

    def test_path(self):
        self.fetcher.fetch_tar = MagicMock()

        path = self.fetcher.path

        self.assertIsInstance(path, Path)
        self.assertEqual(self.fetcher.tmp.name, str(path))
        self.assertEqual(True, path.exists())

    def test_eq(self):
        self.assertEqual(TemplateFetcher("www.foo.com"), TemplateFetcher("www.foo.com"))
        self.assertNotEqual(TemplateFetcher("www.bar.com"), TemplateFetcher("www.foo.com"))

    def test_repr(self):
        self.assertEqual("TemplateFetcher('www.foo.com', {})", repr(TemplateFetcher("www.foo.com")))

    def test_fetch_tar(self):
        with patch("urllib.request.urlopen", return_value="file") as url_mock, patch("tarfile.open") as tar_mock:
            TemplateFetcher.fetch_tar("foo", "bar")

        self.assertEqual([call("foo")], url_mock.call_args_list)
        self.assertEqual([call(fileobj="file", mode="r|gz")], tar_mock.call_args_list)
        self.assertEqual([call(path="bar")], tar_mock.return_value.extractall.call_args_list)


if __name__ == "__main__":
    unittest.main()
