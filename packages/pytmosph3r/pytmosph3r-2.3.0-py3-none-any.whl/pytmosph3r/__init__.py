from .__version__ import __version__


if True:
    # Import numpy to enable warnings suppression
    # noinspection PyUnresolvedReferences
    import numpy


# import submodules
# isort: split
# isort: off
from . import atmosphere
from . import chemistry
from . import external
from . import interface
from . import log
from . import model
from . import observations
from . import planetary_system
from . import plot
from . import util
# isort: on

# import files
# isort: split
# isort: off
from . import aerosols
from . import grid
from . import opacity
from . import rays
# isort: on

# import content from files to match old behavior
# isort: split
from .aerosols import PrepareAerosols
from .grid import Grid, Grid3D
from .opacity import Opacity
from .rays import Rays


# import content from submodules to match old behavior
# isort: split
from .atmosphere import *
from .chemistry import *
from .log import *
from .model import *
from .observations import *
from .planetary_system import *
from .plot import *


# import specific content from submodules
# isort: split
from .interface import write_hdf5, write_netcdf
from .interface.hdf5 import HDF5Input, HDF5Output
from .interface.io import write_spectrum
from .interface.netcdf import ncInput, ncOutput
from .util import constants


# from .plot import Plot
# from .plot.plotutils import BasePlot


def debug(value=True):
    """Activates or deactivates debug mode.

    Args:
        value (bool, optional): If True, debug mode. If False, deactivates most of the logging. Defaults to True.
    """
    from .log import criticalLogging, debugLogging
    from .plot import Plot

    if value:
        debugLogging()
    else:
        criticalLogging()
