"""cellwatch: see which variables a Jupyter cell created, changed or deleted."""

from .core import Change, diff, format_changes, snapshot
from .magic import load_ipython_extension, unload_ipython_extension

__version__ = "0.1.0"

__all__ = [
    "Change",
    "snapshot",
    "diff",
    "format_changes",
    "load_ipython_extension",
    "unload_ipython_extension",
]
