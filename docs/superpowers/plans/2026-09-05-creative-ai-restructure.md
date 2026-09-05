# Creative AI Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the *Creative AI* open textbook into the twelve-week structure, chapter template, extra pages, standalone web apps, and CI checks defined in the spec.

**Architecture:** Chapters stay as markdown-only Jupyter notebooks under `book/`, authored as Markdown and converted with a small script so that every H2 section is one cell. A template checker enforces the chapter shape and catches broken citations and figure paths. Apps are single-file HTML under `book/apps/` copied into the built site. Old chapters are renamed with `git mv` and rewritten in place so content and history survive.

**Tech Stack:** MyST Markdown, mystmd 1.6, Jupyter Book 2, Python 3.11 (numpy, matplotlib), vanilla HTML/CSS/JS with WebAudio, GitHub Actions, markdown-link-check, pa11y.

**Spec:** `docs/superpowers/specs/2026-09-05-creative-ai-restructure-design.md`

## Global Constraints

- 12 teaching weeks, each with three 45-minute blocks: a 45-minute lecture and a 90-minute lab; the Synthetic Gallery is in the exam period.
- Lab order is always **Explore (about 30 min), Reflect (about 15 min), Create (about 45 min)**, then the log at home. The acronym is ERC everywhere.
- No programming prerequisite; code only inside `:::{note} Dig deeper: ...` notes or optional exercises.
- `myst build --html --execute` must pass. Executed cells run offline in CI in under a minute each, with no GPU, API key, or network. Heavy or paid code stays as non-executed fenced listings.
- Web apps: one `index.html` per folder under `book/apps/<name>/`, client-side only, no network after load, no keys, bundled data at most a few megabytes with a stated licence, same CSS variables and palette as `sensingsoundandmusic/book/apps/tap-sync/index.html`, max width 780 px, keyboard operable.
- Every further-reading item and every new bib entry has a DOI or URL.
- Chapter template order: front matter; opening paragraph naming the layer(s); prose sections with Dig deeper notes; Research spotlight; optional "If you took MUS2640" note; `## This week's lab: Explore, Reflect, Create`; `## A critical look: ...`; Chapter summary; Questions; Further reading; Explore interactively.
- Writing style: second person, British spelling with -ise, short paragraphs, describe before you interpret, product names only on the tools page and in Dig deeper notes, bold a term only at first definition, every capability claim carries a year, cite with `[@Key]`.
- Admonition classes: `question`, `tip`, `note` (Dig deeper), `important`, `spotlight`, `seealso`.
- Layers: **data, model, interface, practice, culture**. Concepts: **intentionality, aesthetic control, ethical authorship**.
- Figures live in `book/figures/<chapter-file-stem>/`; cover art stays in `book/figures/cover/`.
- Commit after every task with a descriptive message ending in `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Run every command from the repository root `/home/alexanje/github/Creative-AI` with the virtual environment active: `source .venv/bin/activate`.

---

## File structure

| Path | Responsibility |
| --- | --- |
| `scripts/md2nb.py` | Convert a Markdown chapter to a notebook: front matter cell, one cell per H2 section, `{code-cell}` fences become code cells. |
| `scripts/check-chapters.py` | Enforce the chapter template, cite keys, figure paths for every file in the TOC. |
| `scripts/tests/test_scripts.py` | Plain-assert tests for the two scripts, run with `python scripts/tests/test_scripts.py`. |
| `scripts/verify-book-build.sh` | Local build mirror of CI; also copies apps. |
| `.github/workflows/deploy.yml`, `linkcheck.yml`, `accessibility.yml` | CI. |
| `book/myst.yml` | TOC and site config. |
| `book/intro.ipynb` | Course overview. |
| `book/introduction.ipynb` … `book/body.ipynb` | Twelve chapters, file stems as in the spec schedule. |
| `book/tips-and-tricks.ipynb`, `book/glossary.md`, `book/tools.md`, `book/gallery.md` | Extra pages. |
| `book/templates/practice-log.md`, `book/templates/gallery-page.md` | Student templates. |
| `book/apps/<name>/index.html`, `book/apps/README.md` | Standalone apps. |
| `book/figures/<chapter>/` | Figures per chapter. |
| `book/references.bib` | Bibliography. |
| `README.md` | Repository description. |

Chapter file stems and numbers: 1 `introduction`, 2 `how-it-works`, 3 `co-creation-and-ethics`, 4 `language`, 5 `images`, 6 `sound`, 7 `video`, 8 `spatial`, 9 `code`, 10 `multimodal`, 11 `agents`, 12 `body`.

---

## Phase 0: tooling

### Task 1: Markdown-to-notebook converter

**Files:**
- Create: `scripts/md2nb.py`
- Create: `scripts/tests/test_scripts.py`

**Interfaces:**
- Produces: `python scripts/md2nb.py <input.md> <output.ipynb>`. Input rules: an optional YAML front matter block delimited by `---` lines at the top becomes the first markdown cell (including the delimiters); every line starting with `## ` starts a new markdown cell; a fence opening with ```` ```{code-cell} python ```` and closing with ```` ``` ```` becomes a code cell with empty outputs and `execution_count: null`. Everything else is markdown. Notebook JSON is written with `indent=1` and a trailing newline, nbformat 4.5, kernelspec python3, each markdown cell with `"metadata": {"language": "markdown"}`.

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python scripts/tests/test_scripts.py`
Expected: `FileNotFoundError` or `CalledProcessError` because `scripts/md2nb.py` does not exist.

- [ ] **Step 3: Write the converter**

```python
#!/usr/bin/env python3
"""Convert a Markdown chapter to a markdown-cell notebook.

Usage: python scripts/md2nb.py input.md output.ipynb

Rules: front matter (--- ... ---) is the first cell; each `## ` heading starts
a new markdown cell; ```{code-cell} python fences become code cells.
"""
import json, sys

def lines_to_source(text):
    text = text.strip("\n")
    if not text:
        return []
    parts = text.split("\n")
    return [p + "\n" for p in parts[:-1]] + [parts[-1]]

def md_cell(text):
    return {"cell_type": "markdown", "metadata": {"language": "markdown"}, "source": lines_to_source(text)}

def code_cell(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": lines_to_source(text)}

def convert(md):
    lines = md.split("\n")
    cells, buf, i = [], [], 0
    if lines and lines[0].strip() == "---":
        j = 1
        while j < len(lines) and lines[j].strip() != "---":
            j += 1
        cells.append(md_cell("\n".join(lines[: j + 1])))
        i = j + 1
    def flush():
        if "".join(buf).strip():
            cells.append(md_cell("\n".join(buf)))
        buf.clear()
    while i < len(lines):
        line = lines[i]
        if line.startswith("```{code-cell}"):
            flush()
            i += 1; code = []
            while i < len(lines) and lines[i].strip() != "```":
                code.append(lines[i]); i += 1
            cells.append(code_cell("\n".join(code)))
            i += 1
            continue
        if line.startswith("## ") and buf:
            flush()
        buf.append(line); i += 1
    flush()
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    nb = convert(open(src, encoding="utf-8").read())
    with open(dst, "w", encoding="utf-8") as fh:
        json.dump(nb, fh, indent=1, ensure_ascii=False); fh.write("\n")
    print(f"wrote {dst}: {len(nb['cells'])} cells")
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python scripts/tests/test_scripts.py`
Expected: `ok test_md2nb_splits_sections_and_code`

- [ ] **Step 5: Commit**

```bash
git add scripts/md2nb.py scripts/tests/test_scripts.py
git commit -m "Add Markdown-to-notebook converter with test

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 2: Chapter template checker

**Files:**
- Create: `scripts/check-chapters.py`
- Modify: `scripts/tests/test_scripts.py`

**Interfaces:**
- Produces: `python scripts/check-chapters.py [--book book]` exits 0 when every TOC file passes, else prints `path: problem` lines and exits 1. A file is a **chapter** when its front-matter title matches `^"?\d+\. `. Chapters must contain, in this order, these markers as substrings of the concatenated markdown: `## This week's lab: Explore, Reflect, Create`, `### Explore`, `### Reflect`, `### Create`, `## A critical look:`, ```` ```{admonition} Chapter summary ````, ```` ```{admonition} Questions ````, `:::{seealso} Further reading`, `:::{tip} Explore interactively`; and must contain `:::{admonition} Research spotlight` anywhere before the lab. All TOC files: every `[@Key]` or `[@Key1; @Key2]` key must exist in `book/references.bib`; every `figures/...` path referenced in `{figure}`, `{image}`, or `![...](...)` must exist relative to `book/`.

- [ ] **Step 1: Add failing tests**

Append to `scripts/tests/test_scripts.py` before the `if __name__` block:

```python
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python scripts/tests/test_scripts.py`
Expected: the first new test fails with `FileNotFoundError` for `check-chapters.py`.

- [ ] **Step 3: Write the checker**

```python
#!/usr/bin/env python3
"""Check every TOC file against the chapter template, cite keys, and figure paths.

Usage: python scripts/check-chapters.py [--book book]
Exit 0 when clean; otherwise print `file: problem` lines and exit 1.
"""
import argparse, json, os, re, sys

ORDERED = [
    "## This week's lab: Explore, Reflect, Create",
    "### Explore", "### Reflect", "### Create",
    "## A critical look:",
    "```{admonition} Chapter summary",
    "```{admonition} Questions",
    ":::{seealso} Further reading",
    ":::{tip} Explore interactively",
]
SPOTLIGHT = ":::{admonition} Research spotlight"
CITE_RE = re.compile(r"\[@([^\]]+)\]")
FIG_RE = re.compile(r"(?:\{figure\}|\{image\}|\]\()\s*(figures/[^\s\)]+)")
TITLE_RE = re.compile(r'^title:\s*"?(\d+)\.\s', re.M)

def text_of(path):
    if path.endswith(".ipynb"):
        nb = json.load(open(path, encoding="utf-8"))
        return "\n\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "markdown")
    return open(path, encoding="utf-8").read()

def toc_files(book):
    files, in_toc = [], False
    for line in open(os.path.join(book, "myst.yml"), encoding="utf-8"):
        s = line.strip()
        if s.startswith("toc:"):
            in_toc = True; continue
        if in_toc:
            if s.startswith("- file:"):
                files.append(s.split(":", 1)[1].strip())
            elif s and not s.startswith("-") and not s.startswith("#"):
                in_toc = False
    return files

def bib_keys(book):
    return set(re.findall(r"^@\w+\{([^,]+),", open(os.path.join(book, "references.bib"), encoding="utf-8").read(), re.M))

def check(book):
    problems, keys = [], bib_keys(book)
    for rel in toc_files(book):
        path = os.path.join(book, rel)
        if not os.path.exists(path):
            problems.append(f"{rel}: missing file"); continue
        text = text_of(path)
        for m in CITE_RE.finditer(text):
            for key in [k.strip().lstrip("@") for k in m.group(1).split(";")]:
                if key not in keys:
                    problems.append(f"{rel}: unknown cite key {key}")
        for m in FIG_RE.finditer(text):
            if not os.path.exists(os.path.join(book, m.group(1))):
                problems.append(f"{rel}: missing figure {m.group(1)}")
        if not TITLE_RE.search(text):
            continue
        pos = -1
        for marker in ORDERED:
            at = text.find(marker, pos + 1)
            if at == -1:
                problems.append(f"{rel}: missing or out of order marker {marker!r} (template order)")
            else:
                pos = at
        lab = text.find(ORDERED[0]); spot = text.find(SPOTLIGHT)
        if spot == -1 or (lab != -1 and spot > lab):
            problems.append(f"{rel}: Research spotlight missing or after the lab")
    return problems

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--book", default="book")
    probs = check(ap.parse_args().book)
    for p in probs:
        print(p)
    print("OK: all TOC files pass" if not probs else f"{len(probs)} problem(s)")
    sys.exit(1 if probs else 0)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python scripts/tests/test_scripts.py`
Expected: four `ok` lines.

- [ ] **Step 5: Run the checker on the current book and record the baseline**

Run: `python scripts/check-chapters.py`
Expected: exit 1, with every current chapter listed as missing the template markers (they still use Reflect, Explore, Create). This is the expected starting state; do not fix anything now.

- [ ] **Step 6: Commit**

```bash
git add scripts/check-chapters.py scripts/tests/test_scripts.py
git commit -m "Add chapter template checker with tests

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

## Phase 1: infrastructure

### Task 3: CI workflows, verify script, apps folder

**Files:**
- Create: `.github/workflows/linkcheck.yml`, `.github/workflows/accessibility.yml`
- Modify: `.github/workflows/deploy.yml`, `scripts/verify-book-build.sh`
- Create: `book/apps/README.md`

- [ ] **Step 1: Add the link-check workflow**

```yaml
# .github/workflows/linkcheck.yml
name: Link Check
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  link-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: '20'
      - run: npm install -g markdown-link-check
      - name: Check Markdown links
        run: |
          find . -name '*.md' -not -path './.git/*' -not -path './book/_build/*' -not -path './.venv/*' -not -path './notes/*' -print0 \
            | xargs -0 -I{} markdown-link-check -q {}
```

- [ ] **Step 2: Add the accessibility workflow**

```yaml
# .github/workflows/accessibility.yml
name: Accessibility Check (pa11y)
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  pa11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v6
        with:
          python-version: '3.11'
      - run: |
          python -m pip install --upgrade pip
          pip install "jupyter-book>=2.0.0a0" "mystmd==1.6.0"
          pip install -r requirements.txt
      - uses: actions/setup-node@v5
        with:
          node-version: '20'
      - name: Build HTML
        run: |
          cd book
          myst build --html
          cp -r apps _build/html/apps
      - run: npm install -g pa11y http-server
      - name: Serve and check
        run: |
          http-server ./book/_build/html -p 8080 &
          sleep 3
          pa11y http://127.0.0.1:8080 || true
          for app in book/apps/*/; do
            name=$(basename "$app")
            [ -f "$app/index.html" ] && pa11y "http://127.0.0.1:8080/apps/$name/" || true
          done
```

