"""Step 3: turn a list of changes into a short, readable text report."""

from __future__ import annotations

from .compare import KINDS, Change, count_by_kind

MAX_WIDTH = 60  # longest value text shown in a report


def shorten(text: str, width: int = MAX_WIDTH) -> str:
    """Put ``text`` on one line and cut it to ``width`` characters."""
    text = " ".join(text.split())
    return text if len(text) <= width else text[: width - 3] + "..."


def describe(change: Change) -> str:
    """One report line: ``+`` created, ``~`` changed, ``-`` deleted."""
    if change.kind == "created":
        return f"+ {change.name} = {shorten(change.after.text)}  ({change.after.type_name})"
    if change.kind == "deleted":
        return f"- {change.name}  (was {shorten(change.before.text)})"
    line = f"~ {change.name}: {shorten(change.before.text)} -> {shorten(change.after.text)}"
    if change.before.type_name != change.after.type_name:
        line += f"  (type {change.before.type_name} -> {change.after.type_name})"
    elif change.in_place:
        line += "  (modified in place)"
    return line


def summarize(changes: list[Change]) -> str:
    """A one-line count such as ``1 created, 2 changed``."""
    counts = count_by_kind(changes)
    return ", ".join(f"{counts[kind]} {kind}" for kind in KINDS if kind in counts)


def format_changes(changes: list[Change]) -> str:
    """The full report for one cell."""
    if not changes:
        return "cellwatch: no variables changed"
    lines = ["cellwatch: " + summarize(changes)]
    lines += ["  " + describe(change) for change in changes]
    return "\n".join(lines)
