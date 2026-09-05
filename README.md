# Creative AI

[![Deploy Jupyter Book](https://github.com/fourMs/Creative-AI/actions/workflows/deploy.yml/badge.svg)](https://github.com/fourMs/Creative-AI/actions/workflows/deploy.yml)
[![Link check](https://github.com/fourMs/Creative-AI/actions/workflows/linkcheck.yml/badge.svg)](https://github.com/fourMs/Creative-AI/actions/workflows/linkcheck.yml)
[![Accessibility](https://github.com/fourMs/Creative-AI/actions/workflows/accessibility.yml/badge.svg)](https://github.com/fourMs/Creative-AI/actions/workflows/accessibility.yml)

This is the source code for the open textbook **Creative AI**, a bachelor-level course at the University of Oslo (UiO) open to students from all faculties.

The book has been written using [Jupyter Book v2](https://next.jupyterbook.org/) and the [MyST Markdown](https://mystmd.org/) authoring system. It can be compiled to several formats (HTML, PDF). If you are mainly interested in the content, go to [the build](https://fourms.github.io/Creative-AI/).

## Course at a glance

- **Level:** Bachelor (open to all UiO students)
- **Duration:** 12 teaching weeks
- **Format:** 45-minute lecture + 90-minute lab per week
- **Workload:** ~6 hours of self-study per week
- **Prerequisites:** None. Curiosity, a laptop, and an email address are enough.
- **Labs:** every weekly lab runs the same three movements, Explore, Reflect, and Create.
- **Assessment:** the semester project is the exam, graded A to F. It is performed or installed at *The Synthetic Gallery*, which is held in the exam period. The weekly log and the other activities are obligatory and assessed pass or fail.

The course introduces the field of *Creative AI*, showing how generative models work, how they are used in writing, image-making, music, video, code, design, and games, and how to reflect critically on their use as tools, collaborators, and cultural artefacts.

## Repository structure

```text
book/                       MyST/Jupyter Book sources (one .ipynb per chapter)
book/myst.yml               Book configuration and table of contents
book/apps/                  Eleven self-contained browser apps, one folder each
book/templates/             Student templates (practice log, gallery page, and so on)
book/figures/<chapter>/     Figures, one folder per chapter
book/_static/               Static assets (HTML demos, and the like)
book/references.bib         Bibliography in BibTeX
scripts/md2nb.py            Converts a Markdown chapter draft into a notebook
scripts/check-chapters.py   Checks chapter structure, citations, and figures
scripts/check-style.py      Checks prose against the course style guide
scripts/verify-book-build.sh  Full local build, exactly as CI runs it
scripts/tests/              Tests for the scripts above
.github/workflows/deploy.yml         Builds the book and publishes it to GitHub Pages
.github/workflows/linkcheck.yml      Checks every link in the built site
.github/workflows/accessibility.yml  Runs pa11y over the built site
requirements.txt            Python dependencies for building the book
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

## Checks

Three checks run over the sources, and the last one runs the first two for you:

```bash
python scripts/tests/test_scripts.py   # tests for the helper scripts
python scripts/check-chapters.py       # chapter structure, citations, figures
./scripts/verify-book-build.sh         # full build with every notebook executed
```

Prose style is checked separately by `python scripts/check-style.py`, which reports rather than fails unless you pass `--strict`. The style guide it enforces is the course folder's STYLE.md, which lives outside this repository.

Enable the pre-push hook once, and every push runs the full build first:

```bash
git config core.hooksPath .githooks
```

## Bundled apps

Eleven single-page apps ship with the book. They run in the browser, need no account, and send no data anywhere. Each lives in its own folder under `book/apps/`, and the deploy workflow copies them to `/apps/` on the site.

| App | Chapter | What it shows |
| --- | --- | --- |
| [training-loop](https://fourms.github.io/Creative-AI/apps/training-loop/) | 2 | A tiny model's loss falling step by step as it trains |
| [next-token-sampler](https://fourms.github.io/Creative-AI/apps/next-token-sampler/) | 2, 4 | Greedy, temperature, and top-p sampling on one distribution |
| [diffusion-explorer](https://fourms.github.io/Creative-AI/apps/diffusion-explorer/) | 2, 5 | An image dissolving into noise, and the reverse |
| [evolve](https://fourms.github.io/Creative-AI/apps/evolve/) | 2, 9 | Breeding a drawing by choosing favourites, biomorph style |
| [energy-estimator](https://fourms.github.io/Creative-AI/apps/energy-estimator/) | 3 | Energy and water per query, with the assumptions exposed |
| [provenance-inspector](https://fourms.github.io/Creative-AI/apps/provenance-inspector/) | 3 | What metadata a generated file carries, and what it proves |
| [tokeniser-explorer](https://fourms.github.io/Creative-AI/apps/tokeniser-explorer/) | 4 | How a sentence splits into tokens, and why Norwegian costs more |
| [word-vectors](https://fourms.github.io/Creative-AI/apps/word-vectors/) | 4 | How embeddings place related words near each other |
| [markov-melody](https://fourms.github.io/Creative-AI/apps/markov-melody/) | 6 | A short melody generated from a Markov chain |
| [agent-loop](https://fourms.github.io/Creative-AI/apps/agent-loop/) | 11 | An agent's plan, act, and observe loop, one call at a time |
| [rhythm-bot](https://fourms.github.io/Creative-AI/apps/rhythm-bot/) | 12 | A tapped rhythm mapped onto a generative pattern, live |

See [book/apps/README.md](book/apps/README.md) for the conventions and the licences of the bundled data.

## Credits

Compiled at the University of Oslo. The textbook is released as Open Education under the [Creative Commons Attribution 4.0 (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/) licence, except where otherwise noted.

Substantial portions of the prose have been *co-written* with large language models and then revised by humans. Where AI tools have produced figures, sketches, or examples used in the book, this is indicated locally.
