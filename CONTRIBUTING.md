# Working on cellwatch as a team

## Who uploads what

The package is built from five modules. Each module depends only on the ones
above it in this table, so push them **in this order**.

| Order | Person | Files to push |
|---|---|---|
| 0 | Repository owner | `pyproject.toml`, `README.md`, `CONTRIBUTING.md`, `LICENSE`, `.gitignore`, `src/cellwatch/__init__.py` |
| 1 | Member 1 | `src/cellwatch/snapshot.py`, `tests/test_snapshot.py` |
| 2 | Member 2 | `src/cellwatch/compare.py`, `tests/test_compare.py` |
| 3 | Member 3 | `src/cellwatch/report.py`, `tests/test_report.py` |
| 4 | Member 4 | `src/cellwatch/history.py`, `tests/test_history.py` |
| 5 | Member 5 | `src/cellwatch/magic.py`, `tests/test_magic.py` |

The repository owner is also one of the five members. The `%%cellwatch`
command works once all five modules are in.

## One-time setup (every member)

```bash
git clone https://github.com/Geoeoeo217/cellwatch
cd cellwatch
pip install -e ".[dev]"
```

`git clone` downloads the repository. `pip install -e .` is an "editable"
install: Python uses the files in this folder directly, so your edits take
effect without reinstalling.

## Pushing your module

```bash
git pull                     # get your teammates' latest work first
# copy your two files into src/cellwatch/ and tests/
pytest                       # every test must pass
git add src/cellwatch/YOURFILE.py tests/test_YOURFILE.py
git commit -m "Add YOURFILE module: one line on what it does"
git push
```

If `git push` is rejected, a teammate pushed before you: run `git pull` and
then `git push` again.

## After the first five pushes

One commit each is a start, not a "regular commit history". Each member
should own their module from here on and keep improving it:

- **snapshot.py** – option to ignore chosen variable names; faster handling
  of very large values.
- **compare.py** – for lists and dictionaries, say which items were added or
  removed instead of only before/after.
- **report.py** – coloured HTML table for notebooks (green created, yellow
  changed, red deleted).
- **history.py** – limit the history size; export the history as a list of
  dictionaries.
- **magic.py** – `%cellwatch ignore NAME`; a demo notebook in `examples/`
  that doubles as the 1-minute presentation script.

Small, frequent commits with clear messages are better than one big one.

## Publishing to PyPI

1. Fill in the author names in `pyproject.toml`.
2. Raise `version` in `pyproject.toml` and in `src/cellwatch/__init__.py`.
3. `python -m build` creates the files to upload in `dist/`.
4. `twine upload dist/*` uploads them; it asks for a PyPI API token.
