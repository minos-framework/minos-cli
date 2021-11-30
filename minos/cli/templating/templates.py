from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from .fetchers import fetch_tarfile

TEMPLATE_VERSION = "0.0.1.dev0"
TEMPLATE_ARTIFACT_URL = "https://github.com/Clariteia/minos-templates/releases/download/{version}/{name}.tar.gz"


class Template:
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


MICROSERVICE_INIT_TEMPLATE = Template("microservice-init", TEMPLATE_VERSION)
PROJECT_INIT_TEMPLATE = Template("project-init", TEMPLATE_VERSION)
