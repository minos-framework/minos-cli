from __future__ import (
    annotations,
)

import tarfile
import urllib.request
from pathlib import (
    Path,
)
from tempfile import (
    TemporaryDirectory,
)
from typing import (
    Any,
    Final,
)

from ..consoles import (
    console,
)

TEMPLATE_URL: Final[str] = "https://github.com/Clariteia/minos-templates/releases/download"
TEMPLATE_VERSION: Final[str] = "0.0.1.dev4"

TEMPLATE_ROOT_URL = "/".join([TEMPLATE_URL, TEMPLATE_VERSION])


class TemplateFetcher:
    """Template Fetcher class."""

    def __init__(self, url: str):
        self.url = url
        self._tmp = None

    @classmethod
    def from_name(cls, name: str, version: str) -> TemplateFetcher:
        """Build a new instance from name and version.

        :param name: The name of the template.
        :param version: The version of the template.
        :return: A ``TemplateFetcher`` instance.
        """
        pattern = "/".join([TEMPLATE_URL, "{version}/{name}.tar.gz"])
        url = pattern.format(name=name, version=version)
        return cls(url)

    @property
    def path(self) -> Path:
        """Get the local path of the template.

        :return: A ``Path`` instance.
        """
        return Path(self.tmp.name)

    @property
    def tmp(self) -> TemporaryDirectory:
        """Get the temporal directory in which the template is downloaded.

        :return: A ``TemporaryDirectory`` instance.
        """
        if self._tmp is None:
            cache_dir = Path.home() / ".minos" / "tmp"
            cache_dir.mkdir(parents=True, exist_ok=True)
            tmp = TemporaryDirectory(dir=str(cache_dir))
            self.fetch_tar(self.url, tmp.name)
            self._tmp = tmp
        return self._tmp

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.url!r})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.url == other.url

    @staticmethod
    def fetch_tar(url: str, path: str) -> None:
        """Fetch a tar file from the given url and uncompress it onn the given path.

        :param url: The url of the tar file.
        :param path: The location of the uncompressed file.
        :return: This method does not return anything.
        """
        with console.status(f"Downloading template from {url!r}...", spinner="moon"):
            stream = urllib.request.urlopen(url)
        console.print(f":moon: Downloaded template from {url!r}!\n")

        tar = tarfile.open(fileobj=stream, mode="r|gz")
        with console.status(f"Extracting template into {path!r}...", spinner="moon"):
            tar.extractall(path=path)
        console.print(f":moon: Extracted template into {path!r}!\n")


MICROSERVICE_INIT = TemplateFetcher.from_name("microservice-init", TEMPLATE_VERSION)
PROJECT_INIT = TemplateFetcher.from_name("project-init", TEMPLATE_VERSION)
