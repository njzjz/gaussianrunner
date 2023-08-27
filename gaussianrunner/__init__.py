"""Init."""
import logging

import coloredlogs

try:
    from importlib.metadata import PackageNotFoundError, version
except ModuleNotFoundError:
    from importlib_metadata import PackageNotFoundError, version

from .analyst import GaussianAnalyst
from .runner import GaussianRunner

__all__ = ["GaussianRunner", "GaussianAnalyst"]

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = ""

coloredlogs.install(
    fmt=f"%(asctime)s - GaussianRunner {__version__} - %(levelname)s: %(message)s",
    level=logging.INFO,
    milliseconds=True,
)
