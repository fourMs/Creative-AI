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
