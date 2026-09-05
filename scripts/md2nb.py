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
