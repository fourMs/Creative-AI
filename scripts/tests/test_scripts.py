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

CHAPTER_OK = """---
title: "3. Good chapter"
---

Opens by naming the culture layer.

:::{admonition} Research spotlight
:class: spotlight
MishMash.
:::

## This week's lab: Explore, Reflect, Create

### Explore
### Reflect
### Create

## A critical look: is this real?

```{admonition} Chapter summary
:class: tip
Summary.
```

```{admonition} Questions
:class: question
1. Q?
```

:::{seealso} Further reading
- Item https://doi.org/10.1000/xyz
:::

:::{tip} Explore interactively
- App
:::
"""

def _run_checker(md, bib="@article{Vaswani2017, title={x}}"):
    with tempfile.TemporaryDirectory() as d:
        book = os.path.join(d, "book"); os.makedirs(os.path.join(book, "figures", "x"))
        open(os.path.join(book, "figures", "x", "a.svg"), "w").write("<svg/>")
        open(os.path.join(book, "references.bib"), "w").write(bib)
        open(os.path.join(book, "myst.yml"), "w").write("project:\n  toc:\n    - file: ch.ipynb\n")
        src = os.path.join(d, "ch.md"); open(src, "w").write(md)
        subprocess.run([PY, os.path.join(ROOT, "scripts", "md2nb.py"), src, os.path.join(book, "ch.ipynb")], check=True)
        return subprocess.run([PY, os.path.join(ROOT, "scripts", "check-chapters.py"), "--book", book],
                              capture_output=True, text=True)

def test_checker_accepts_good_chapter():
    r = _run_checker(CHAPTER_OK)
    assert r.returncode == 0, r.stdout + r.stderr

def test_checker_flags_wrong_lab_order_and_bad_cite_and_missing_figure():
    bad = CHAPTER_OK.replace("### Explore\n### Reflect\n### Create", "### Reflect\n### Explore\n### Create")
    bad += "\nSee [@Nope2020].\n\n```{figure} figures/x/missing.svg\n:alt: a\nCaption.\n```\n"
    r = _run_checker(bad)
    assert r.returncode == 1
    assert "order" in r.stdout and "Nope2020" in r.stdout and "missing.svg" in r.stdout, r.stdout

def test_checker_skips_template_for_non_chapters():
    page = CHAPTER_OK.replace('title: "3. Good chapter"', 'title: "Tools"').split("## This week")[0]
    r = _run_checker(page)
    assert r.returncode == 0, r.stdout

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok", name)
