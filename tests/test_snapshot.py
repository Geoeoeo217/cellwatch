import math

from cellwatch.snapshot import safe_repr, snapshot


def test_records_text_type_and_identity():
    scores = [1, 2]
    record = snapshot({"scores": scores})["scores"]
    assert (record.text, record.type_name, record.identity) == ("[1, 2]", "list", id(scores))


def test_private_names_ipython_names_and_modules_are_skipped():
    assert snapshot({"_hidden": 1, "math": math, "In": [], "x": 1}).keys() == {"x"}


def test_broken_repr_does_not_crash():
    class Broken:
        def __repr__(self):
            raise ValueError("oops")

    assert safe_repr(Broken()).startswith("<unprintable Broken")
