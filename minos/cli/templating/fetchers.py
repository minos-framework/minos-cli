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
    Optional,
)

from ..consoles import (
    console,
)

TEMPLATE_URL: Final[str] = "https://github.com/minos-framework/minos-templates/releases/download"
TEMPLATE_VERSION: Final[str] = "v0.2.1"


class TemplateFetcher:
    """Template Fetcher class."""

    def __init__(self, uri: str, metadata: Optional[dict[str, Any]] = None):
        if metadata is None:
            metadata = dict()
        self.uri = uri
        self.metadata = metadata
        self._tmp = None

    @classmethod
    def from_url(cls, url: str) -> TemplateFetcher:
        """Build a new instance from url.

        :param url: The url of the template.
        :return: A ``TemplateFetcher`` instance.
        """
        registry, name = url.rsplit("/", 1)
        stem = name.split(".", 1)[0]
        metadata = {"template_registry": registry, "template_name": stem}
        return cls(url, metadata)

    @classmethod
    def from_path(cls, path: Path) -> TemplateFetcher:
        """Build a new instance from path.

        :param path: The path of the template.
        :return: A ``TemplateFetcher`` instance.
        """
        metadata = {"template_registry": path.parent.as_uri(), "template_name": path.name.split(".", 1)[0]}
        return cls(path.as_uri(), metadata)

    @classmethod
    def from_name(cls, name: str, version: str = TEMPLATE_VERSION) -> TemplateFetcher:
        """Build a new instance from name and version.

        :param name: The name of the template.
        :param version: The version of the template.
        :return: A ``TemplateFetcher`` instance.
        """
        registry = f"{TEMPLATE_URL}/{version}"
        url = f"{registry}/{name}.tar.gz"
        metadata = {"template_registry": registry, "template_version": version, "template_name": name}
        return cls(url, metadata)

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
            self.fetch_tar(self.uri, tmp.name)
            self._tmp = tmp
        return self._tmp

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.uri!r}, {self.metadata!r})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.uri == other.uri and self.metadata == other.metadata

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
