import pytest

IPython = pytest.importorskip("IPython")
from IPython.testing.globalipapp import start_ipython


@pytest.fixture(scope="module")
def ip():
    shell = start_ipython() or IPython.get_ipython()
    shell.run_line_magic("load_ext", "cellwatch")
    return shell


def test_cell_magic_reports_changes(ip, capsys):
    ip.run_cell("scores = [3, 1, 2]")
    capsys.readouterr()
    ip.run_cell_magic("cellwatch", "", "scores.sort()\ntotal = sum(scores)")
    out = capsys.readouterr().out
    assert "1 created, 1 changed" in out
    assert "+ total = 6" in out
    assert "~ scores: [3, 1, 2] -> [1, 2, 3]  (modified in place)" in out


def test_auto_mode_on_and_off(ip, capsys):
    ip.run_line_magic("cellwatch", "on")
    ip.run_cell("auto_value = 42")
    assert "+ auto_value = 42" in capsys.readouterr().out
    ip.run_line_magic("cellwatch", "off")
    capsys.readouterr()
    ip.run_cell("another_value = 1")
    assert "another_value" not in capsys.readouterr().out


def test_history_command(ip, capsys):
    ip.run_line_magic("cellwatch", "history total")
    out = capsys.readouterr().out
    assert "cellwatch history for 'total':" in out and "+ total = 6" in out
    ip.run_line_magic("cellwatch", "clear")
    ip.run_line_magic("cellwatch", "history")
    assert "no recorded changes" in capsys.readouterr().out


def test_public_names_are_importable():
    from cellwatch import History, diff, format_changes, snapshot  # noqa: F401


def test_history_uses_the_cell_number(ip, capsys):
    ip.run_line_magic("cellwatch", "clear")
    result = ip.run_cell("%%cellwatch\nnumbered = 1", store_history=True)
    capsys.readouterr()
    ip.run_line_magic("cellwatch", "history numbered")
    assert f"[{result.execution_count}] + numbered = 1" in capsys.readouterr().out
