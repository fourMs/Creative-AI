#!/usr/bin/env python3
"""Who did what, measured from the commit history (run: .venv/bin/python scripts/authorship_stats.py).

Writes book/data/authorship.json, which the overview's author's note prints. The numbers are
never typed into the prose. CI checks out one commit only, so the file is made locally and
committed; run the script again before a release.
"""
import json
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout


def main():
    sep = "\x1e"
    log = git("log", f"--format=%ad%x1f%(trailers:key=Co-Authored-By,valueonly,separator=%x1d){sep}", "--date=short")
    commits = [c.strip("\n").split("\x1f") for c in log.split(sep) if c.strip()]
    dates = sorted(c[0] for c in commits)
    tools = {}
    with_agent = 0
    for _, trailers in commits:
        names = {re.sub(r"\s*<.*", "", t).split()[0] for t in trailers.split("\x1d") if t.strip()}
        with_agent += bool(names)
        for n in names:
            tools[n] = tools.get(n, 0) + 1
    out = dict(measured=date.today().isoformat(), first_commit=dates[0], commits=len(commits),
               commits_with_agent=with_agent, by_agent=dict(sorted(tools.items(), key=lambda kv: -kv[1])),
               apps=len([p for p in (ROOT / "book" / "apps").iterdir() if (p / "index.html").exists()]))
    path = ROOT / "book" / "data" / "authorship.json"
    path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(path.read_text())


if __name__ == "__main__":
    main()
