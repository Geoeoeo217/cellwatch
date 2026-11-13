from cellwatch.compare import diff
from cellwatch.report import format_changes, shorten
from cellwatch.snapshot import snapshot


def report(before_ns, after_ns):
    return format_changes(diff(snapshot(before_ns), snapshot(after_ns)))


def test_no_changes():
    assert report({"x": 1}, {"x": 1}) == "cellwatch: no variables changed"


def test_full_report():
    text = report({"a": 1, "b": "old"}, {"a": 2, "c": [1]})
    assert text.splitlines() == [
        "cellwatch: 1 created, 1 changed, 1 deleted",
        "  + c = [1]  (list)",
        "  ~ a: 1 -> 2",
        "  - b  (was 'old')",
    ]


def test_type_change_is_mentioned():
    assert "(type int -> str)" in report({"x": 1}, {"x": "1"})


def test_long_values_are_shortened():
    assert len(shorten("x" * 500)) == 60
    assert all(len(line) < 100 for line in report({}, {"big": list(range(1000))}).splitlines())
