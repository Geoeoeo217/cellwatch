"""cellwatch: see which variables a Jupyter cell created, changed or deleted."""

__version__ = "0.1.0"

# Public names and the module each one lives in.
_PUBLIC = {
    "Record": "snapshot",
    "snapshot": "snapshot",
    "Change": "compare",
    "diff": "compare",
    "format_changes": "report",
    "History": "history",
    "format_history": "history",
}

__all__ = sorted(_PUBLIC) + ["load_ipython_extension", "unload_ipython_extension"]


def __getattr__(name):
    """Import a public name the first time someone asks for it.

    Python calls this special function when ``cellwatch.<name>`` is not found
    the normal way. Loading modules only when needed keeps each module usable
    on its own.
    """
    if name in _PUBLIC:
        from importlib import import_module

        return getattr(import_module(f".{_PUBLIC[name]}", __name__), name)
    raise AttributeError(f"module 'cellwatch' has no attribute {name!r}")


def load_ipython_extension(ipython):
    """Called by ``%load_ext cellwatch``."""
    from .magic import load

    load(ipython)


def unload_ipython_extension(ipython):
    """Called by ``%unload_ext cellwatch``."""
    from .magic import unload

    unload(ipython)
