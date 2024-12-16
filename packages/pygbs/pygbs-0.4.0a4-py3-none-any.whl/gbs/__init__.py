import warnings

from pygbs.core import *
from pygbs.interpolate import *
from pygbs.tools import *
from pygbs.analysis import *
from pygbs.transform import *
try:
    from build import *
except ImportError:
    warnings.warn(
        "build module not available.",
        ImportWarning,
        stacklevel=2
    )

warnings.warn(
    "Importing from `gbs` is deprecated. Please import from submodules.",
    DeprecationWarning,
    stacklevel=2,
)