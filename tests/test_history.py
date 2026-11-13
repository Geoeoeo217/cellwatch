from cellwatch.compare import diff
from cellwatch.history import History, format_history
from cellwatch.snapshot import snapshot


def make_history():
    history = History()
    history.record(1, diff(snapshot({}), snapshot({"x": 1, "y": 5})))
    history.record(2, diff(snapshot({"x": 1}), snapshot({"x": 2})))
    return history


def test_entries_can_be_filtered_by_name():
    history = make_history()
    assert len(history) == 3
    assert [cell for cell, _ in history.entries("x")] == [1, 2]


def test_format_history_for_one_variable():
    assert format_history(make_history(), "x").splitlines() == [
        "cellwatch history for 'x':",
        "  [1] + x = 1  (int)",
        "  [2] ~ x: 1 -> 2",
    ]


def test_empty_and_cleared_history():
    history = make_history()
    history.clear()
    assert format_history(history) == "cellwatch: no recorded changes for all variables"
