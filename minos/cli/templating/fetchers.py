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

from ..consoles import (
    console,
)

TEMPLATE_VERSION = "0.0.1.dev0"
TEMPLATE_ARTIFACT_URL = "https://github.com/Clariteia/minos-templates/releases/download/{version}/{name}.tar.gz"


class TemplateFetcher:
    """Template Fetcher class."""

    def __init__(self, name: str, version: str):
        self._name = name
        self._version = version
        self._tmp = None

    @property
    def name(self) -> str:
        """Get the name of the template.

        :return: A ``str`` value.
        """
        return self._name

    @property
    def version(self) -> str:
        """Get the version of the template.

        :return: A ``str`` value.
        """
        return self._version

    @property
    def url(self) -> str:
        """Get the url of the template.

        :return: A ``str`` value.
        """
        return TEMPLATE_ARTIFACT_URL.format(name=self._name, version=self._version)

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
            tmp = TemporaryDirectory()
            self.fetch_tar(self.url, tmp.name)
            self._tmp = tmp
        return self._tmp

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


MICROSERVICE_INIT = TemplateFetcher("microservice-init", TEMPLATE_VERSION)
PROJECT_INIT = TemplateFetcher("project-init", TEMPLATE_VERSION)
