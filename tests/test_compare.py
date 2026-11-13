from cellwatch.compare import count_by_kind, diff
from cellwatch.snapshot import snapshot


def changes_between(before_ns, after_ns):
    return diff(snapshot(before_ns), snapshot(after_ns))


def test_created_and_deleted():
    [created] = changes_between({}, {"x": 1})
    [deleted] = changes_between({"x": 1}, {})
    assert (created.kind, deleted.kind) == ("created", "deleted")


def test_reassigned_variable():
    [change] = changes_between({"x": 1}, {"x": 2})
    assert (change.kind, change.before.text, change.after.text) == ("changed", "1", "2")
    assert not change.in_place


def test_in_place_change_is_detected():
    scores = [3, 1, 2]
    before = snapshot({"scores": scores})
    scores.sort()
    [change] = diff(before, snapshot({"scores": scores}))
    assert change.kind == "changed" and change.in_place


def test_unchanged_variable_is_not_reported():
    assert changes_between({"x": 1}, {"x": 1}) == []


def test_count_by_kind():
    changes = changes_between({"a": 1, "b": 1}, {"a": 2, "c": 3})
    assert count_by_kind(changes) == {"created": 1, "changed": 1, "deleted": 1}