- [ ] **Step 3: Copy apps in the deploy workflow and add the checker**

In `.github/workflows/deploy.yml`, replace the build step:

```yaml
      - name: Check chapter template, citations, and figures
        run: python scripts/check-chapters.py

      - name: Build Jupyter Book HTML
        run: |
          cd book
          myst build --html --execute
          # Copy the bundled web apps to a stable top-level path (/apps/...).
          cp -r apps _build/html/apps
```

- [ ] **Step 4: Update the verify script**

```bash
#!/usr/bin/env bash
# Full HTML build with notebook execution — matches .github/workflows/deploy.yml.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v myst >/dev/null 2>&1; then
  echo "myst not found. Install: pip install -r requirements.txt" >&2
  exit 1
fi

echo "Checking chapter template, citations, and figures..."
python scripts/check-chapters.py

cd book
echo "Running: myst build --html --execute (same as CI deploy)..."
myst build --html --execute
# Mirror the deploy workflow: copy bundled web apps to a stable top-level path.
cp -r apps _build/html/apps
echo "OK: book built with all notebooks executed."
```

- [ ] **Step 5: Create the apps README**

```markdown
# Bundled web apps

Self-contained, browser-based apps used by the book. Each app is a single
`index.html` that runs offline, sends no data anywhere, and needs no account.
They are copied into the deployed site under `/apps/` by
`.github/workflows/deploy.yml` and `scripts/verify-book-build.sh`.

Conventions: same CSS variables and light/dark palette as the apps in the
*Sensing Sound and Music* book, system font, max width 780 px, keyboard
operable, one intro paragraph stating what the app shows and that nothing
leaves the browser. Bundled data files list their licence here.

| App | Chapter | Bundled data |
| --- | --- | --- |
```

- [ ] **Step 6: Verify the checker still fails (baseline) and the verify script runs the checker**

Run: `bash scripts/verify-book-build.sh; echo "exit $?"`
Expected: the checker prints the baseline problems and the script exits 1 before building. That is correct until the chapters are rewritten.

- [ ] **Step 7: Commit**

