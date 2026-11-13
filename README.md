# cellwatch

See exactly which variables a Jupyter cell **created**, **changed** or **deleted**.

```text
%%cellwatch
scores.sort()
total = sum(scores)
del draft
```

```text
cellwatch: 1 created, 1 changed, 1 deleted
  + total = 6  (int)
  ~ scores: [3, 1, 2] -> [1, 2, 3]  (modified in place)
  - draft  (was 'old text')
```

## Motivation

In a notebook, variables live on after a cell finishes, and any later cell can
quietly change them. Beginners often get stuck because a cell changed something
they did not expect: a list was sorted in place, a name was reused, or a
variable was overwritten by a cell that was run twice. Jupyter can list the
variables that exist right now (`%whos`), but it cannot tell you what a cell
just did to them.

## What is new

- **A per-cell diff of variables.** `cellwatch` records the variables before a
  cell runs, records them again afterwards, and reports only the differences.
- **It spots in-place changes.** `scores.sort()` does not assign anything, so
  it is easy to miss. `cellwatch` labels it `modified in place`.
- **It complements existing tools.** `%whos` lists variables but shows no
  changes. [Kishu](https://github.com/illinoisdata/kishu) can undo a cell but
  does not explain what the cell changed. `cellwatch` is the explaining part,
  with one small dependency (IPython, which Jupyter already includes).

## Install

```bash
pip install cellwatch
```

## Usage

Load the extension once per notebook:

```python
%load_ext cellwatch
```

**Report on one cell** by putting `%%cellwatch` on its first line:

```python
%%cellwatch
x = 10
```

**Report after every cell** until you switch it off:

```python
%cellwatch on
...
%cellwatch off
```

How to read a report:

| Symbol | Meaning |
|---|---|
| `+` | the variable was created |
| `~` | the variable's value changed (`before -> after`) |
| `-` | the variable was deleted |

Imported modules and names starting with `_` are not reported.

**Use it from plain Python** (no notebook needed):

```python
from cellwatch import snapshot, diff, format_changes

before = snapshot(globals())
data = [1, 2, 3]
print(format_changes(diff(before, snapshot(globals()))))
```

## Example use cases

- **Debugging a surprise.** A result is wrong and you suspect an earlier cell.
  Turn on `%cellwatch on`, rerun the cells, and read what each one touched.
- **Learning mutation vs. reassignment.** Compare `b = a` then `b.append(4)`
  with `b = a + [4]`: the report shows that the first also changes `a`.
- **Teaching and demos.** An instructor can show the effect of each cell
  without adding `print` statements everywhere.
- **Checking a notebook before submission.** Confirm that a cell does not
  overwrite a variable another cell depends on.

## Limitations

- Changes are detected by comparing the printed form (`repr`) of each value,
  so an object whose printed form stays the same is reported as unchanged.
- Very large values can make each report slower, because they are printed
  twice per cell.

## Development

```bash
git clone https://github.com/YOUR-USERNAME/cellwatch
cd cellwatch
pip install -e ".[dev]"
pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for how the team works and what is left
to build.

## License

MIT
