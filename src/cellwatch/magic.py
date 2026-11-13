"""Step 5: the Jupyter commands %%cellwatch and %cellwatch."""

from __future__ import annotations

from IPython.core.magic import Magics, line_cell_magic, magics_class

from .compare import diff
from .history import History, format_history
from .report import format_changes
from .snapshot import snapshot

USAGE = """Usage:
  %%cellwatch              report on this cell (first line of the cell)
  %cellwatch on | off      report after every cell / stop
  %cellwatch history       list every recorded change
  %cellwatch history NAME  list the changes made to one variable
  %cellwatch clear         forget the recorded history"""


@magics_class
class CellWatchMagics(Magics):
    """Adds the ``cellwatch`` magic command to a notebook."""

    def __init__(self, shell):
        super().__init__(shell)
        self.history = History()
        self._auto = False
        self._before = None

    @line_cell_magic
    def cellwatch(self, line, cell=None):
        """Report which variables a cell created, changed or deleted."""
        if cell is not None:
            self._run_and_report(cell)
            return
        words = line.split()
        command = words[0].lower() if words else ""
        if command == "on":
            self._set_auto(True)
            print("cellwatch: reporting after every cell (%cellwatch off to stop)")
        elif command == "off":
            self._set_auto(False)
            print("cellwatch: automatic reporting stopped")
        elif command == "history":
            print(format_history(self.history, words[1] if len(words) > 1 else None))
        elif command == "clear":
            self.history.clear()
            print("cellwatch: history cleared")
        else:
            print(USAGE)

    def _run_and_report(self, cell):
        was_auto = self._auto
        self._auto = False  # avoid a second report from automatic mode
        cell_number = self._cell_number()
        before = snapshot(self.shell.user_ns)
        try:
            self.shell.run_cell(cell)
        finally:
            self._auto = was_auto
        changes = diff(before, snapshot(self.shell.user_ns))
        self.history.record(cell_number, changes)
        print(format_changes(changes))

    def _cell_number(self):
        """The number shown as ``In [n]`` beside the cell that is running.

        IPython keeps every cell's code in a list called ``In``; the running
        cell is its last item, so its number is the last index of that list.
        """
        inputs = self.shell.user_ns.get("In", [])
        return max(len(inputs) - 1, 0)

    def _set_auto(self, enabled):
        if enabled == self._auto:
            return
        events = self.shell.events
        if enabled:
            events.register("pre_run_cell", self._pre_run_cell)
            events.register("post_run_cell", self._post_run_cell)
        else:
            events.unregister("pre_run_cell", self._pre_run_cell)
            events.unregister("post_run_cell", self._post_run_cell)
        self._auto = enabled
        self._before = None

    def _pre_run_cell(self, info):
        self._before = snapshot(self.shell.user_ns)

    def _post_run_cell(self, result):
        if self._before is None or not self._auto:
            return
        changes = diff(self._before, snapshot(self.shell.user_ns))
        self._before = None
        if changes:
            self.history.record(self._cell_number(), changes)
            print(format_changes(changes))


_instances = {}


def load(ipython):
    """Register the magic command with a running IPython/Jupyter session."""
    magics = CellWatchMagics(ipython)
    _instances[id(ipython)] = magics
    ipython.register_magics(magics)


def unload(ipython):
    """Stop automatic reporting when the extension is unloaded."""
    magics = _instances.pop(id(ipython), None)
    if magics is not None:
        magics._set_auto(False)
