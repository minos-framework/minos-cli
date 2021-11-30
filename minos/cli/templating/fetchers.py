import urllib.request
import tarfile

from minos.cli import console


def fetch_tarfile(url: str, path: str) -> None:
    """TODO"""

    with console.status(f"Downloading template from {url!r}...", spinner="moon"):
        stream = urllib.request.urlopen(url)
    console.print(f":moon: Downloaded template from {url!r}!\n")

    tar = tarfile.open(fileobj=stream, mode="r|gz")
    with console.status(f"Extracting template into {path!r}...", spinner="moon"):
        tar.extractall(path=path)
    console.print(f":moon: Extracted template into {path!r}!\n")
