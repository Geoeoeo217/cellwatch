# Working on cellwatch as a team

## One-time setup

```bash
git clone https://github.com/YOUR-USERNAME/cellwatch
cd cellwatch
pip install -e ".[dev]"
pytest
```

`pip install -e .` is an "editable" install: Python uses the files in this
folder directly, so your edits take effect without reinstalling.

## Every time you make a change

```bash
git pull                              # get your teammates' latest work
git checkout -b short-name-of-change  # work on your own branch
# ...edit files...
pytest                                # all tests must pass
git add -A
git commit -m "Say what changed and why"
git push -u origin short-name-of-change
```

Then open a pull request on GitHub and ask a teammate to look at it.
Small, frequent commits are better than one big one.

## Where things are

| File | What it holds |
|---|---|
| `src/cellwatch/core.py` | Snapshot and diff logic (no Jupyter needed) |
| `src/cellwatch/magic.py` | The `%%cellwatch` and `%cellwatch` commands |
| `tests/` | Automatic tests, run with `pytest` |
| `pyproject.toml` | Package name, version, dependencies |

## Open tasks (pick one each)

1. **Coloured notebook output.** Show the report as an HTML table with green
   (created), yellow (changed) and red (deleted) rows. Start in `magic.py`.
2. **Ignore list.** `%cellwatch ignore name1 name2` hides variables the user
   does not care about. Needs a new option in `magic.py` and a test.
3. **History.** `%cellwatch history x` lists every change made to `x` so far.
4. **Demo notebook.** Add `examples/demo.ipynb` that walks through the use
   cases in the README; this is also the script for the 1-minute presentation.
5. **Documentation site.** Publish the docs with GitHub Pages.
6. **Release.** Fill in the author names and repository links in
   `pyproject.toml`, then publish to PyPI (see below).

## Publishing to PyPI

1. Raise `version` in `pyproject.toml` and in `src/cellwatch/__init__.py`.
2. `python -m build` creates the files to upload in `dist/`.
3. `twine upload dist/*` uploads them; it asks for a PyPI API token.