```bash
git add .github/workflows scripts/verify-book-build.sh book/apps/README.md
git commit -m "Add link-check and accessibility workflows; copy apps and run checker in builds

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 4: Figures into per-chapter folders

**Files:**
- Move: `book/figures/*.svg` into `book/figures/<chapter>/`
- Modify: the notebooks that reference them

- [ ] **Step 1: Move the figures**

```bash
cd book/figures
mkdir -p introduction how-it-works images sound video multimodal
git mv timeline.svg introduction/
git mv ml-pipeline.svg how-it-works/
git mv conditioning.svg how-it-works/
git mv diffusion.svg images/
git mv spectrogram.svg sound/
git mv video.svg video/
git mv multimodal.svg multimodal/
cd ../..
```

- [ ] **Step 2: Update the paths in the current notebooks**

```bash
sed -i 's#figures/timeline.svg#figures/introduction/timeline.svg#' book/introduction.ipynb
sed -i 's#figures/ml-pipeline.svg#figures/how-it-works/ml-pipeline.svg#' book/foundations.ipynb
sed -i 's#figures/conditioning.svg#figures/how-it-works/conditioning.svg#' book/generative-ai.ipynb
sed -i 's#figures/diffusion.svg#figures/images/diffusion.svg#' book/ai-images.ipynb
sed -i 's#figures/spectrogram.svg#figures/sound/spectrogram.svg#' book/ai-sound.ipynb
sed -i 's#figures/video.svg#figures/video/video.svg#' book/ai-video.ipynb
sed -i 's#figures/multimodal.svg#figures/multimodal/multimodal.svg#' book/multimodal-agents.ipynb
```

- [ ] **Step 3: Verify no missing figures**

Run: `python scripts/check-chapters.py | grep "missing figure"; echo "exit $?"`
Expected: no lines printed and `exit 1` from grep (no matches).

- [ ] **Step 4: Commit**

```bash
git add -A book/figures book/*.ipynb
git commit -m "Move figures into per-chapter folders

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 5: Bibliography additions

**Files:**
- Modify: `book/references.bib`

**Interfaces:**
- Produces the cite keys used by every chapter task: `Vear2021`, `Riaz2026`, `Newen2018`, `Jensenius2022`, `GodoyLeman2010`, `Clarke2005`, `Leman2007`, `Briot2020`, `Sturm2019`, `Bretan2016`, `Bringsjord2001`, `Liang2023`, `Luccioni2024`, `Carlini2023`, `Somepalli2023`, `Slater2009`, `Kazemitabaar2023`, `Prather2023`, `Wei2022`, `METR2025`, `Rahmanzadehgervi2024`, `Bruce2024`, `Caillon2021`, `ClarkChalmers1998`, `Kolb1984`, `Roose2022`, `C2PA`, `AMBIENT`, `MusicLab`, `DrSquiggles`, `ZRob`, `SelfPlayingGuitars`, `Krzyzaniak2021`, `Karbasi2023`, `NorwAI`, `DeezerIpsos2024`, `MGTpython`.

- [ ] **Step 1: Copy shared entries from the other book**

```bash
SSM=/home/alexanje/github/sensingsoundandmusic/book/references.bib
for key in Jensenius2022 Newen2018OxfordHandbook4ECognition Clarke2005 Leman2007 Briot2020 Sturm2019AIMusic; do
  grep -n "^@.*{$key," "$SSM" || echo "MISSING $key"
done
```
For each key found, copy the whole entry with `awk "/^@.*{$key,/,/^}/" "$SSM" >> book/references.bib`. Then rename inside the copied text: `Newen2018OxfordHandbook4ECognition` to `Newen2018`, `Sturm2019AIMusic` to `Sturm2019`. Find the Godøy and Leman *Musical Gestures* entry with `grep -n "Musical Gestures" "$SSM"` and copy it as `GodoyLeman2010` (DOI 10.4324/9780203863411).

- [ ] **Step 2: Append the new entries**

```bibtex
@article{Vear2021,
  author = {Vear, Craig}, year = {2021},
  title = {Creative {AI} and musicking robots},
  journal = {Frontiers in Robotics and AI}, volume = {8}, pages = {631752},
  doi = {10.3389/frobt.2021.631752}
}
@article{Bretan2016,
  author = {Bretan, Mason and Weinberg, Gil}, year = {2016},
  title = {A survey of robotic musicianship},
  journal = {Communications of the ACM}, volume = {59}, number = {5}, pages = {100--109},
  doi = {10.1145/2818994}
}
@article{Bringsjord2001,
  author = {Bringsjord, Selmer and Bello, Paul and Ferrucci, David}, year = {2001},
  title = {Creativity, the {Turing} test, and the (better) {Lovelace} test},
  journal = {Minds and Machines}, volume = {11}, pages = {3--27},
  doi = {10.1023/A:1011206622741}
}
@article{Liang2023,
  author = {Liang, Weixin and Yuksekgonul, Mert and Mao, Yining and Wu, Eric and Zou, James}, year = {2023},
  title = {{GPT} detectors are biased against non-native {English} writers},
  journal = {Patterns}, volume = {4}, number = {7}, pages = {100779},
  doi = {10.1016/j.patter.2023.100779}
}
@inproceedings{Luccioni2024,
  author = {Luccioni, Sasha and Jernite, Yacine and Strubell, Emma}, year = {2024},
  title = {Power hungry processing: Watts driving the cost of {AI} deployment?},
  booktitle = {Proceedings of the 2024 ACM Conference on Fairness, Accountability, and Transparency},
  doi = {10.1145/3630106.3658542}
}
@inproceedings{Carlini2023,
  author = {Carlini, Nicholas and Hayes, Jamie and Nasr, Milad and Jagielski, Matthew and Sehwag, Vikash and Tram{\`e}r, Florian and Balle, Borja and Ippolito, Daphne and Wallace, Eric}, year = {2023},
  title = {Extracting training data from diffusion models},
  booktitle = {32nd USENIX Security Symposium},
  url = {https://arxiv.org/abs/2301.13188}
}
@inproceedings{Somepalli2023,
  author = {Somepalli, Gowthami and Singla, Vasu and Goldblum, Micah and Geiping, Jonas and Goldstein, Tom}, year = {2023},
  title = {Diffusion art or digital forgery? {Investigating} data replication in diffusion models},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  url = {https://arxiv.org/abs/2212.03860}
}
@article{Slater2009,
  author = {Slater, Mel}, year = {2009},
  title = {Place illusion and plausibility can lead to realistic behaviour in immersive virtual environments},
  journal = {Philosophical Transactions of the Royal Society B}, volume = {364}, pages = {3549--3557},
  doi = {10.1098/rstb.2009.0138}
}
@inproceedings{Kazemitabaar2023,
  author = {Kazemitabaar, Majeed and Chow, Justin and Ma, Carl Ka To and Ericson, Barbara J. and Weintrop, David and Grossman, Tovi}, year = {2023},
  title = {Studying the effect of {AI} code generators on supporting novice learners in introductory programming},
  booktitle = {Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems},
  doi = {10.1145/3544548.3580919}
}
@article{Prather2023,
  author = {Prather, James and Reeves, Brent N. and Denny, Paul and Becker, Brett A. and Leinonen, Juho and Luxton-Reilly, Andrew and Powell, Garrett and Finnie-Ansley, James and Santos, Eddie Antonio}, year = {2023},
  title = {``It's weird that it knows what {I} want'': Usability and interactions with {Copilot} for novice programmers},
  journal = {ACM Transactions on Computer-Human Interaction}, volume = {31}, number = {1},
  doi = {10.1145/3617367}
}
@article{Wei2022,
  author = {Wei, Jason and Tay, Yi and Bommasani, Rishi and Raffel, Colin and Zoph, Barret and Borgeaud, Sebastian and Yogatama, Dani and Bosma, Maarten and Zhou, Denny and Metzler, Donald and Chi, Ed H. and Hashimoto, Tatsunori and Vinyals, Oriol and Liang, Percy and Dean, Jeff and Fedus, William}, year = {2022},
  title = {Emergent abilities of large language models},
  journal = {Transactions on Machine Learning Research},
  url = {https://arxiv.org/abs/2206.07682}
}
@techreport{METR2025,
  author = {{Model Evaluation and Threat Research}}, year = {2025},
  title = {Measuring {AI} ability to complete long tasks},
  url = {https://arxiv.org/abs/2503.14499}
}
@article{Rahmanzadehgervi2024,
  author = {Rahmanzadehgervi, Pooyan and Bolton, Logan and Taesiri, Mohammad Reza and Nguyen, Anh Totti}, year = {2024},
  title = {Vision language models are blind},
  journal = {arXiv preprint},
  url = {https://arxiv.org/abs/2407.06581}
}
@inproceedings{Bruce2024,
  author = {Bruce, Jake and Dennis, Michael and Edwards, Ashley and Parker-Holder, Jack and Shi, Yuge and Hughes, Edward and Lai, Matthew and Mavalankar, Aditi and Steigerwald, Richie and Apps, Chris and Aytar, Yusuf and Bechtle, Sarah and Behbahani, Feryal and Chan, Stephanie and Heess, Nicolas and Gonzalez, Lucy and Osindero, Simon and Ozair, Sherjil and Reed, Scott and Zhang, Jingwei and Zolna, Konrad and Clune, Jeff and de Freitas, Nando and Singh, Satinder and Rockt{\"a}schel, Tim}, year = {2024},
  title = {Genie: Generative interactive environments},
  booktitle = {Proceedings of the 41st International Conference on Machine Learning},
  url = {https://arxiv.org/abs/2402.15391}
}
@article{Caillon2021,
  author = {Caillon, Antoine and Esling, Philippe}, year = {2021},
  title = {{RAVE}: A variational autoencoder for fast and high-quality neural audio synthesis},
  journal = {arXiv preprint},
  url = {https://arxiv.org/abs/2111.05011}
}
@article{ClarkChalmers1998,
  author = {Clark, Andy and Chalmers, David}, year = {1998},
  title = {The extended mind},
  journal = {Analysis}, volume = {58}, number = {1}, pages = {7--19},
  doi = {10.1093/analys/58.1.7}
}
@book{Kolb1984,
  author = {Kolb, David A.}, year = {1984},
  title = {Experiential Learning: Experience as the Source of Learning and Development},
  publisher = {Prentice-Hall},
  url = {https://www.worldcat.org/isbn/0132952610}
}
@misc{Roose2022,
  author = {Roose, Kevin}, year = {2022},
  title = {An {A.I.}-generated picture won an art prize. {Artists} aren't happy},
  howpublished = {The New York Times, 2 September 2022},
  url = {https://www.nytimes.com/2022/09/02/technology/ai-artificial-intelligence-artists.html}
}
@misc{C2PA, author = {{Coalition for Content Provenance and Authenticity}}, title = {{C2PA} technical specification}, url = {https://c2pa.org/specifications/}, year = {2024}}
@misc{AMBIENT, author = {{RITMO}}, title = {Bodily entrainment to audiovisual rhythms ({AMBIENT})}, url = {https://www.uio.no/ritmo/english/projects/ambient/index.html}, year = {2024}}
@misc{DrSquiggles, author = {{RITMO}}, title = {Dr. {Squiggles}: an interactive musical robot}, url = {https://www.uio.no/ritmo/english/projects/dr-squiggles/}, year = {2022}}
@misc{ZRob, author = {{RITMO}}, title = {Interactive robotic system ({ZRob})}, url = {https://www.uio.no/ritmo/english/projects/ZRob/}, year = {2024}}
@misc{SelfPlayingGuitars, author = {{RITMO}}, title = {Self-playing guitars}, url = {https://www.uio.no/ritmo/english/projects/self-playing-guitars/}, year = {2026}}
@misc{NorwAI, author = {{NorwAI}}, title = {{NorwAI}: Norwegian Research Center for {AI} Innovation}, url = {https://www.ntnu.edu/norwai}, year = {2026}}
@misc{MGTpython, author = {{fourMs Lab}}, title = {Musical {Gestures} {Toolbox} for {Python}}, url = {https://github.com/fourMs/MGT-python}, year = {2026}}
```

- [ ] **Step 3: Look up the five entries whose identifiers must be verified**

Run each query and paste the resulting DOI or URL into an entry with the key shown:

```bash
q() { curl -s "https://api.crossref.org/works?rows=3&query.bibliographic=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$1")" | python3 -c "import json,sys;[print(i.get('DOI'),'|',i.get('title',[''])[0],'|',i.get('container-title',[''])[:1]) for i in json.load(sys.stdin)['message']['items']]"; }
q "Inverse and indirect mappings in embodied AI systems in everyday environments Riaz Erdem Jensenius"      # -> Riaz2026 (@article, Frontiers in Computer Science)
q "Dr. Squiggles interactive musical robot Krzyzaniak"                                                      # -> Krzyzaniak2021
q "ZRob robotic drumming Karbasi Jensenius Tørresen"                                                        # -> Karbasi2023
```
For `MusicLab`, run `curl -sI https://www.uio.no/ritmo/english/projects/musiclab/ | head -1`; if it is not 200, search `site:uio.no ritmo MusicLab` and use the page that is. For `DeezerIpsos2024`, search "Deezer Ipsos survey AI-generated music listeners cannot tell 2024" and use the Deezer newsroom URL; entry type `@misc`, author `{Deezer and Ipsos}`, year 2024.

- [ ] **Step 4: Verify every DOI resolves and every key is unique**

```bash
python3 - <<'EOF'
import re, subprocess, collections
txt = open("book/references.bib", encoding="utf-8").read()
keys = re.findall(r"^@\w+\{([^,]+),", txt, re.M)
dups = [k for k, n in collections.Counter(keys).items() if n > 1]
assert not dups, f"duplicate keys: {dups}"
bad = []
for doi in re.findall(r"doi\s*=\s*\{([^}]+)\}", txt):
    code = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-I", "-L", f"https://doi.org/{doi}"], capture_output=True, text=True).stdout
    if code not in ("200", "302", "303"):
        bad.append((doi, code))
print("bad DOIs:", bad); print("keys:", len(keys))
EOF
```
Expected: `bad DOIs: []`. Fix any that fail by checking the DOI on crossref before continuing.

- [ ] **Step 5: Commit**

```bash
git add book/references.bib
git commit -m "Add references for robotics, embodiment, detection, energy, memorisation, XR, and RITMO projects

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

## Phase 2: extra pages

### Task 6: Templates, tools page, gallery page

**Files:**
- Create: `book/templates/practice-log.md`, `book/templates/gallery-page.md`, `book/tools.md`, `book/gallery.md`
- Modify: `book/myst.yml` (add `tools.md` and `gallery.md` at the end of the TOC, before nothing else yet)

- [ ] **Step 1: Write the practice-log template**

```markdown
# Practice log — week N

**Brief.** One sentence on what you set out to do this week.

**Tools.** Name, model, version or date, for each tool used.

## Explore
Three or four sentences: what you varied, what you compared, what surprised you.

## Reflect
Three or four sentences: what the experiments showed, and the one intention you set before making.

## Create
Three or four sentences: what you made, where you exerted your own will (prompt, edit, refusal, selection), and a link to the artefact.

**Open question.** One sentence you want answered next week.
```

- [ ] **Step 2: Write the gallery-page template**

```markdown
# Project title

**Makers.** Names (or a pseudonym if you prefer).
**Modalities.** At least two, for example text + image.
**Tools.** Name, model, version or date, for each.

## The work
Embed or link the artefact. One paragraph on what a visitor is looking at.

## The brief
Who it is for and what it had to do.

## Surprise and will
One paragraph on where the AI surprised you, one on where you exerted your will.

## Provenance
Prompt log link, human edits, any voices or likenesses used and the consent obtained.

## Consent for the archive
- [ ] Keep this page in the public Synthetic Gallery for future cohorts.
- [ ] Remove it after the course.
```

- [ ] **Step 3: Write `book/tools.md`**

Front matter: `title: Tools`, `description: "The tool categories used in the course, with current examples and open alternatives."`. Body: one paragraph that the point is to learn the categories; a first section **Apps made for this book** listing every app from `book/apps/README.md` as links to `https://fourms.github.io/Creative-AI/apps/<name>/` (start with the ten first-batch names from the spec, marked "in preparation" until built); then the six `<details>` categories from the current `intro.ipynb` "Tools we will use" section (text and dialogue; images; sound and music; video and animation; code and creative coding; 3D, XR, design, and games), each with one **open alternative** line, and the XR category adding a headset viewer entry and a phone AR viewer entry; then a **Hardware to borrow** section (a VR headset, a 360 camera, a phone gimbal, an Arduino kit with sensors, a small robot platform) marked "available through the fourMs Lab, ask the course coordinator"; then the existing "Tool turnover" warning.

- [ ] **Step 4: Write `book/gallery.md`**

Front matter: `title: The Synthetic Gallery`. Body, moved from the current `futures.ipynb` "Final projects" section and `intro.ipynb` "The final project" section: what it is (public showcase in the exam period, physical room plus static online gallery), what a project can look like (the eleven examples), technical requirements (two modalities, logged prompts, acknowledged tools), what you deliver (work, 1 500–2 500 word reflection with the listed contents, 5-minute presentation plus 5-minute Q&A, gallery page from `templates/gallery-page.md`, prompt log), what good looks like (the three example projects), the two process-memo questions, and an **Archive** heading with the sentence "Pages from past cohorts appear below with their makers' consent." and no entries yet.

- [ ] **Step 5: Add both pages to the TOC and build**

Append to `project.toc` in `book/myst.yml`:
```yaml
    - file: tools.md
    - file: gallery.md
```
Run: `cd book && myst build --html 2>&1 | tail -5; cd ..`
Expected: build completes; warnings are acceptable, errors are not.

- [ ] **Step 6: Commit**

```bash
git add book/templates book/tools.md book/gallery.md book/myst.yml
git commit -m "Add tools page, Synthetic Gallery page, and student templates

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 7: Course overview page

**Files:**
- Modify: `book/intro.ipynb` (rewrite via Markdown and `md2nb.py`)

- [ ] **Step 1: Write the overview as Markdown in the scratchpad**

Write `/tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/intro.md` with this structure, keeping the current front matter and cover image:

1. `## Introduction` — three paragraphs: what the course is (bachelor, all faculties, no prerequisites), the twofold aim, the three concepts. Then the `:::{important} Learning outcomes` block copied from the current page.
2. `## Five layers` — the layer table from the spec section 3 and one paragraph saying each chapter names its layer, in parallel with the levels of description in *Sensing Sound and Music* (link `https://fourms.github.io/sensingsoundandmusic/`).
3. `## Course schedule` — the table from the spec section 4 with chapter links `[What is Creative AI?](introduction.ipynb)` etc., the exam-period row for the gallery, and a paragraph introducing the five extra pages with links to `tips-and-tricks.ipynb`, `glossary.md`, `tools.md`, `gallery.md`.
4. `## Explore, Reflect, Create` — the ERC lab structure from spec section 5, with this diagram and the four-step list with timings, the mapping onto surprise and will, and the log tip:
   ```
   ```{mermaid}
   flowchart LR
       E[Explore<br/><i>try: where the model surprises you</i>] --> R[Reflect<br/><i>decide: what it showed, what you intend</i>]
       R --> C[Create<br/><i>make: where you exert your will</i>]
       C --> L[Log<br/><i>at home: three paragraphs</i>]
       L --> E
   ```
   ```
   Keep the three track descriptions (humanities and social sciences; applied and behavioural; making) from the current page, retitled in ERC order.
5. `## Pedagogical strategy` — subsections: A course for everyone at UiO; Active learning and a flipped classroom; Studio labs and process over polish; Research-based and research-led (RITMO, the fourMs Lab, and the MishMash Centre for AI and Creativity with links `https://www.uio.no/ritmo/english/`, `https://www.uio.no/ritmo/english/research/labs/fourms/`, `https://mishmash.no/`; one paragraph that every chapter carries a Research spotlight and that students may join ongoing studies); Reading claims about AI (the claim, evidence, method, limits checklist applied to model cards, benchmarks, and announcements, with a `:::{tip}` on benchmark numbers without error bars); Guest lecturers; Open education (the current text); A note on AI tools used to write this book.
6. `## Assessment` — the current table with milestones updated: A1 due week 2, A2 due week 5, ethics essay due week 7, A3 due week 8, proposal due week 10, final project due end of week 12, Synthetic Gallery in the exam period; the weekly log described as three paragraphs Explore, Reflect, Create linking `templates/practice-log.md`; the process memo; a one-paragraph pointer to `gallery.md`; the academic-integrity tip.
7. `## Reading list` — the current core curriculum and supplementary lists unchanged, with the chapter numbers in the "Where it is going" and "Norway and the EU" items updated (Salma paper now chapter 3, NB AI Lab now chapter 4 and 6).
8. `## How to read this book` — the twelve-step template list from spec section 6 in prose, and the sentence "Let's begin."
9. `## Learn more` — a `::::{grid} 1 1 2 2` with three cards: MUS2640 Sensing Sound and Music (`https://www.uio.no/studier/emner/hf/imv/MUS2640/`), MUS2850 Computer Music (`https://www.uio.no/studier/emner/hf/imv/MUS2850/`), IN3050 Introduction to Artificial Intelligence and Machine Learning (`https://www.uio.no/studier/emner/matnat/ifi/IN3050/`).

Drop from the current page: the tools lists (now `tools.md`), the gallery details (now `gallery.md`).

- [ ] **Step 2: Convert and build**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/intro.md book/intro.ipynb
python scripts/check-chapters.py | grep "intro.ipynb"; echo "grep exit $?"
cd book && myst build --html 2>&1 | grep -iE "error|intro" | head; cd ..
```
Expected: no `intro.ipynb` lines from the checker (grep exit 1); no build errors.

- [ ] **Step 3: Commit**

```bash
git add book/intro.ipynb
git commit -m "Rewrite course overview: five layers, ERC labs, new schedule, research-led framing

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 8: Tips and tricks page

**Files:**
- Create: `book/tips-and-tricks.ipynb`
- Modify: `book/myst.yml` (insert `- file: tips-and-tricks.ipynb` before `tools.md`)

- [ ] **Step 1: Write the page as Markdown in the scratchpad**

Front matter: `title: "Tips and tricks"`, `subtitle: "Prompting, logging, writing about AI-made work, and preparing your portfolio"`. One intro paragraph modelled on the *Sensing Sound and Music* page: a companion, dip in when needed. Sections, each three to six paragraphs:

1. `## Prompt craft that transfers` — the ROLE / TASK / CONSTRAINTS / CONTEXT / OUTPUT template; be specific, show not tell, constrain the form, iterate on what is wrong, generate three and veto; image and video prompt orders (subject, composition, style, medium, lighting, mood; plus camera and motion for video); the change-one-knob rule.
2. `## Keeping a decisions and prompt log` — what to record (brief, tool, model, version or date, exact prompt, seed, settings, what you got, what you expected, the gap, human edits), one file per project, why it protects you and is honest; link `templates/practice-log.md`.
3. `## Writing about AI-made work` — describe before you interpret; give addresses ("the third variation at guidance 9", "at 0:42"); name the tool, model, version, date, and seed; separate what the model did from what you did; keep terminology fixed (model, tool, prompt, sample, generation).
4. `## Citing models, datasets, and generated material` — cite a model by its card (author or organisation, year, name, version, URL); cite a dataset by its card or paper; for generated material state tool, version, date, and that it was generated, in the caption; use a reference manager (Zotero) and one style consistently; when in doubt follow the UiO library guidance (`https://www.ub.uio.no/english/`).
5. `## Figures and captions for generated images` — every figure has a caption that says what it is and what to notice, states that it is generated and by what, and credits reference images; screenshots of tools need the tool name and date.
6. `## Privacy, accounts, and UiO` — the AI at UiO page (`https://www.uio.no/english/services/ai/`) and its approved services; never paste personal data, unpublished research, or other people's work into a commercial tool without a licence; prefer the UiO service or a local model for sensitive material; consent before cloning any voice or face.
7. `## Running models locally` — why (privacy, reproducibility, cost, learning); what a laptop can run in 2026 (small open-weight language models, distilled image models at low resolution, speech recognition); pointers to the tools page; a `:::{note} Dig deeper: a first local model` with the two commands to install a local runner and pull a small model, written generically ("your runner's pull command").
8. `## Preparing the portfolio and the gallery` — the ladder of deliverables; a five-minute presentation structure (brief, one artefact, one surprise, one act of will, one open question); rehearse with the projector; check every link; the gallery-page template.
9. `## Study technique for a flipped course` — read the chapter before the lecture and bring one question; 30-minute blocks; explain a concept aloud; turn headings into questions; use an AI assistant to quiz you on the chapter and then check its answers against the text.

- [ ] **Step 2: Convert, add to TOC, check, build**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/tips-and-tricks.md book/tips-and-tricks.ipynb
sed -i 's#^    - file: tools.md#    - file: tips-and-tricks.ipynb\n    - file: tools.md#' book/myst.yml
python scripts/check-chapters.py | grep "tips-and-tricks"; echo "grep exit $?"
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
```
Expected: no checker lines for the page; no build errors.

- [ ] **Step 3: Commit**

```bash
git add book/tips-and-tricks.ipynb book/myst.yml
git commit -m "Add tips and tricks page

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 9: Glossary skeleton

**Files:**
- Create: `book/glossary.md`
- Modify: `book/myst.yml` (append `- file: glossary.md` as the last TOC entry)

- [ ] **Step 1: Write the skeleton**

```markdown
# Glossary

This page collects the technical vocabulary of the book in one place, as a lookup list for revision and for writing your reflections. Every term is explained in context in the chapters, so treat these short definitions as reminders rather than as first introductions.

```{glossary}
Agent
: A system given a goal that chooses its own steps, calling tools in a loop of plan, act, and observe until a stopping condition is met.

Conditioning
: Any input besides noise that steers what a generative model produces, such as a text prompt, a reference image, a mask, or a control signal.

Diffusion model
: A generative model trained to remove noise step by step, so that it can turn pure noise into a coherent image, sound, or video.

Foundation model
: A very large model trained once on broad data and then adapted to many tasks by prompting or fine-tuning.

Hallucination
: A fluent, confident output that is false, a direct consequence of training a model to produce plausible rather than true text.

Inference
: Using a trained model to produce an output from an input; the parameters do not change.

Large language model (LLM)
: A transformer trained to predict the next token in text, on which chat, coding, and reasoning behaviours are built.

Prompt
: The text (and sometimes images or audio) given to a model to condition its output; the main interface of current generative tools.

Token
: The unit a language model reads and writes, usually a word piece; Norwegian text uses more tokens than the same text in English.

Training
: Repeatedly adjusting a model's parameters to reduce a loss measured on batches of data.
```
```

The glossary is filled in Task 32 from the terms set in bold at first definition in the chapters; this skeleton makes the page exist so cross-references resolve.

- [ ] **Step 2: Add to the TOC, build, commit**

```bash
printf '    - file: glossary.md\n' >> book/myst.yml
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
git add book/glossary.md book/myst.yml
git commit -m "Add glossary skeleton

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

## Phase 3: chapters

Every chapter task uses the same five-step cycle. The steps are written out in each task. The chapter Markdown is written in the scratchpad at `/tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/<stem>.md`, then converted into `book/<stem>.ipynb`. When the source is an existing notebook, read it with the Read tool first and reuse its prose wherever the outline keeps a topic; rewrite only what the outline changes. Every chapter has: front matter `title: "N. Title"`, `subtitle`, `description`; an opening paragraph that names the layer(s) and links back to `[the five layers](intro.ipynb#five-layers)`; the elements of the template in order; five questions; every further-reading item with a DOI or URL; the "Explore interactively" tip listing the chapter's apps as `https://fourms.github.io/Creative-AI/apps/<name>/` links, marked "(in preparation)" until the app task lands.

### Task 10: Chapter 1, What is Creative AI?

**Files:**
- Modify: `book/introduction.ipynb` (rewrite)

- [ ] **Step 1: Read the current chapter and write the new Markdown**

Keep the current front matter with title `"1. What is Creative AI?"`. Opening paragraph: this chapter works at the **culture** layer and sets up the whole spine. Sections:

- `## Three slippery words` with `### Creativity`, `### Artificial intelligence`, `### Creative AI` — keep as is, including the Boden distinctions and the working definition.
- `## A short, opinionated history` with `### The art-historical strand`, `### The technical strand` — keep; extend the technical strand with two 2024–2026 bullets: "2024–2025 — reasoning models and agents" and "2025–2026 — world models and embodied AI", each one sentence.
- `## Three concepts that thread through the course` — keep.
- `## Five layers` — a short section introducing data, model, interface, practice, culture with one sentence each and the note that every chapter names its layer; link to the overview.
- `## What is not Creative AI` — keep the first two bullets; replace the "AGI/ASI predictions" bullet with "Forecasting. We look at scenarios in chapter 3 as a way to ask questions, not as predictions."; keep the "we take seriously" list.
- `:::{admonition} Research spotlight` `:class: spotlight` — MishMash Centre for AI and Creativity: the national consortium led by UiO with RITMO and the fourMs Lab at its origin, its aim to create, explore, and reflect on AI for, through, and in creative practices, its seven work packages (performances, processes, well-being, education, creative industries, cultural heritage, problem-solving), and one sentence that Explore, Reflect, Create is the same triad; link `https://mishmash.no/`.
- `## This week's lab: Explore, Reflect, Create` — `### Explore (about 30 min)`: pick one text tool and one image tool from the tools page; same brief, two media; vary one thing; save both. `### Reflect (about 15 min)`: in pairs, compare your one-sentence definition from the start of the chapter with the working definition, and say one thing you now intend to make. `### Create (about 45 min)`: assemble one flyer or diptych; write the first log entry using `templates/practice-log.md`; the last 15 minutes present each other's artefacts to a third student. Keep the "Save your prompts" tip.
- `## A critical look: did an AI win the Colorado State Fair?` — claim (a generated image won a 2022 digital-art prize and "AI beat human artists"); evidence (the entry was made with a text-to-image tool plus many hours of prompting, selection, and editing; the category was digital arts; the judges said they would have awarded it anyway) [@Roose2022]; method (a juried competition with a small category and no blind test of AI versus human); limits (one event tells you about that jury and that category, not about art; the interesting question it raises is who the author was, which chapter 3 takes up).
- Chapter summary; five questions (definition of creativity; Boden's three kinds; why the art-historical strand matters; the three concepts; which layer a given claim belongs to); Further reading (keep the current list; every item already has a key); Explore interactively: none, so link the tools page and the two apps of chapter 2 as a preview.

- [ ] **Step 2: Convert**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/introduction.md book/introduction.ipynb
```

- [ ] **Step 3: Check and build**

```bash
python scripts/check-chapters.py | grep "introduction.ipynb"; echo "grep exit $?"
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
```
Expected: grep exit 1 (no problems for this file); no build errors.

- [ ] **Step 4: Commit**

```bash
git add book/introduction.ipynb
git commit -m "Rewrite chapter 1 to the new template with MishMash spotlight and critical look

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 11: Chapter 2, How generative AI works

**Files:**
- Rename: `book/foundations.ipynb` to `book/how-it-works.ipynb`, then rewrite
- Read for content: `book/generative-ai.ipynb` (do not delete yet; Task 12 deletes it)
- Modify: `book/myst.yml` (replace the `foundations.ipynb` and `generative-ai.ipynb` entries with one `how-it-works.ipynb` entry)

- [ ] **Step 1: Rename and write the merged Markdown**

`git mv book/foundations.ipynb book/how-it-works.ipynb`. Front matter title `"2. How generative AI works"`, subtitle `"Data, models, training, sampling, and conditioning"`. Opening paragraph: **data** and **model** layers. Sections:

- `## A toy starting point: learning from examples` with the `figures/how-it-works/ml-pipeline.svg` figure — from foundations.
- `## The cast of characters` with `### Data`, `### Models`, `### Training`, `### Inference`, `### Generalisation`, `### Bias` — from foundations; the bias paragraph forward-links to chapter 3.
- `## A very short tour of neural networks` — from foundations, plus `:::{note} Dig deeper: what a layer computes` holding a five-line description of a matrix multiply and a non-linearity.
- `## From classifying to generating` — from generative-ai, with the "learn a distribution, then sample" important box.
- `## Probability without tears` with `### Distributions`, `### Sampling` — from generative-ai.
- `## Conditioning: telling the model what you want` with the `figures/how-it-works/conditioning.svg` figure — from generative-ai.
- `## Prompts as the new interface` — from generative-ai, shortened to one paragraph plus the five principles; the craft moves to the tips page.
- `## A taxonomy of generative models` — from generative-ai.
- `## Foundation models and fine-tuning` — from foundations.
- `## What generative models cannot do` — from generative-ai.
- `:::{note} Dig deeper: a 12-line training loop` containing the numpy loop from foundations as an executed cell: wrap it as ```` ```{code-cell} python ```` and add, after the loop, a matplotlib scatter of `x, y` with the fitted line and `plt.xlabel("x"); plt.ylabel("y"); plt.title("A two-parameter model fitted by gradient descent")`. This cell must run in under a second with numpy and matplotlib only.
- `:::{note} Dig deeper: sampling from a tiny language model` holding the GPT-2 temperature listing from generative-ai as a plain fenced listing, not executed.
- Research spotlight: AMBIENT (Bodily Entrainment to Audiovisual Rhythms) as an example of the data a model would need to learn how bodies respond to rhythm: multi-person motion capture, physiology, and audio recorded together in the fourMs Lab; a sentence on why such data is scarce and consented; link and cite [@AMBIENT].
- `:::{note} If you took MUS2640` — artificial neural networks are introduced in *The brain* and model families in *Machine listening* (`https://fourms.github.io/sensingsoundandmusic/the-brain/`, `https://fourms.github.io/sensingsoundandmusic/machine-listening/`); this chapter goes from there to generation.
- Lab: Explore (about 30 min): inspect one model card on Hugging Face (dataset, parameters, licence, limitations) and run one prompt through three sampler settings in an image tool; Reflect (about 15 min): pairs discuss distribution versus boundary and what the three samples show, each states one intention; Create (about 45 min): the captioned triptych with a 150-word artist's statement; the training-loop and sampler apps as optional Explore.
- `## A critical look: is a language model just autocomplete?` — claim; evidence (next-token training objective is autocomplete; in-context learning [@Brown2020GPT3] and reported emergent abilities [@Wei2022]); method (benchmarks with sharp metrics can make smooth improvement look like sudden jumps); limits (both "just autocomplete" and "understands" over-claim; the useful question is what the model can do reliably on your task).
- Summary; questions (training versus inference; why bias is a data property; distribution versus boundary; what a sampler knob does; one thing a generative model cannot do and why); Further reading (Mitchell2019, Goodfellow2016, Blue1Brown, HuggingFaceCourse, Weng2021Diffusion, Karpathy2015RNN); Explore interactively: `training-loop`, `next-token-sampler`, `diffusion-explorer` (all in preparation).

- [ ] **Step 2: Convert and update the TOC**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/how-it-works.md book/how-it-works.ipynb
sed -i 's#    - file: foundations.ipynb#    - file: how-it-works.ipynb#; /    - file: generative-ai.ipynb/d' book/myst.yml
```

- [ ] **Step 3: Check and build with execution**

```bash
python scripts/check-chapters.py | grep "how-it-works"; echo "grep exit $?"
cd book && myst build --html --execute 2>&1 | grep -iE "error|how-it-works" | head; cd ..
```
Expected: no checker lines; the executed cell produces a figure and no errors.

- [ ] **Step 4: Commit**

```bash
git add -A book/how-it-works.ipynb book/foundations.ipynb book/myst.yml
git commit -m "Merge foundations and generative AI into chapter 2, How generative AI works

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 12: Chapter 3, Co-creation, authorship, and ethics

**Files:**
- Rename: `book/ethics.ipynb` to `book/co-creation-and-ethics.ipynb`, then rewrite
- Read for content: `book/generative-ai.ipynb` (five paradoxes), `book/futures.ipynb` (three futures)
- Delete: `book/generative-ai.ipynb`
- Modify: `book/myst.yml` (move the entry to position 3, after `how-it-works.ipynb`)

- [ ] **Step 1: Rename and write the Markdown**

`git mv book/ethics.ipynb book/co-creation-and-ethics.ipynb`. Title `"3. Co-creation, authorship, and ethics"`, subtitle `"Working with a collaborator that was trained on everyone"`. Opening: **culture** layer, placed early so every later chapter can use its vocabulary. Sections:

- `## Executors and collaborators` — the Salma framing and the five-paradox table with the practical walk-through, from generative-ai; the "from craftsperson to creative director" important box.
- `## A simple frame: harm, benefit, and to whom` — the four questions, from ethics.
- `## Topic 1 — Copyright, consent, and training data` through `## Topic 5 — Authorship, authenticity, and the public sphere` — from ethics, each with its "What you can do" list; in Topic 4 add one paragraph with the inference-energy figures from [@Luccioni2024] (image generation costs far more than text classification per query; multimodal and reasoning modes multiply it) and the reminder that the same paper shows wide ranges.
- `## Death of the Artist or Birth of the Curator?` — from ethics.
- `## Three futures, as a foresight exercise` — the three scenarios from futures, reframed as a way to ask "what does your discipline look like in each", and a sentence that the closing chapter returns to what stays human.
- `## A small personal toolkit` — from ethics.
- Research spotlight: MishMash's work on human agency in co-creative systems and on gender equity in technology-mediated creative fields; one sentence each; link `https://mishmash.no/`.
- Lab: Explore (about 30 min): audit one tool with the four questions (provenance, bias probe of ten prompts, labour, sustainability, labelling), 600–1 000 words started in class; Reflect (about 15 min): the structured debate with drawn positions, two teams, then each student states the essay prompt they will take; Create (about 45 min): the one-page AI policy for an imagined organisation, committed as `ai-policy.md`. The ethics essay block from the current chapter, with the five prompts, moved here and marked **due week 7**.
- `## A critical look: does one image cost a bottle of water?` — claim (viral estimates of water per query); evidence (measured energy per generation from [@Luccioni2024]; water depends on the data centre's cooling and grid, which companies rarely publish; Strubell's training estimates [@Strubell2019Energy]); method (extrapolation from a few benchmarks and assumed cooling ratios); limits (order-of-magnitude claims are defensible, exact bottles are not; the estimator app makes the assumptions visible).
- Summary; questions (name the five paradoxes; the four questions; opt-in versus opt-out; what "creative director" changes about authorship; which future your discipline is already in); Further reading (keep the current list plus Salma2025 and Luccioni2024); Explore interactively: `energy-estimator`, `provenance-inspector`.

- [ ] **Step 2: Convert, delete the merged source, fix the TOC**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/co-creation-and-ethics.md book/co-creation-and-ethics.ipynb
git rm -q book/generative-ai.ipynb
sed -i '/    - file: ethics.ipynb/d' book/myst.yml
sed -i 's#    - file: how-it-works.ipynb#    - file: how-it-works.ipynb\n    - file: co-creation-and-ethics.ipynb#' book/myst.yml
```

- [ ] **Step 3: Check and build**

```bash
python scripts/check-chapters.py | grep "co-creation"; echo "grep exit $?"
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
```

- [ ] **Step 4: Commit**

```bash
git add -A book/co-creation-and-ethics.ipynb book/ethics.ipynb book/generative-ai.ipynb book/myst.yml
git commit -m "Move ethics to chapter 3 as Co-creation, authorship, and ethics; absorb paradoxes and futures

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 13: Chapter 4, Language

**Files:**
- Rename: `book/ai-language.ipynb` to `book/language.ipynb`, then rewrite
- Modify: `book/myst.yml`

- [ ] **Step 1: Rename and write the Markdown**

`git mv book/ai-language.ipynb book/language.ipynb`. Title `"4. Language"`, subtitle `"Writing, dialogue, and large language models"`. Opening: **interface** layer. Sections: keep `## What is a language model?` (`### Tokens, not words`, `### Context, not memory`), `## In-context learning, or "prompting"` (with the template), `## The failure modes you need to recognise` (all six), `## Open vs closed models`, `## How to write with an LLM`. Add `## Norwegian and other small languages`: tokenisation cost, weaker output, the NB AI Lab and NorwAI efforts [@NBAILab; @NorwAI], and why open weights matter for a language of five million speakers. Move the API listing into `:::{note} Dig deeper: calling a model from a notebook` as a non-executed listing. Research spotlight: the NB AI Lab's Norwegian models and NB-Whisper [@NBWhisper; @NBAILab] as the national context for "open". Lab: Explore (about 30 min): hallucination hunt and two-model comparison; Reflect (about 15 min): pairs share where the model helped and hindered, each states the three tasks their prompt library will cover; Create (about 45 min): the prompt library `prompt-library.md`. Critical look: `## A critical look: do AI-text detectors work?` — claim (detectors can tell AI text from human text); evidence (high false-positive rates for non-native writers [@Liang2023], easy evasion by paraphrase, vendors' own withdrawals); method (evaluation on the detector's own test sets); limits (detectors are not evidence; declaration and process logs are the honest alternative, which is this course's policy). Summary; questions (next-token prediction; context window; three prompt patterns; name three failure modes and a mitigation; when to prefer an open model); Further reading (current list plus Liang2023); Explore interactively: `tokeniser-explorer`, `word-vectors`.

- [ ] **Step 2: Convert and update the TOC**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/language.md book/language.ipynb
sed -i 's#    - file: ai-language.ipynb#    - file: language.ipynb#' book/myst.yml
```

- [ ] **Step 3: Check and build**

```bash
python scripts/check-chapters.py | grep "language.ipynb"; echo "grep exit $?"
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
```

- [ ] **Step 4: Commit**

```bash
git add -A book/language.ipynb book/ai-language.ipynb book/myst.yml
git commit -m "Rewrite chapter 4, Language, with Norwegian context and detector critical look

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 14: Chapter 5, Images

**Files:**
- Rename: `book/ai-images.ipynb` to `book/images.ipynb`, then rewrite
- Modify: `book/myst.yml`

- [ ] **Step 1: Rename and write the Markdown**

`git mv book/ai-images.ipynb book/images.ipynb`. Title `"5. Images"`, subtitle `"Diffusion models and the new picture-making"`. Opening: **model** and **interface** layers. Keep all current sections (`## How diffusion works (in pictures)` with `figures/images/diffusion.svg`, `## The vocabulary of text-to-image`, `## Prompting for images` with its subsections, `## Editing instead of generating`, `## Where image models still struggle`). Add `## Consistency across a series`: character references, seed locking, LoRA fine-tunes in one paragraph each. Move the diffusers listing into `:::{note} Dig deeper: generating locally` (not executed). Research spotlight: motiongrams and video visualisation from the Musical Gestures Toolbox [@MGTpython] as pictures computed from motion data rather than generated, and what it means for a picture to be true to a recording; link `https://github.com/fourMs/MGT-python`. Lab: Explore (about 30 min): the four one-variable grids and image-to-image at three strengths; Reflect (about 15 min): pairs compare a generated "typical Norwegian street" with a photograph and say what was averaged away, each states the series they will make; Create (about 45 min): the four-image series, poster, or diptych with the 100-word honest caption. Critical look: `## A critical look: does an image model copy its training images?` — claim (models are collage machines); evidence (extraction of near-duplicates from diffusion models for a small fraction of heavily duplicated training images [@Carlini2023; @Somepalli2023]); method (targeted prompts and nearest-neighbour search against the training set); limits (memorisation is real but rare and concentrated on duplicated images; "copy" is the wrong word for most outputs, and the legal cases [@AndersenStability; @GettyStability] turn on training, not output). Summary; questions (forward and reverse diffusion; what latent diffusion changes; the change-one-knob rule; three control signals; why series drift); Further reading (current list plus Carlini2023); Explore interactively: `diffusion-explorer`, `grid-viewer` (second batch).

- [ ] **Step 2: Convert and update the TOC**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/images.md book/images.ipynb
sed -i 's#    - file: ai-images.ipynb#    - file: images.ipynb#' book/myst.yml
```

- [ ] **Step 3: Check and build**

```bash
python scripts/check-chapters.py | grep "images.ipynb"; echo "grep exit $?"
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
```

- [ ] **Step 4: Commit**

```bash
git add -A book/images.ipynb book/ai-images.ipynb book/myst.yml
git commit -m "Rewrite chapter 5, Images, with series consistency and memorisation critical look

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 15: Chapter 6, Sound and music

**Files:**
- Rename: `book/ai-sound.ipynb` to `book/sound.ipynb`, then rewrite
- Modify: `book/myst.yml`

- [ ] **Step 1: Rename and write the Markdown**

`git mv book/ai-sound.ipynb book/sound.ipynb`. Title `"6. Sound and music"`, subtitle `"Speech, music, and sound design with generative audio models"`. Opening: **practice** layer, and the sentence that this chapter begins where machine listening ends: at the turn from analysing sound to producing it. Keep `## Three quick families of audio AI`, `## How models represent sound` (with `figures/sound/spectrogram.svg`), `## Text-to-speech and voice cloning` (with `### A note on consent`), `## Music generation`, `## Sound design and Foley`, `## Where sound AI fits in a real workflow`. Add `## From analysis to generation`: one section explaining that generation reuses the representations of analysis (spectrograms, codecs, features) and that RAVE [@Caillon2021] is the open research model that makes timbre transfer playable in real time; and `## Playing with a model, not just prompting it`: latency, real-time models, and instruments built on them, one paragraph each. Move the whisper and audiocraft commands into `:::{note} Dig deeper: transcription and generation on your laptop`. Research spotlight: RITMO's MusicLab concerts as sites where generated and live sound meet bodies in a room [@MusicLab], and the self-playing guitars [@SelfPlayingGuitars] as instruments whose sound is generated but radiated acoustically. `:::{note} If you took MUS2640`: spectrograms, machine listening, MIR, and the generative-music section live in *Machine listening* (`https://fourms.github.io/sensingsoundandmusic/machine-listening/`); the live spectrogram app there is the one to use here. Lab: Explore (about 30 min): record a clip with permission, transcribe it, generate a new voice reading it, compare; Reflect (about 15 min): pairs listen to a 30-second generated clip and say what gives it away and what does not, each states the brief for the piece; Create (about 45 min): the 30-second piece with generated music plus a generated ambience bed, mixed, with a consent and provenance note. Critical look: `## A critical look: can listeners tell AI music from human music?` — claim (nobody can tell any more); evidence (a 2024 industry survey [@DeezerIpsos2024] in which most listeners could not identify generated tracks; smaller controlled studies find musicians do better, especially with longer excerpts); method (forced-choice on short excerpts, usually pop, often lossy); limits (short pop excerpts are the easy case; long-range form and rule-breaking are where generation is weak, as *Machine listening* also notes [@Briot2020; @Sturm2019]). Summary; questions (three families; why codecs; what consent means for a voice; what music generation struggles with; where AI sits in a real workflow); Further reading (current list plus Caillon2021, Briot2020, Sturm2019); Explore interactively: `markov-melody`, and the *Sensing Sound and Music* live spectrogram (`https://fourms.github.io/sensingsoundandmusic/apps/live-spectrogram/`).

- [ ] **Step 2: Convert and update the TOC**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/sound.md book/sound.ipynb
sed -i 's#    - file: ai-sound.ipynb#    - file: sound.ipynb#' book/myst.yml
```

- [ ] **Step 3: Check and build**

```bash
python scripts/check-chapters.py | grep "sound.ipynb"; echo "grep exit $?"
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
```

- [ ] **Step 4: Commit**

```bash
git add -A book/sound.ipynb book/ai-sound.ipynb book/myst.yml
git commit -m "Rewrite chapter 6, Sound and music, starting at the analysis-to-generation turn

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 16: Chapter 7, Video

**Files:**
- Rename: `book/ai-video.ipynb` to `book/video.ipynb`, then rewrite
- Modify: `book/myst.yml`

- [ ] **Step 1: Rename and write the Markdown**

`git mv book/ai-video.ipynb book/video.ipynb`. Title `"7. Video"`, subtitle `"Text-to-video, image-to-video, and the time problem"`. Opening: **model** layer. Keep `## Why video is hard` (with `figures/video/video.svg`), `## What current video models can do`, `## The vocabulary of video prompting`, `## Workflow: where video AI actually fits`, `## Lip-sync and avatars`, `## A short word on cost and access`. Add `## World models`: video generation and interactive simulation are converging; a model that predicts the next frame given an action is a playable world [@Bruce2024]; two sentences on what this means for games and for chapter 8. Research spotlight: video analysis of musicians in the fourMs Lab with the Musical Gestures Toolbox [@MGTpython], as the mirror image of generation: extracting motion from video rather than fabricating it, and why a videogram is evidence while a generated clip is not. Lab: Explore (about 30 min): image-to-video with three variations and an end frame; Reflect (about 15 min): pair critique of the variations with the three-question form (what the AI did well, what gives it away, the next step), each states their three-shot idea; Create (about 45 min): three shots, ambient soundtrack from chapter 6, edited, with the provenance card. Critical look: `## A critical look: will AI video replace film crews?` — claim; evidence (what has shipped by 2026: ad inserts, B-roll, music videos, no sustained narrative feature; the Sora system card's own limits [@OpenAISora]); method (demo reels versus production use); limits (the transformed parts are storyboarding and animation; pacing, sound, and colour remain human, and the labour question from chapter 3 applies). Summary; questions (three reasons video is hard; three model strategies; a camera move and a motion in a prompt; why plan the last frame; what a world model is); Further reading (current list plus Bruce2024); Explore interactively: `frame-consistency` (second batch).

- [ ] **Step 2: Convert and update the TOC**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/video.md book/video.ipynb
sed -i 's#    - file: ai-video.ipynb#    - file: video.ipynb#' book/myst.yml
```

- [ ] **Step 3: Check and build**

```bash
python scripts/check-chapters.py | grep "video.ipynb"; echo "grep exit $?"
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
```

- [ ] **Step 4: Commit**

```bash
git add -A book/video.ipynb book/ai-video.ipynb book/myst.yml
git commit -m "Rewrite chapter 7, Video, with world models and a critical look at production claims

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 17: Chapter 8, 3D, XR, and games

**Files:**
- Rename: `book/ai-3d-games.ipynb` to `book/spatial.ipynb`, then rewrite
- Modify: `book/myst.yml`

- [ ] **Step 1: Rename and write the Markdown**

`git mv book/ai-3d-games.ipynb book/spatial.ipynb`. Title `"8. 3D, XR, and games"`, subtitle `"Generative AI in spatial and interactive media"`. Opening: **practice** layer. Keep `## Three kinds of "3D AI"` (capture, generation, textures), `## AI in design (2D and UX)`, `## AI in game development`, `## Where 3D AI still struggles`. Add `## Virtual, augmented, and extended reality`: definitions of VR, AR, MR, and XR in one paragraph; **presence** and **embodiment** as the two things a headset changes [@Slater2009]; scale and the body as interface; where generated assets, generated environments, and generated characters enter an XR pipeline; phone AR as the accessible entry; a `:::{note} Dig deeper: an XR pipeline in 2026` listing the steps from capture or generation to a headset scene with WebXR. Research spotlight: RITMO's Bodies in Concert and the fourMs Lab infrastructure for motion capture and VR, where the question is how presence and joint action change when the concert is virtual; link `https://www.uio.no/ritmo/english/research/labs/fourms/`. Lab: Explore (about 30 min): deliberately break a capture tool with a reflective, a thin, and a moving subject, three screenshots; Reflect (about 15 min): pairs discuss where design judgement sits when variations are free and which parts of 3D work they want to stay human, each states their Create path; Create (about 45 min): Path A Gaussian splat capture, Path B text-to-3D asset placed in a scene, Path C a small XR scene viewed in a headset or on a phone (a WebXR page with one generated asset and one generated ambience), Path D the game-asset pipeline; all committed with captions. Critical look: `## A critical look: does VR make you feel present?` — claim (VR is "the empathy machine"); evidence (place illusion and plausibility illusion are measurable and produce realistic behaviour [@Slater2009]); method (controlled lab studies with questionnaires and physiology); limits (presence is not empathy, effects fade, and generated environments add plausibility failures of their own). Summary; questions (splats versus meshes; what XR adds beyond video; two presence illusions; why topology matters; what changed for a five-person studio); Further reading (current list plus Slater2009); Explore interactively: `splat-viewer` (second batch).

- [ ] **Step 2: Convert and update the TOC**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/spatial.md book/spatial.ipynb
sed -i 's#    - file: ai-3d-games.ipynb#    - file: spatial.ipynb#' book/myst.yml
```

- [ ] **Step 3: Check and build**

```bash
python scripts/check-chapters.py | grep "spatial.ipynb"; echo "grep exit $?"
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
```

- [ ] **Step 4: Commit**

```bash
git add -A book/spatial.ipynb book/ai-3d-games.ipynb book/myst.yml
git commit -m "Rewrite chapter 8 as 3D, XR, and games with a presence critical look

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 18: Chapter 9, Creative coding

**Files:**
- Rename: `book/ai-code.ipynb` to `book/code.ipynb`, then rewrite
- Modify: `book/myst.yml` (the entry moves after `spatial.ipynb`)

- [ ] **Step 1: Rename and write the Markdown**

`git mv book/ai-code.ipynb book/code.ipynb`. Title `"9. Creative coding"`, subtitle `"Pair programming with an assistant, and code as a creative medium"`. Opening: **practice** layer. Keep `## AI coding assistants in 2026`, `## A worked example: p5.js + an assistant`, `## How to talk to a coding assistant`, `## Generative graphics, sound, and interactivity`, `## Building a tiny AI-powered web tool`. Add `## Reading before writing`: a section arguing that supervision is a reading skill, with the explain-back habit. Research spotlight: the Musical Gestures Toolbox for Python [@MGTpython] as an open research codebase students can read, run on their own video, and extend with an assistant; one sentence on how research code differs from tutorial code. Lab: Explore (about 30 min): the same p5.js feature in two assistants, compared; Reflect (about 15 min): explain back the longest generated function to a partner, each states the two features their sketch will have; Create (about 45 min): the mouse-reactive sketch, three iterations, saved publicly; the generative-pipeline option stays as advanced. Critical look: `## A critical look: does AI make beginners better programmers?` — claim; evidence (novices complete more tasks with an assistant but show mixed retention and over-reliance [@Kazemitabaar2023; @Prather2023]); method (classroom experiments with pre and post tests); limits (short studies, one course each; the deskilling question is open, which is why this course grades reading and explaining, not only shipping). Summary; questions (four assistant patterns; why read before write; two prompts that help an assistant; one bug an assistant introduces; what a tiny AI web tool needs); Further reading (current list plus Kazemitabaar2023 and Prather2023); Explore interactively: the p5.js web editor (`https://editor.p5js.org/`).

- [ ] **Step 2: Convert and update the TOC**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/code.md book/code.ipynb
sed -i '/    - file: ai-code.ipynb/d' book/myst.yml
sed -i 's#    - file: spatial.ipynb#    - file: spatial.ipynb\n    - file: code.ipynb#' book/myst.yml
```

- [ ] **Step 3: Check and build**

```bash
python scripts/check-chapters.py | grep "code.ipynb"; echo "grep exit $?"
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
```

- [ ] **Step 4: Commit**

```bash
git add -A book/code.ipynb book/ai-code.ipynb book/myst.yml
git commit -m "Rewrite chapter 9, Creative coding, with reading-first framing

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 19: Chapter 10, Multimodal AI

**Files:**
- Create: `book/multimodal.ipynb` from the multimodal half of `book/multimodal-agents.ipynb`
- Modify: `book/myst.yml` (replace `multimodal-agents.ipynb` with `multimodal.ipynb`; Task 20 adds `agents.ipynb`)

- [ ] **Step 1: Write the Markdown**

Title `"10. Multimodal AI"`, subtitle `"Models that see, hear, and speak"`. Opening: **model** layer. Sections: `## Many media, one model` (the encode, shared transformer, decode recipe with `figures/multimodal/multimodal.svg`, from the current chapter); `## Show, don't tell` (the concrete consequences list and the multimodal prompt); `## Multimodal critique` (using a model to critique your own image, layout, or clip, with the caution that it pattern-matches taste); `## Cross-modal translation as a method` (image to text to sound and back as a creative technique, with a sentence on cross-modal correspondences as studied in music psychology); `## Where multimodal models fail` (grounding failures, counting, reading small text, spatial reasoning [@Rahmanzadehgervi2024]). Research spotlight: multimodal recording at RITMO, where sound, motion, physiology, and video are captured together, and what a model trained on such data could and could not learn; link `https://www.uio.no/ritmo/english/`. `:::{note} If you took MUS2640`: multimodality and cross-modal correspondences are in *Tuning in* and *Vision* (`https://fourms.github.io/sensingsoundandmusic/tuning-in/`, `https://fourms.github.io/sensingsoundandmusic/vision/`). Lab: Explore (about 30 min): three increasingly specific questions about a photograph, then a redesign request; Reflect (about 15 min): pairs discuss where design knowledge ended and pattern-matching began, each picks the project material they will translate; Create (about 45 min): a cross-modal translation of the student's own work in progress (an image described into a sound brief, a sound described into an image, a text turned into a storyboard), documented in the log. Critical look: `## A critical look: does a model "see"?` — claim (vision-language models see like we do); evidence (failures on simple visual tasks such as counting intersections and reading overlapping shapes [@Rahmanzadehgervi2024]); method (small synthetic test sets that humans find trivial); limits (the models are good at description and poor at geometry, which is exactly the split a designer must know). Summary; questions (the three-step recipe; a multimodal prompt; what critique a model can give; one failure class; how translation differs from generation); Further reading (Vaswani2017, Radford2021CLIP, Rahmanzadehgervi2024); Explore interactively: `cross-modal-sketchpad` (second batch).

- [ ] **Step 2: Create the file and update the TOC**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/multimodal.md book/multimodal.ipynb
sed -i 's#    - file: multimodal-agents.ipynb#    - file: multimodal.ipynb#' book/myst.yml
```

- [ ] **Step 3: Check and build**

```bash
python scripts/check-chapters.py | grep "multimodal.ipynb"; echo "grep exit $?"
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
```

- [ ] **Step 4: Commit**

```bash
git add book/multimodal.ipynb book/myst.yml
git commit -m "Add chapter 10, Multimodal AI, split from the multimodal-and-agents chapter

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 20: Chapter 11, Agentic AI

**Files:**
- Rename: `book/multimodal-agents.ipynb` to `book/agents.ipynb`, then rewrite
- Modify: `book/myst.yml` (insert `agents.ipynb` after `multimodal.ipynb`)

- [ ] **Step 1: Rename and write the Markdown**

`git mv book/multimodal-agents.ipynb book/agents.ipynb`. Title `"11. Agentic AI"`, subtitle `"Loops, tools, briefs, and supervision"`. Opening: **interface** layer, the brief as the new interface. Sections from the agent half of the current chapter: `## Agentic AI` (the minimal architecture), `## A creative pipeline as an agent`, `## What agents are not`, `## Where this is going`. Add `## Supervising an agent`: cheap-to-verify tasks, reading traces, permissions, budgets, and the human-in-the-loop checkpoint as a design element; and `## Agents in time`: agents that act in a rhythm rather than in text, as a bridge to chapter 12. Move the Agents SDK sentence into `:::{note} Dig deeper: a three-step agent` as a listing. Research spotlight: the Dr. Squiggles swarm [@DrSquiggles], autonomous robots that listen, track a beat, and improvise together, as agents whose loop runs in musical time; cite [@Krzyzaniak2021]. Lab: Explore (about 30 min): give a coding or research agent one bounded task and read its trace end to end; Reflect (about 15 min): pairs decide which steps of their final project they would delegate and which they would keep, each states the slice they will run; Create (about 45 min): the pipeline diagram with model, input, output, verification, failure, and human checkpoints per step, plus one slice actually run; the agent-loop app as a warm-up. Critical look: `## A critical look: can agents complete real creative tasks?` — claim (agents can now do a producer's job); evidence (measured success falls sharply with task length, with a doubling time in the tasks agents can complete [@METR2025]); method (timed human baselines on software tasks, not creative ones); limits (creative pipelines have soft success criteria; supervision cost is the real budget). Summary; questions (three parts of an agent; why cheap-to-verify; a permission you would never grant; what a good brief contains; what changes when the loop runs in time); Further reading (ClaudeCode, OpenAIOperator, Karpathy2024Software, METR2025, AutoGPT); Explore interactively: `agent-loop`.

- [ ] **Step 2: Convert and update the TOC**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/agents.md book/agents.ipynb
sed -i 's#    - file: multimodal.ipynb#    - file: multimodal.ipynb\n    - file: agents.ipynb#' book/myst.yml
```

- [ ] **Step 3: Check and build**

```bash
python scripts/check-chapters.py | grep "agents.ipynb"; echo "grep exit $?"
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
```

- [ ] **Step 4: Commit**

```bash
git add -A book/agents.ipynb book/multimodal-agents.ipynb book/myst.yml
git commit -m "Add chapter 11, Agentic AI, with supervision and a Dr. Squiggles spotlight

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 21: Chapter 12, AI with a body, and what stays human

**Files:**
- Rename: `book/futures.ipynb` to `book/body.ipynb`, then rewrite
- Modify: `book/myst.yml`

- [ ] **Step 1: Rename and write the Markdown**

`git mv book/futures.ipynb book/body.ipynb`. Title `"12. AI with a body, and what stays human"`, subtitle `"Embodiment, musicking robots, and the limits of the model"`. Opening: **practice** and **culture** layers; the course ends where its research home begins, with bodies. Sections:

- `## Why a body?` — perception and action are one loop; a model with no body has no action-perception loop of its own; the extended-mind argument [@ClarkChalmers1998] and 4E cognition in one paragraph each [@Newen2018].
- `## Movement, motion, action, gesture` — the four terms from *Sound Actions* [@Jensenius2022] in one paragraph, and why a robot's sensors measure motion but must infer action.
- `## Action-sound couplings and mappings` — acoustic couplings versus designed mappings, and the 2026 work on inverse and indirect mappings in embodied AI in everyday environments [@Riaz2026].
- `## Musicking robots` — robotic musicianship [@Bretan2016], Vear's embodied musicking robots and belief systems [@Vear2021], and RITMO's three: ZRob learning to drum through interaction [@ZRob; @Karbasi2023], the Dr. Squiggles swarm [@DrSquiggles], the self-playing guitars [@SelfPlayingGuitars].
- `## Sensors and actuators as interface` — a sensor-to-generator mapping is a prompt made of motion; latency; the audience's body as input.
- `## Robots in performance, care, and everyday life` — where embodied AI is heading beyond music, with one paragraph on care settings and MishMash's well-being work package.
- `## What stays human` — from futures, kept, and extended with one paragraph tying it to embodiment.
- `## Reading the next decade` — from futures, kept.
- `## Closing` — from futures, with the question box about the week-1 definition.
- Research spotlight: the fourMs Lab, its motion capture and robot platforms, and how a student can visit, borrow, or join a study; link `https://www.uio.no/ritmo/english/research/labs/fourms/`.
- `:::{note} If you took MUS2640`: 4E cognition, the motion terminology, motion capture, and the Musical Gestures Toolbox are in *The body*, and the action-perception loop in *Tuning in* (`https://fourms.github.io/sensingsoundandmusic/the-body/`, `https://fourms.github.io/sensingsoundandmusic/tuning-in/`).
- Lab: Explore (about 30 min): the rhythm-bot session, then map a phone or laptop sensor to a generator with the mapper app or a borrowed kit; Reflect (about 15 min): pairs decide which parts of their own final project should stay embodied and why, each states what they will rehearse; Create (about 45 min): a timed project rehearsal with peer feedback using the gallery-page template, and the final log entry with the week-1 definition beside the new one.
- `## A critical look: can a robot musician be creative?` — claim; evidence (the Lovelace objection and the better Lovelace test [@Bringsjord2001]; audiences in musicking-robot studies treat robots as partners when their behaviour is legible [@Vear2021]); method (performance studies and audience interviews rather than benchmarks); limits (creativity here is a relation between players, not a property of the machine, which is the course's answer to its week-1 question).
- Summary; questions (why the action-perception loop matters for AI; motion versus action; coupling versus mapping; one thing each RITMO robot does; what stays human and why); Further reading (Vear2021, Bretan2016, Jensenius2022, GodoyLeman2010, Newen2018, Bridle2022, StanfordAIIndex); Explore interactively: `rhythm-bot`, `sensor-mapper` (second batch).

- [ ] **Step 2: Convert and update the TOC**

```bash
python scripts/md2nb.py /tmp/claude-1000/-home-alexanje-github-Creative-AI/f9b50328-aa72-404f-83d9-9c42ecce8a4e/scratchpad/body.md book/body.ipynb
sed -i 's#    - file: futures.ipynb#    - file: body.ipynb#' book/myst.yml
```

- [ ] **Step 3: Check the whole book and build with execution**

```bash
python scripts/check-chapters.py; echo "exit $?"
cd book && myst build --html --execute 2>&1 | grep -iE "error" | head; cd ..
```
Expected: `OK: all TOC files pass`, exit 0; no build errors. Confirm the TOC order in `book/myst.yml` is exactly: intro, introduction, how-it-works, co-creation-and-ethics, language, images, sound, video, spatial, code, multimodal, agents, body, tips-and-tricks, tools, gallery, glossary.

- [ ] **Step 4: Commit**

```bash
git add -A book/body.ipynb book/futures.ipynb book/myst.yml
git commit -m "Add chapter 12, AI with a body, and what stays human; complete the twelve-week structure

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

## Phase 4: web apps (first batch)

Every app task creates `book/apps/<name>/index.html`, adds a row to `book/apps/README.md`, replaces "(in preparation)" for that app in the chapter's Explore interactively tip and on `tools.md`, and verifies with the same three checks: (a) `python -m http.server 8765 --directory book/apps` and open `http://localhost:8765/<name>/` in a browser, no console errors; (b) the Network panel shows no requests after load except the page itself; (c) the app works with keyboard only. Where a browser is not available to the executor, run `node -e "..."` syntax checks on the extracted script and Read the HTML for the acceptance list; record that manual browser checks remain in the commit message.

Shared skeleton for every app (copy the `<style>` block verbatim from `/home/alexanje/github/sensingsoundandmusic/book/apps/tap-sync/index.html`, lines 1–52, and keep the same `:root` variables, dark-mode media query, `fieldset`, `button`, `.row`, and `canvas` rules):

```html
<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>APP TITLE</title>
  <style>/* copied from tap-sync */</style>
