# scripts/tests/test_scripts.py
import json, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PY = sys.executable

SAMPLE = """---
title: "9. Test chapter"
---

Opening paragraph.

## First section

Text with a citation [@Vaswani2017].

```{code-cell} python
print("hi")
```

## Second section

More text.
"""

def test_md2nb_splits_sections_and_code():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "in.md"); dst = os.path.join(d, "out.ipynb")
        open(src, "w").write(SAMPLE)
        subprocess.run([PY, os.path.join(ROOT, "scripts", "md2nb.py"), src, dst], check=True)
        nb = json.load(open(dst))
        kinds = [c["cell_type"] for c in nb["cells"]]
        assert kinds == ["markdown", "markdown", "markdown", "code", "markdown"], kinds
        assert "".join(nb["cells"][0]["source"]).startswith("---\ntitle")
        assert "".join(nb["cells"][3]["source"]) == 'print("hi")'
        assert nb["cells"][3]["outputs"] == [] and nb["cells"][3]["execution_count"] is None
        assert nb["nbformat"] == 4 and nb["nbformat_minor"] == 5

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok", name)
