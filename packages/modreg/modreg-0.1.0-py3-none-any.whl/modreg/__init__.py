from importlib.metadata import PackageNotFoundError, version

from .registry import Registry

try:
    __version__ = version("modreg")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["Registry", "__version__"]
