"""Step 2: compare two snapshots and list the differences."""

from __future__ import annotations

from dataclasses import dataclass

from .snapshot import Record

KINDS = ("created", "changed", "deleted")


@dataclass(frozen=True)
class Change:
    """One difference between two snapshots."""

    name: str
    kind: str  # one of KINDS
    before: Record | None  # None when the variable was created
    after: Record | None  # None when the variable was deleted

    @property
    def in_place(self) -> bool:
        """True if the same object was modified, e.g. by ``list.sort()``."""
        return (
            self.kind == "changed"
            and self.before.identity == self.after.identity
            and self.before.type_name == self.after.type_name
        )


def diff(before: dict[str, Record], after: dict[str, Record]) -> list[Change]:
    """List what was created, changed or deleted between two snapshots."""
    changes = []
    # "after.keys() - before.keys()" is the set of names only found in after.
    for name in sorted(after.keys() - before.keys()):
        changes.append(Change(name, "created", None, after[name]))
    # "&" keeps the names found in both snapshots.
    for name in sorted(after.keys() & before.keys()):
        old, new = before[name], after[name]
        if old.text != new.text or old.type_name != new.type_name:
            changes.append(Change(name, "changed", old, new))
    for name in sorted(before.keys() - after.keys()):
        changes.append(Change(name, "deleted", before[name], None))
    return changes


def count_by_kind(changes: list[Change]) -> dict[str, int]:
    """Count the changes of each kind, e.g. {"created": 1, "changed": 2}."""
    counts = {}
    for change in changes:
        counts[change.kind] = counts.get(change.kind, 0) + 1
    return counts