</head>
<body>
  <h1>APP TITLE</h1>
  <p class="intro">ONE PARAGRAPH: what the app shows. Everything runs in your browser; nothing is sent anywhere.</p>
  <!-- controls in <fieldset> blocks, a <canvas> or output area -->
  <script>
    'use strict';
    // app code
  </script>
</body>
</html>
```

### Task 22: Training loop playground

**Files:**
- Create: `book/apps/training-loop/index.html`
- Modify: `book/apps/README.md`, `book/how-it-works.ipynb`, `book/tools.md`

- [ ] **Step 1: Build the app**

Controls: a select for the target function (line `y = 2x + 0.5`, sine, step), a noise slider (0 to 0.5), a learning-rate slider (0.001 to 0.5, log scale), a model select (line with 2 parameters; polynomial of degree 3 with 4 parameters; tiny network with one hidden layer of 8 tanh units), buttons Start, Step, Reset, and a speed slider. Canvas 1 draws the data points and the current model curve; canvas 2 draws loss against step on a log y axis. Algorithm: generate 200 points once per Reset with `Math.random()` seeded by a fixed linear congruential generator so the data is the same across reloads; one step is a full-batch gradient descent step with analytic gradients for the line and polynomial and backpropagation for the network; loss is mean squared error. Display the current parameters and loss with three decimals. Intro paragraph: "Every model in this book is trained by the loop you can watch here: predict, measure the loss, nudge the parameters, repeat."

- [ ] **Step 2: Verify**

Open the page; press Start with the line model; expected: loss falls below 0.02 within 300 steps and the parameters read about 2.0 and 0.5. Set the learning rate to 0.5 with the polynomial model; expected: the loss diverges, which the page reports with the text "Loss is growing: the learning rate is too high." No console errors, no network requests.

- [ ] **Step 3: Wire it in and commit**

Add the README row `| training-loop | 2 | none |`; in `book/how-it-works.ipynb` and `book/tools.md` replace `training-loop/ (in preparation)` wording with the live link. Use `python scripts/md2nb.py` only if you re-export the chapter; otherwise edit the notebook JSON with a small script that replaces the exact substring in the markdown cell and asserts one replacement.

```bash
git add book/apps/training-loop book/apps/README.md book/how-it-works.ipynb book/tools.md
git commit -m "Add training loop playground app

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 23: Next-token sampler

