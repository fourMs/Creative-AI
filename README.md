# Creative AI

This is the source code for the open textbook **Creative AI**, a bachelor-level course at the University of Oslo (UiO) open to students from all faculties.

The book has been written using [Jupyter Book v2](https://next.jupyterbook.org/) and the [MyST Markdown](https://mystmd.org/) authoring system. It can be compiled to several formats (HTML, PDF). If you are mainly interested in the content, go to [the build](https://fourms.github.io/Creative-AI/).

## Course at a glance

- **Level:** Bachelor (open to all UiO students)
- **Duration:** 12 teaching weeks
- **Format:** 1 lecture hour and 2 practice hours per week
- **Workload:** ~6 hours of self-study per week
- **Prerequisites:** None. Curiosity, a laptop, and an email address are enough.

The course introduces the field of *Creative AI*, showing how generative models work, how they are used in writing, image-making, music, video, code, design, and games, and how to reflect critically on their use as tools, collaborators, and cultural artefacts.

## Repository structure

```text
book/                MyST/Jupyter Book sources (one .ipynb per chapter)
book/figures/        Figures used in the chapters
book/_static/        Static assets (HTML demos, etc.)
book/references.bib  Bibliography in BibTeX
scripts/             Helper scripts (e.g. local build verification)
.github/workflows/   GitHub Actions for the gh-pages deployment
requirements.txt     Python dependencies for building the book
```

## How to run locally

Install the Python dependencies in a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To run the book using a local server:

```bash
cd book
jupyter book start
```

To build the HTML version of the book:

```bash
cd book
myst build --html
```

For a full local build with executed notebooks (as in CI), use:

```bash
cd book
myst build --html --execute
```

Or from the repository root:

```bash
./scripts/verify-book-build.sh
```

### Run notebook execution before every push (optional)

CI already runs `myst build --html --execute` on `main`. To run the same check locally before `git push`, enable this repository's hooks once:

```bash
git config core.hooksPath .githooks
```

To push without the check (e.g. a docs-only WIP branch):

```bash
SKIP_BOOK_VERIFY=1 git push
```

## Authoring notes

- Chapters live as Jupyter notebooks (`*.ipynb`) in `book/`. Text cells use MyST Markdown; you can mix Python (or other) code cells freely where executable demos help the argument.
- Each chapter starts with a YAML frontmatter cell that sets the title, subtitle, and description.
- Use the directive `:::{important}`, `:::{tip}`, `:::{warning}`, etc. for callouts.
- Cite literature with `[@CitationKey]` against entries in `book/references.bib`.
- New chapters must be added to the `toc` in `book/myst.yml`.

The source repository lives at <https://github.com/fourMs/Creative-AI>.

## Credits

Compiled at the University of Oslo. The textbook is released as Open Education under the [Creative Commons Attribution 4.0 (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/) licence, except where otherwise noted.

Substantial portions of the prose have been *co-written* with large language models and then revised by humans. Where AI tools have produced figures, sketches, or examples used in the book, this is indicated locally.
