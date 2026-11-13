"""Step 4: remember the changes made by every watched cell."""

from __future__ import annotations

from .compare import Change
from .report import describe


class History:
    """A running log of changes, grouped by the cell that made them."""

    def __init__(self):
        self._entries = []  # list of (cell_number, Change) pairs

    def record(self, cell_number: int, changes: list[Change]) -> None:
        """Add the changes made by one cell."""
        for change in changes:
            self._entries.append((cell_number, change))

    def entries(self, name: str | None = None) -> list[tuple[int, Change]]:
        """All entries, or only those for the variable called ``name``."""
        if name is None:
            return list(self._entries)
        return [entry for entry in self._entries if entry[1].name == name]

    def clear(self) -> None:
        """Forget everything recorded so far."""
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)


def format_history(history: History, name: str | None = None) -> str:
    """A text timeline, one line per change, labelled with its cell number."""
    entries = history.entries(name)
    subject = f"'{name}'" if name else "all variables"
    if not entries:
        return f"cellwatch: no recorded changes for {subject}"
    lines = [f"cellwatch history for {subject}:"]
    lines += [f"  [{cell_number}] {describe(change)}" for cell_number, change in entries]
    return "\n".join(lines)