**Files:**
- Create: `book/apps/next-token-sampler/index.html`
- Modify: `book/apps/README.md`, `book/how-it-works.ipynb`, `book/tools.md`

- [ ] **Step 1: Build the app**

A textarea prefilled with about 2 000 words of public-domain English text (the opening of *Alice's Adventures in Wonderland*, Project Gutenberg, public domain, stated in the README row) and a button to load a Norwegian sample (the opening of Ibsen's *Et dukkehjem*, public domain). Controls: order select (1, 2, 3 words of context), temperature slider (0.1 to 2.0), top-k slider (1 to 50, with "off"), a seed prompt input, Generate button, and a "show probabilities" toggle. Algorithm: tokenise on whitespace and punctuation; build an n-gram count table; at each step compute the next-token distribution from counts, apply temperature by raising probabilities to `1/T` and renormalising, apply top-k by keeping the k most likely, sample, append, repeat for 60 tokens. When "show probabilities" is on, render a bar list of the top ten candidates at the last step with their probabilities. Intro: "A language model predicts the next token from the ones before it. This tiny model counts word sequences in the text you paste; the temperature and top-k knobs are the same ones you meet in real tools."

- [ ] **Step 2: Verify**

Generate at temperature 0.1 with order 2: output repeats phrases from the text. Generate at temperature 2.0 with top-k off: output is near-random word salad. Top-k 1 at any temperature gives deterministic output for a fixed seed prompt. No console errors, no network requests.

