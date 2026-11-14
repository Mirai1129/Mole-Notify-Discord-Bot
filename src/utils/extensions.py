import importlib
import inspect
import pkgutil
from typing import NoReturn


def unqualify(name: str) -> str:
    """Return the unqualified name, i.e. without any preceding module path."""
    return name.rsplit(".", maxsplit=1)[-1]


def walk_extensions(package: str = "src") -> list[str]:
    """Discover all extensions recursively under the package."""
    module = importlib.import_module(package)

    extensions = []

    for module_info in pkgutil.walk_packages(
            module.__path__,
            prefix=f"{package}.",
    ):
        module_name = module_info.name

        # Skip private modules and packages
        if any(
                part.startswith("_")
                for part in module_name.split(".")[1:]
        ):
            continue

        # Skip packages themselves
        if module_info.ispkg:
            continue

        imported = importlib.import_module(module_name)

        if inspect.isfunction(getattr(imported, "setup", None)):
            extensions.append(module_name)

    return extensions
