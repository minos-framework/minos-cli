import importlib.util
from collections.abc import (
    Callable,
)
from pathlib import (
    Path,
)
from types import (
    ModuleType,
)


class FunctionLoader:
    """Function Loader class."""

    @classmethod
    def load_many_from_directory(cls, names: list[str], directory_path: Path) -> dict[str, Callable]:
        """Load multiple functions.

        :param names: The function names.
        :param directory_path: The directory path.
        :return: A mapping from function name to function itself.
        """
        ans = dict()
        for name in names:
            fn = cls.load_one_from_directory(name, directory_path)
            ans[fn.__name__] = fn
        return ans

    @classmethod
    def load_one_from_directory(cls, name: str, directory_path: Path) -> Callable:
        """Load one function.

        :param name: The function name.
        :param directory_path: The directory path.
        :return: A function.
        """
        module_name, fn = name.rsplit(".", 1)
        module = cls.load_module_from_file(directory_path / f"{module_name}.py")
        fn = getattr(module, fn)
        return fn

    @staticmethod
    def load_module_from_file(file_path: Path) -> ModuleType:
        """Load a module from file path.

        :param file_path: The module's file path.
        :return: A module.
        """

        spec = importlib.util.spec_from_file_location(file_path.name.split(".", 1)[0], str(file_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
