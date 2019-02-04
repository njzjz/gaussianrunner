"""Init."""
import logging

import coloredlogs
from pkg_resources import DistributionNotFound, get_distribution

from .analyst import GaussianAnalyst
from .runner import GaussianRunner

__all__ = ['GaussianRunner', 'GaussianAnalyst']

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = ''

coloredlogs.install(
    fmt=f'%(asctime)s - GaussianRunner {__version__} - %(levelname)s: %(message)s',
    level=logging.INFO, milliseconds=True)