- [ ] **Step 3: Wire it in and commit**

README row `| next-token-sampler | 2, 4 | Gutenberg text (public domain) |`; link from chapters 2 and 4 and `tools.md`.

```bash
git add book/apps/next-token-sampler book/apps/README.md book/how-it-works.ipynb book/language.ipynb book/tools.md
git commit -m "Add next-token sampler app

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 24: Tokeniser explorer

**Files:**
- Create: `book/apps/tokeniser-explorer/index.html`, `book/apps/tokeniser-explorer/vocab.json`
- Modify: `book/apps/README.md`, `book/language.ipynb`, `book/tools.md`

- [ ] **Step 1: Build the vocabulary**

Train a byte-pair-encoding vocabulary of 4 000 merges offline with a short Python script kept at `scripts/build-tokeniser-vocab.py`: corpus is the two Gutenberg samples from Task 23 plus 20 000 words of English and 20 000 words of Norwegian Wikipedia text downloaded once with the MediaWiki API (`https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles=...` for ten article titles per language listed in the script); the script writes `vocab.json` as `{"merges": [["a","b"], ...]}`. Wikipedia text is CC-BY-SA; note it in the README row. The file must be under 500 KB.

- [ ] **Step 2: Build the app**

A textarea prefilled with one English sentence and its Norwegian translation ("The library is open until eight tonight." / "Biblioteket er åpent til klokka åtte i kveld."). The app applies the merges to the input (byte-level, spaces marked with `▁`) and renders tokens as coloured chips, with counts per line and a ratio. Controls: a slider limiting how many merges are applied (0 to 4 000), so students can watch words fall apart into characters. Intro: "Models do not see words. Type in two languages and compare how many tokens each needs; then lower the number of merges and watch the pieces get smaller."

- [ ] **Step 3: Verify**

The Norwegian sentence uses more tokens than the English one at 4 000 merges; at 0 merges every character is a token. No console errors; the only network request is `vocab.json` at load.

- [ ] **Step 4: Wire it in and commit**

README row `| tokeniser-explorer | 4 | vocab.json trained on Gutenberg (public domain) and Wikipedia (CC-BY-SA) text |`.

```bash
git add book/apps/tokeniser-explorer scripts/build-tokeniser-vocab.py book/apps/README.md book/language.ipynb book/tools.md
git commit -m "Add tokeniser explorer app with bundled BPE vocabulary

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 25: Forward diffusion explorer

