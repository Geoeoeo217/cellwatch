"""Step 1: take a snapshot (a record of every user variable at one moment)."""

from __future__ import annotations

import types
from dataclasses import dataclass

# Names that IPython itself puts in the notebook; not the user's variables.
IPYTHON_NAMES = {"In", "Out", "exit", "quit", "get_ipython", "open"}


@dataclass(frozen=True)
class Record:
    """What we remember about one variable at one moment."""

    text: str  # repr() of the value, i.e. how Python prints it
    type_name: str  # e.g. "list"
    identity: int  # id() of the object; same id means same object


def is_user_variable(name: str, value: object) -> bool:
    """Return False for private names, IPython's own names and modules."""
    if name.startswith("_"):
        return False
    if name in IPYTHON_NAMES:
        return False
    if isinstance(value, types.ModuleType):
        return False
    return True


def safe_repr(value: object) -> str:
    """Like repr(), but never raises an error."""
    try:
        return repr(value)
    except Exception as error:  # a broken __repr__ must not break the report
        return f"<unprintable {type(value).__name__}: {error}>"


def snapshot(namespace: dict) -> dict[str, Record]:
    """Record the current state of every user variable in ``namespace``.

    ``namespace`` is a dictionary of variable names to values, for example
    ``globals()`` or a notebook's ``user_ns``.
    """
    return {
        name: Record(safe_repr(value), type(value).__name__, id(value))
        for name, value in list(namespace.items())
        if is_user_variable(name, value)
    }
