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

STYLE_VIOLATIONS_MD = """# Show, don't tell

This chapter **really** matters for the argument, and it don't make sense otherwise.

Moreover, the seminar was cancelled today.

We will now see how this fits into the wider story of the course.

I disagree with this reading, and I want to explain exactly why.

This sentence keeps going and going without much of a point just to push the total count of words past the forty word threshold so that the checker has something long enough to flag as a long sentence for the test to verify properly today.

This is audio-visual content that mixes the two channels.

Wow, this is surprising!

This has one em dash — right there in a sentence.
"""

STYLE_CLEAN_MD = """# Show, don't tell

**The claim.** This paragraph opens with an allowed critical-look label.

- **Term.** A list item may start with a bold lead like this one.

This is a plain sentence with no problems in it at all.

:::{seealso} Further reading
- **Author, Title (2020)** — a short annotated note about the reading itself.
:::

:::{tip} Explore interactively
- [App](https://example.org/app): don't worry, this app link isn't checked for style at all!
:::
"""


def test_style_checker_flags_each_violation():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "ch.md"); open(src, "w").write(STYLE_VIOLATIONS_MD)
        r = subprocess.run([PY, os.path.join(ROOT, "scripts", "check-style.py"), "--files", src],
                            capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
        for category in ["contraction", "bold-in-sentence", "paragraph-opener", "long-sentence",
                          "audiovisual", "first-person", "lecturer-we", "exclamation", "em-dash"]:
            assert f": {category}:" in r.stdout, f"missing {category} in:\n{r.stdout}"


def test_style_checker_strict_fails_on_violations():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "ch.md"); open(src, "w").write(STYLE_VIOLATIONS_MD)
        r = subprocess.run([PY, os.path.join(ROOT, "scripts", "check-style.py"), "--files", src, "--strict"],
                            capture_output=True, text=True)
        assert r.returncode == 1, r.stdout + r.stderr


def test_style_checker_accepts_clean_fixture():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "ch.md"); open(src, "w").write(STYLE_CLEAN_MD)
        r = subprocess.run([PY, os.path.join(ROOT, "scripts", "check-style.py"), "--files", src, "--strict"],
                            capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr


def test_style_checker_bold_titled_list_item_exempt_from_em_dash():
    # A "- **Title** — description" item outside Further reading is still the
    # reading-list/tool-list title-dash-description convention, not the
    # mid-sentence drama dash rule 13 warns about.
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "ch.md")
        open(src, "w").write("- **Title** — a description of the linked or cited work.\n")
        r = subprocess.run([PY, os.path.join(ROOT, "scripts", "check-style.py"), "--files", src],
                            capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
        assert ": em-dash:" not in r.stdout, r.stdout


def test_style_checker_italic_example_exempt_from_first_person():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "ch.md")
        open(src, "w").write("A hedge phrase to avoid is *I am not sure*, used here as an example.\n")
        r = subprocess.run([PY, os.path.join(ROOT, "scripts", "check-style.py"), "--files", src],
                            capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
        assert ": first-person:" not in r.stdout, r.stdout


def test_style_checker_quoted_audiovisual_exempt_but_bare_flagged():
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "ch.md")
        open(src, "w").write(
            'The style guide says not to write "audiovisual" in this book, '
            "but audiovisual still appears here.\n"
        )
        r = subprocess.run([PY, os.path.join(ROOT, "scripts", "check-style.py"), "--files", src],
                            capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
        assert r.stdout.count(": audiovisual:") == 1, r.stdout


def _style_stdout(md, *extra):
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "ch.md"); open(src, "w").write(md)
        r = subprocess.run([PY, os.path.join(ROOT, "scripts", "check-style.py"), "--files", src, *extra],
                            capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
        return r.stdout


def _load_check_style():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "check_style", os.path.join(ROOT, "scripts", "check-style.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# A 45-word sentence carrying two Markdown links and one citation. Counted by
# visible text it is over forty words; counted by raw tokens each link would
# collapse to one word and the sentence would slip under the limit.
LINK_HEAVY_MD = (
    "The [history of generative art](https://en.wikipedia.org/wiki/Generative_art) "
    "and the [transformer architecture](https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)) "
    "both matter here [@Vaswani2017], because the tools that students reach for today "
    "grew out of a long tradition of rule-based making that is worth knowing about "
    "before anyone in the class starts to prompt a model.\n"
)


def test_style_checker_counts_link_text_in_long_sentences():
    out = _style_stdout(LINK_HEAVY_MD)
    assert out.count(": long-sentence:") == 1, out


def test_style_checker_does_not_split_sentence_at_link_destination():
    mod = _load_check_style()
    line = ("The next chapter on [sound](sound.ipynb) picks the thread up again and "
            "shows how the same idea works for audio material.")
    assert len(line.split()) == 20, line.split()
    sentences = mod.sentences_of(mod.normalise_links(line))
    assert len(sentences) == 1, sentences


ADMONITION_MD = """```{admonition} Chapter summary
:class: tip
This summary sentence keeps going and going without much of a point at all, just to push the total count of words well past the forty word threshold so that the checker has something long enough to flag inside a fenced admonition body.
```
"""

CODE_CELL_MD = """```{code-cell} python
# This comment keeps going and going without much of a point at all, just to push the total count of words well past the forty word threshold so that the checker would flag it if code cell bodies were ever read as prose.
print("hi")
```
"""


def test_style_checker_reads_fenced_admonition_body_as_prose():
    out = _style_stdout(ADMONITION_MD)
    assert out.count(": long-sentence:") == 1, out
    assert ": bold-in-sentence:" not in out, out


def test_style_checker_ignores_fenced_code_cell_body():
    out = _style_stdout(CODE_CELL_MD)
    assert ": long-sentence:" not in out, out


# Five lines of front matter, then a violation on line 9. Blanking the front
# matter rather than deleting it keeps the reported line number honest.
FRONT_MATTER_MD = """---
title: "9. Test chapter"
subtitle: "A fixture"
author: "Nobody"
---

Opening paragraph.

This line uses a contraction, so it isn't clean prose.
"""


def test_style_checker_line_numbers_survive_front_matter():
    assert FRONT_MATTER_MD.split("\n")[8].startswith("This line uses a contraction")
    out = _style_stdout(FRONT_MATTER_MD)
    assert ":9: contraction:" in out, out


def test_style_checker_full_stop_after_bare_url_ends_sentence():
    mod = _load_check_style()
    line = "See https://example.com. Next sentence."
    sentences = mod.sentences_of(mod.normalise_links(line))
    assert len(sentences) == 2, sentences


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print("ok", name)