**Files:**
- Create: `book/apps/diffusion-explorer/index.html`, `book/apps/diffusion-explorer/sample.jpg`
- Modify: `book/apps/README.md`, `book/how-it-works.ipynb`, `book/images.ipynb`, `book/tools.md`

- [ ] **Step 1: Build the app**

Bundle one sample photograph under 150 KB taken by the course team (ask the coordinator for a fourMs Lab photo; until then use a 512 px crop of the book cover SVG rendered to JPEG with `rsvg-convert` or `inkscape`, noted in the README). Controls: a file input to load the student's own image (read locally with `FileReader`, never uploaded), a step slider 0 to 1 000, a schedule select (linear, cosine), a "play" button that animates from step 0 to 1 000, and a "denoise (blur demo)" toggle that is clearly labelled as an illustration, not a real model. Algorithm: resize the image to 256 px on a canvas; for step t compute `alpha_bar(t)` from the chosen schedule; render `sqrt(alpha_bar) * x + sqrt(1 - alpha_bar) * noise` per pixel with fixed Gaussian noise generated once with Box-Muller; show the numeric signal-to-noise ratio. Plot `alpha_bar` against t with the current step marked. Intro: "Forward diffusion adds noise to a picture in small steps until nothing is left. A real model learns to run this backwards; here you can watch the forward half and see why the schedule matters."

- [ ] **Step 2: Verify**

At step 0 the image is unchanged; at step 1 000 it is indistinguishable from static; cosine and linear differ visibly at step 300. Loading a local file works and no upload occurs. No console errors.

- [ ] **Step 3: Wire it in and commit**

README row `| diffusion-explorer | 2, 5 | sample.jpg (course photo, CC-BY-4.0) |`.

```bash
git add book/apps/diffusion-explorer book/apps/README.md book/how-it-works.ipynb book/images.ipynb book/tools.md
git commit -m "Add forward diffusion explorer app

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 26: Inference energy estimator

**Files:**
- Create: `book/apps/energy-estimator/index.html`
- Modify: `book/apps/README.md`, `book/co-creation-and-ethics.ipynb`, `book/tools.md`

- [ ] **Step 1: Build the app**

Inputs: task type (text classification, text generation short, text generation long, image generation, image generation high resolution, video 5 s) each with a default energy per query in watt-hours taken from the ranges reported in [@Luccioni2024] and stated in a visible "Assumptions" table on the page with the source; number of queries per day; days; grid carbon intensity in g CO2e per kWh with presets (Norway hydro about 30, EU average about 250, coal about 800); water use effectiveness in litres per kWh with a slider 0 to 5 and the note that operators rarely publish it. Output: energy in kWh, CO2e in kg, water in litres, and comparisons rendered as sentences ("about the same as charging a phone N times", "about N kilometres in an electric car at 0.17 kWh per km"). Every default is editable, and a "reset to sources" button restores them. Intro: "Estimates of AI's footprint vary by a factor of a thousand depending on assumptions. This calculator makes the assumptions visible so you can argue about them."

- [ ] **Step 2: Verify**

With image generation, 100 queries per day, 30 days, Norway grid, water 1.8: output is on the order of a few kWh and a few hundred grams of CO2e; changing the grid to coal multiplies CO2e by about 25 while energy stays the same. No console errors, no network requests.

- [ ] **Step 3: Wire it in and commit**

README row `| energy-estimator | 3 | none (defaults cite Luccioni et al. 2024) |`.

```bash
git add book/apps/energy-estimator book/apps/README.md book/co-creation-and-ethics.ipynb book/tools.md
git commit -m "Add inference energy estimator app

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 27: Provenance inspector

**Files:**
- Create: `book/apps/provenance-inspector/index.html`
- Modify: `book/apps/README.md`, `book/co-creation-and-ethics.ipynb`, `book/tools.md`

- [ ] **Step 1: Build the app**

A file input (local only) accepting JPEG, PNG, and WebP. The script parses, without any library: JPEG APP1 EXIF segments for Make, Model, Software, DateTimeOriginal, and the ImageDescription and UserComment fields; JPEG APP11 JUMBF boxes and PNG `caBX` chunks, reporting whether a C2PA manifest is present and listing any claim generator and assertion labels found as plain strings (`c2pa.actions`, `c2pa.hash.data`, and the `softwareAgent` value), without verifying signatures; PNG `tEXt`/`iTXt` chunks, showing keys such as `parameters` (the field several open image tools use to store the prompt and seed). Output is a table of what was found and a short verdict line: "No provenance data found", "Camera metadata found", "Software field present: ...", or "C2PA manifest present (signature not verified here)". Intro: "Files carry traces of how they were made, and sometimes a signed provenance manifest. Drop in an image to see what it says about itself, and what it does not."

- [ ] **Step 2: Verify**

A phone photo shows Make and Model; a PNG saved from an open image tool shows a `parameters` key; a plain screenshot reports no provenance. Nothing is uploaded. No console errors.

- [ ] **Step 3: Wire it in and commit**

README row `| provenance-inspector | 3 | none |`.

```bash
git add book/apps/provenance-inspector book/apps/README.md book/co-creation-and-ethics.ipynb book/tools.md
git commit -m "Add provenance inspector app

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 28: Word-vector explorer

**Files:**
- Create: `book/apps/word-vectors/index.html`, `book/apps/word-vectors/vectors.json`, `scripts/build-word-vectors.py`
- Modify: `book/apps/README.md`, `book/language.ipynb`, `book/tools.md`

- [ ] **Step 1: Build the vectors**

`scripts/build-word-vectors.py` downloads GloVe 6B 50d once (`https://nlp.stanford.edu/data/glove.6B.zip`, Public Domain Dedication and License), keeps the 5 000 most frequent words, quantises to one decimal, and writes `vectors.json` as `{"words": [...], "vectors": [[...], ...]}`. The file must be under 2 MB.

- [ ] **Step 2: Build the app**

Controls: a word input with nearest-neighbour output (top ten by cosine similarity); an analogy form with three inputs (`king - man + woman`) and top five results; a 2D map that projects the vocabulary with a fixed random projection plus the two axes the user picks by typing two words (the axis is the difference vector), and lets students click a point to read its word. Intro: "Before transformers, language models learned a vector for every word. Vectors are how every model in this book represents meaning, and this small English set shows what that captures and what it gets wrong."

