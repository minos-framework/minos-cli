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


def fetch_tarfile(url: str, path: str) -> None:
    """TODO"""

    with console.status(f"Downloading template from {url!r}...", spinner="moon"):
        stream = urllib.request.urlopen(url)
    console.print(f":moon: Downloaded template from {url!r}!\n")

    tar = tarfile.open(fileobj=stream, mode="r|gz")
    with console.status(f"Extracting template into {path!r}...", spinner="moon"):
        tar.extractall(path=path)
    console.print(f":moon: Extracted template into {path!r}!\n")


class TemplateFetcher:
    """TODO"""

    def __init__(self, name: str, version: str):
        self._name = name
        self._version = version
        self._tmp = None

    @property
    def url(self) -> str:
        """TODO"""
        return TEMPLATE_ARTIFACT_URL.format(name=self._name, version=self._version)

    @property
    def path(self) -> Path:
        """TODO"""
        return Path(self.tmp.name)

    @property
    def tmp(self) -> TemporaryDirectory:
        """TODO"""
        if self._tmp is None:
            tmp = TemporaryDirectory()
            fetch_tarfile(self.url, tmp.name)
            self._tmp = tmp
        return self._tmp


MICROSERVICE_INIT_TEMPLATE = TemplateFetcher("microservice-init", TEMPLATE_VERSION)
PROJECT_INIT_TEMPLATE = TemplateFetcher("project-init", TEMPLATE_VERSION)
