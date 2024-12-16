import warnings

from core import *
from interpolate import *
from tools import *
from analysis import *
from transform import *
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