- [ ] **Step 3: Verify**

`king - man + woman` returns `queen` in the top five; the neighbours of `oslo` include other capitals; the axis `man` to `woman` places `nurse` and `engineer` on opposite sides, which the chapter uses as the bias example. Only `vectors.json` is requested at load. No console errors.

- [ ] **Step 4: Wire it in and commit**

README row `| word-vectors | 4 | vectors.json from GloVe 6B 50d (PDDL) |`.

```bash
git add book/apps/word-vectors scripts/build-word-vectors.py book/apps/README.md book/language.ipynb book/tools.md
git commit -m "Add word-vector explorer app with bundled GloVe subset

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 29: Markov melody generator

**Files:**
- Create: `book/apps/markov-melody/index.html`
- Modify: `book/apps/README.md`, `book/sound.ipynb`, `book/tools.md`

- [ ] **Step 1: Build the app**

Input: an on-screen two-octave keyboard (also mapped to keys `a s d f g h j k` for white notes and `w e t y u` for black notes) that records a melody of pitch and duration as the student plays, plus a "load example" button with a bundled 32-note folk-style melody written in the script. Controls: order select (1, 2, 3), temperature slider, generate length, tempo, Generate, Play, Stop, Clear. Algorithm: build n-gram counts over (pitch, duration-class) pairs from the recorded melody; generate a continuation by sampling with temperature as in Task 23; play with WebAudio using a triangle oscillator with a short ADSR envelope. Display the recorded and generated melodies as a piano-roll canvas, recorded in one colour and generated in another. Intro: "The folk-tune generators of the 2010s learned melodies from thousands of tunes. This one learns from the melody you play and continues it; the order and temperature knobs decide how much it copies and how much it wanders."

- [ ] **Step 2: Verify**

With the example melody and order 3 at temperature 0.2 the continuation repeats phrases from the input; at temperature 1.5 it wanders; playback is audible and Stop silences it. Keyboard input works without a mouse. No network requests, no console errors.

- [ ] **Step 3: Wire it in and commit**

README row `| markov-melody | 6 | none |`.

```bash
git add book/apps/markov-melody book/apps/README.md book/sound.ipynb book/tools.md
git commit -m "Add Markov melody generator app

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 30: Agent loop simulator

**Files:**
- Create: `book/apps/agent-loop/index.html`
- Modify: `book/apps/README.md`, `book/agents.ipynb`, `book/tools.md`

- [ ] **Step 1: Build the app**

A 10 by 10 grid world drawn on a canvas with a start cell, a goal cell (a "publish" icon), obstacles, and three "tool" cells (search, draft, render) that must be visited in order before the goal counts as done. Controls: Step, Run, Reset, a budget input (max steps), a "perception noise" slider (probability that the agent misreads a neighbouring cell), and a "human checkpoint" toggle that pauses the run after each tool use and asks the student to approve or redirect. The agent is scripted: each step it prints a plan line ("Plan: go to draft"), an action line ("Move north"), and an observation line ("Observed: obstacle north, replanning") in a scrolling trace panel; movement uses breadth-first search on the agent's *believed* map, which drifts from the true map when noise is on. Counters show steps used, budget left, and tool calls. Intro: "An agent is a loop: plan, act, observe, repeat, until the goal is met or the budget runs out. Step through one and watch what noise and a budget do to it, and where a human checkpoint would have helped."

- [ ] **Step 2: Verify**

With noise 0 and budget 60 the agent completes the task; with noise 0.3 it sometimes exhausts the budget, which the trace reports; the checkpoint toggle pauses after each tool cell. Keyboard: Step is reachable by Tab and Space. No network, no console errors.

- [ ] **Step 3: Wire it in and commit**

README row `| agent-loop | 11 | none |`.

```bash
git add book/apps/agent-loop book/apps/README.md book/agents.ipynb book/tools.md
git commit -m "Add agent loop simulator app

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 31: Rhythm-bot

**Files:**
- Create: `book/apps/rhythm-bot/index.html`
- Modify: `book/apps/README.md`, `book/body.ipynb`, `book/tools.md`

- [ ] **Step 1: Build the app**

Input: taps on the space bar or a large pad button (as in the *Sensing Sound and Music* tap-sync app), and an optional microphone onset detector (energy threshold on a `ScriptProcessor` or `AudioWorklet`, analysed locally, never recorded) behind a "Use microphone" button that asks permission. Algorithm: keep the last eight inter-onset intervals; estimate the tempo as their median; estimate the phase from the last onset; the bot plays a click on predicted beats with a WebAudio noise burst, and after four stable beats starts improvising a pattern from a small rule set (a random choice among three subdivisions weighted by a "boldness" slider), always re-anchoring on the human's onsets. Controls: Boldness slider, Follow strength slider (how fast the bot adapts to tempo changes), Mute bot, Reset. A canvas shows a scrolling timeline of human onsets (one colour), bot beats (another), and the current tempo estimate in BPM. Intro: "Dr. Squiggles is a robot at RITMO that listens to your rhythm and plays along. This is its browser cousin: tap a beat, and it will lock on and start improvising. Change the tempo and watch it follow, or lose you."

- [ ] **Step 2: Verify**

Tapping a steady beat at about 100 BPM makes the bot lock within four beats and show 95 to 105 BPM; speeding up gradually is followed when Follow strength is high and lost when it is low; Mute silences the bot but keeps tracking. Microphone mode works on a laptop with the built-in mic when clapping. No network, no console errors.

- [ ] **Step 3: Wire it in and commit**

README row `| rhythm-bot | 12 | none |`.

```bash
git add book/apps/rhythm-bot book/apps/README.md book/body.ipynb book/tools.md
git commit -m "Add rhythm-bot app, a browser cousin of Dr. Squiggles

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

## Phase 5: closing pass

### Task 32: Fill the glossary from bolded terms

**Files:**
- Modify: `book/glossary.md`

- [ ] **Step 1: Extract candidate terms**

```bash
python3 - <<'EOF'
import json, re, glob
terms = {}
for f in sorted(glob.glob("book/*.ipynb")):
    nb = json.load(open(f))
    text = "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "markdown")
    for m in re.finditer(r"\*\*([A-Za-z][A-Za-z0-9 /\-–()]{2,40})\*\*", text):
        t = m.group(1).strip().rstrip(".:,")
        terms.setdefault(t.lower(), (t, f))
for k in sorted(terms):
    print(terms[k][0], "\t", terms[k][1])
print(len(terms), "candidates")
EOF
```

- [ ] **Step 2: Write the definitions**

From the candidate list, keep every technical term (drop emphasis-only bolding such as "What you can do"), aim for about 120 entries, and write each as one or two sentences in the style of the existing ten. Every term must be defined in a chapter; the glossary reminds, it does not introduce. Sort alphabetically. Include at least: agent, aesthetic control, alignment, autoregressive model, bias, brief, C2PA, CFG or guidance scale, classifier, conditioning, context window, ControlNet, co-creation, data, deepfake, diffusion model, distillation, distribution, embedding, embodiment, ethical authorship, fine-tuning, flow matching, foundation model, four E's, GAN, Gaussian splat, generalisation, guidance, hallucination, in-context learning, inference, inpainting, intentionality, latent space, LoRA, loss, mapping (action-sound), memorisation, model card, multimodal model, musicking, negative prompt, NeRF, neural network, open-weight model, outpainting, overfitting, parameters, presence, prompt, provenance, reasoning model, RLHF, sampler, seed, stem separation, sycophancy, temperature, text-to-speech, token, top-k, top-p, training, transformer, vocoder, voice cloning, world model, XR.

- [ ] **Step 3: Build and commit**

```bash
cd book && myst build --html 2>&1 | grep -iE "error" | head; cd ..
git add book/glossary.md
git commit -m "Fill the glossary from terms defined in the chapters

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 33: Cross-link pass, README, cleanup

**Files:**
- Modify: every chapter notebook (cross-references), `README.md`, `book/tools.md`
- Delete: `scripts/build-notebooks.py`, `book/_config.yml`

- [ ] **Step 1: Fix stale chapter references**

```bash
python3 - <<'EOF'
import json, glob, re
old = ["foundations.ipynb", "generative-ai.ipynb", "ai-language.ipynb", "ai-images.ipynb", "ai-sound.ipynb",
       "ai-video.ipynb", "ai-code.ipynb", "ai-3d-games.ipynb", "multimodal-agents.ipynb", "ethics.ipynb", "futures.ipynb"]
for f in sorted(glob.glob("book/*.ipynb")):
    nb = json.load(open(f))
    text = "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "markdown")
    for o in old:
        if o in text:
            print(f, "still references", o)
    for m in re.finditer(r"chapter \[(\d+)\]\(([a-z\-]+)\.ipynb\)", text):
        print(f, "check chapter number", m.group(0))
EOF
```
For every line printed, edit the notebook so the link points at the new file and the chapter number matches the schedule (1 introduction, 2 how-it-works, 3 co-creation-and-ethics, 4 language, 5 images, 6 sound, 7 video, 8 spatial, 9 code, 10 multimodal, 11 agents, 12 body). Use a small replace script that asserts the number of replacements, then rerun the check until it prints nothing.

- [ ] **Step 2: Remove the old scaffolding and legacy config**

```bash
git rm -q scripts/build-notebooks.py book/_config.yml
```
`build-notebooks.py` regenerates the old chapters and would overwrite the new ones; `_config.yml` is a Jupyter Book v1 file that mystmd ignores.

- [ ] **Step 3: Update the README**

Rewrite the "Repository structure" block to list `book/apps/`, `book/templates/`, `book/figures/<chapter>/`, `scripts/md2nb.py`, `scripts/check-chapters.py`, `scripts/tests/`, and the three workflows; add a "Checks" section: `python scripts/tests/test_scripts.py`, `python scripts/check-chapters.py`, `./scripts/verify-book-build.sh`; add the three workflow badges in the same form as the *Sensing Sound and Music* README; update the "Course at a glance" bullets to say the Synthetic Gallery is held in the exam period; add one line on the Explore, Reflect, Create lab structure; add "Enable the pre-push hook once: `git config core.hooksPath .githooks`".

- [ ] **Step 4: Full verification**

```bash
python scripts/tests/test_scripts.py
python scripts/check-chapters.py
bash scripts/verify-book-build.sh
ls book/_build/html/apps
```
Expected: all tests `ok`; `OK: all TOC files pass`; the build ends with `OK: book built with all notebooks executed.`; the apps directory lists the ten first-batch apps. Open `book/_build/html/index.html` in a browser and click through every chapter and every "Explore interactively" link.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "Cross-link pass, README update, remove old scaffolding

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

### Task 34: Second-batch apps (one task each, same shape as Phase 4)

These follow after the first batch and are listed so the plan is complete; each is executed as its own task with the Phase 4 skeleton, verification checks, README row, and chapter link.

- `grid-viewer` (chapter 5): drop four to sixteen local images, enter the one variable each differs in, get a captioned grid rendered to a single PNG the student can save with a Save button (a download link is acceptable here because the page is served from the course site, not an artifact sandbox).
- `frame-consistency` (chapter 7): load a local short clip, sample one frame per 100 ms with a video element and canvas, plot mean absolute pixel difference between consecutive frames, and show the frames at the peaks.
- `splat-viewer` (chapter 8): render a bundled Gaussian splat under 3 MB (a fourMs Lab object captured by the course team, CC-BY-4.0) with a vendored MIT-licensed splat renderer kept beside the page, orbit with mouse and keyboard.
- `cross-modal-sketchpad` (chapter 10): draw a line on a canvas; its height maps to pitch and its thickness to loudness on playback; record a sound with the microphone and see its pitch contour drawn back as a line; nothing leaves the browser.
- `sensor-mapper` (chapter 12): read `DeviceMotion` on a phone or the mouse on a laptop, choose which axis maps to which synth parameter (pitch, filter, tempo), with the mapping table visible and editable, as a one-screen demonstration of a designed action-sound mapping.
- `browser-llm` (chapter 4, stretch): load a small open-weight model through WebGPU from the Hugging Face hub at first use (this is the one app that fetches after load; say so on the page), then chat locally with temperature and top-p sliders.

---

## Self-review notes

- Spec coverage: layers (Task 7, every chapter opening), schedule (Task 7, Tasks 10–21), ERC (Task 7, every lab), template (Task 2 enforces, Tasks 10–21 implement), extra pages (Tasks 6–9, 32), apps (Tasks 22–31, 34), assessment (Task 7, Task 6 gallery), MUS2640 relationship (Tasks 11, 15, 19, 21, Task 7 cards), infrastructure (Tasks 3–5, 33), style (Global Constraints), out of scope respected (no key-based apps in the first batch; the stretch app is flagged).
- Every bib key used in a chapter task appears in Task 5 or in the existing `references.bib` (`Brown2020GPT3`, `Strubell2019Energy`, `AndersenStability`, `GettyStability`, `OpenAISora`, `Radford2021CLIP`, `NBAILab`, `NBWhisper`, `Salma2025`, `Mitchell2019`, `Goodfellow2016`, `Blue1Brown`, `HuggingFaceCourse`, `Weng2021Diffusion`, `Karpathy2015RNN`, `ClaudeCode`, `OpenAIOperator`, `Karpathy2024Software`, `AutoGPT`, `Bridle2022`, `StanfordAIIndex`); the checker in Task 2 catches any miss at build time.
- App folder names are used identically in the chapter tasks, the README rows, and the Explore interactively tips: `training-loop`, `next-token-sampler`, `tokeniser-explorer`, `diffusion-explorer`, `energy-estimator`, `provenance-inspector`, `word-vectors`, `markov-melody`, `agent-loop`, `rhythm-bot`.
