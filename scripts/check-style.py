#!/usr/bin/env python3
"""Report style issues against the book's style guide.

The book's own style guide lives outside this repository, at
`/home/alexanje/UiO Dropbox/alexanje@uio.no/Undervisning/2027v/Creative AI/STYLE.md`
(admin and process documents live in Dropbox; only the book lives on
GitHub). Read that document for the rules this checker enforces.

Usage:
    python scripts/check-style.py [--book book] [--strict] [--files FILE ...]

By default this reads every TOC file in `book/myst.yml` (via `toc_files`
and `text_of`, imported from `check-chapters.py`). Pass `--files` to check
specific Markdown or notebook files directly instead (used, for example,
to check documents that are not part of the book's table of contents).

Each file's prose is stripped of fenced code blocks, admonition option
lines (`:class:`, `:label:`, `:width:`), Markdown tables, and front
matter, then scanned line by line for:

    contraction        contractions such as "don't", "it's"
    bold-in-sentence    double-starred emphasis used mid-sentence
                        rather than as a line-start label, a
                        list-item lead, or a table cell
    paragraph-opener    a paragraph opening with "Moreover",
                        "Furthermore", "Additionally", "Ultimately",
                        "Importantly", or "Crucially"
    long-sentence       a sentence over forty words
    "audiovisual"       "audiovisual" outside "Audiovisual Rhythms"
                        and cite keys, or the hyphenated forms
                        "audio-visual" / "auditory-visual"
    first-person        first-person singular "I" in prose
    lecturer-we         the lecturer's "we" ("we will", "let us", and
                        the like); report-only, never fails --strict,
                        because "we" about UiO or the fourMs Lab is
                        allowed and needs human judgement
    exclamation         an exclamation mark in prose
    em-dash             a sentence with exactly one em dash, outside
                        Further reading list items and outside a list
                        item titled with bold, a link, or a citation

Three things are exempt throughout: the em dash used as the list-item
separator inside ":::{seealso} Further reading" blocks and inside any
list item whose title is bold, linked, or cited (the reading-list and
tool-list convention); quoted or *italicised* example text, for the
first-person and "audiovisual" rules, so this rulebook can name the
very word it bans; and all content inside ":::{tip} Explore
interactively" blocks (the app links), which is skipped entirely.

Exit 0 and print per-file, per-category counts. With --strict, exit 1
if any category other than lecturer-we has a hit anywhere.
"""
import argparse, importlib.util, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

_spec = importlib.util.spec_from_file_location("check_chapters", os.path.join(HERE, "check-chapters.py"))
check_chapters = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_chapters)
text_of = check_chapters.text_of
toc_files = check_chapters.toc_files

ALLOWLIST_PATH = os.path.join(HERE, "style-allowlist.txt")

CONTRACTIONS = [
    "don't", "it's", "isn't", "you're", "we're", "can't", "won't", "let's",
    "that's", "there's", "doesn't", "didn't", "aren't", "wasn't", "hasn't",
    "haven't", "wouldn't", "couldn't", "shouldn't", "I'm", "they're",
]
CONTRACTION_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in CONTRACTIONS) + r")\b", re.IGNORECASE)

OPENERS = ["Moreover", "Furthermore", "Additionally", "Ultimately", "Importantly", "Crucially"]
OPENER_RE = re.compile(r"^(" + "|".join(OPENERS) + r")\b")

CRITICAL_LABELS = {"The claim.", "The evidence.", "The method.", "The limits."}
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")

ABBR_RE = re.compile(r"\b(e\.g|i\.e|Dr|Fig|Mr|Mrs|Ms|vs|etc|Prof|St|No|cf)\.")

WE_PHRASES = ["we will", "we now", "we have seen", "we turn", "let us", "we return", "we look at", "we can see", "we saw"]
WE_RE = re.compile(r"\b(" + "|".join(re.escape(p) for p in WE_PHRASES) + r")\b", re.IGNORECASE)

AUDIOVISUAL_RE = re.compile(r"\baudiovisual\b", re.IGNORECASE)
AUDIO_HYPHEN_RE = re.compile(r"\baudio-visual\b", re.IGNORECASE)
AUDITORY_HYPHEN_RE = re.compile(r"\bauditory-visual\b", re.IGNORECASE)

FIRST_PERSON_RE = re.compile(r"(?<![\w'])I(?=\s|$)")

FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n?", re.S)
FENCED_CODE_RE = re.compile(r"(?ms)^```.*?^```[ \t]*$\n?")
OPTION_LINE_RE = re.compile(r"(?m)^[ \t]*:(class|label|width):.*$\n?")
TABLE_LINE_RE = re.compile(r"(?m)^[ \t]*\|.*\|[ \t]*$\n?")

FURTHER_READING_START = ":::{seealso} Further reading"
EXPLORE_TIP_START = ":::{tip} Explore interactively"
FENCE_END = ":::"

# A list item whose title is a bold span, a Markdown link, or a citation key
# uses the em dash as a "title — description" separator (the reading-list and
# tool-list convention), not the mid-sentence drama dash rule 13 warns about.
LIST_MARKER_RE = re.compile(r"^[ \t]*(?:[-*+]|\d+\.)[ \t]+")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\([^)]+\)")
CITE_KEY_RE = re.compile(r"\[@[^\]]+\]")
BOLD_LEAD_RE = re.compile(r"^\*\*.+?\*\*")

# A single, unnested *italic* span (never the "*" of a "**bold**" pair).
ITALIC_RE = re.compile(r"(?<!\*)\*(?!\*)([^*\n]*?)(?<!\*)\*(?!\*)")

CATEGORIES = [
    "contraction", "bold-in-sentence", "paragraph-opener", "long-sentence",
    "audiovisual", "first-person", "lecturer-we", "exclamation", "em-dash",
]


def strip_non_prose(text):
    text = FRONT_MATTER_RE.sub("", text)
    text = FENCED_CODE_RE.sub("", text)
    text = OPTION_LINE_RE.sub("", text)
    text = TABLE_LINE_RE.sub("", text)
    return text


def mask_quotes(line):
    line = re.sub(r'"[^"]*"', lambda m: "�" * len(m.group(0)), line)
    line = re.sub(r"“[^”]*”", lambda m: "�" * len(m.group(0)), line)
    return line


def mask_examples(line):
    """Mask quoted text and *italicised* example text (a line at a time; this
    never reaches across lines). Used by rules where such text is an example
    or a mention rather than the author's own voice: first-person "I" and the
    word "audiovisual". Bold **spans** are left untouched: the italic pattern
    never matches a "*" that is part of a "**" pair."""
    line = mask_quotes(line)
    # Do not let a leading "* " or "1. " list marker read as an italic
    # delimiter: blank it out first, in place, so positions do not shift.
    m = LIST_MARKER_RE.match(line)
    if m:
        line = " " * len(m.group(0)) + line[len(m.group(0)):]
    line = ITALIC_RE.sub(lambda mm: "�" * len(mm.group(0)), line)
    return line


def is_titled_list_item(line):
    """A list item is exempt from the em-dash rule when its title is a bold
    span, a Markdown link, or a citation key: the "title — description"
    convention used throughout the reading and tool lists."""
    m = LIST_MARKER_RE.match(line)
    if not m:
        return False
    rest = line[m.end():]
    return bool(BOLD_LEAD_RE.match(rest) or MD_LINK_RE.search(rest) or CITE_KEY_RE.search(rest))


def load_allowlist():
    if not os.path.exists(ALLOWLIST_PATH):
        return set()
    entries = set()
    for raw in open(ALLOWLIST_PATH, encoding="utf-8"):
        s = raw.strip()
        if s and not s.startswith("#"):
            entries.add(s)
    return entries


def is_line_start_bold(line, start_idx):
    prefix = line[:start_idx]
    prefix = re.sub(r"^[ \t]*(?:>[ \t]*)*(?:[-*+][ \t]+|\d+\.[ \t]+)?", "", prefix)
    return prefix == ""


def excerpt(line, start, end, width=40):
    lo, hi = max(0, start - width), min(len(line), end + width)
    return line[lo:hi].strip()


def sentences_of(line):
    protected = ABBR_RE.sub(lambda m: m.group(1) + "\x00", line)
    parts = re.split(r"[.!?]+", protected)
    return [p.replace("\x00", ".").strip() for p in parts if p.strip()]


def check_text(text, allowlist):
    """Return a list of (line_no, category, snippet) hits."""
    hits = []
    text = strip_non_prose(text)
    in_explore = False
    in_further = False

    for lineno, line in enumerate(text.split("\n"), start=1):
        stripped = line.strip()

        if stripped.startswith(EXPLORE_TIP_START):
            in_explore = True
            continue
        if stripped.startswith(FURTHER_READING_START):
            in_further = True
            continue
        if stripped == FENCE_END:
            in_explore = False
            in_further = False
            continue
        if in_explore:
            continue

        # contractions (quotation marks excluded; headings only allowed via the allowlist)
        is_heading = stripped.startswith("#")
        heading_text = re.sub(r"^#+\s*", "", stripped).strip() if is_heading else None
        if not (is_heading and heading_text in allowlist):
            masked = mask_quotes(line)
            for m in CONTRACTION_RE.finditer(masked):
                hits.append((lineno, "contraction", excerpt(line, m.start(), m.end())))

        # bold inside a sentence
        for m in BOLD_RE.finditer(line):
            if m.group(1) in CRITICAL_LABELS:
                continue
            if is_line_start_bold(line, m.start()):
                continue
            hits.append((lineno, "bold-in-sentence", excerpt(line, m.start(), m.end())))

        # paragraph openers (this book writes one paragraph per line)
        if not is_heading and not re.match(r"^[ \t]*(?:[-*+]|\d+\.)[ \t]+", line):
            m = OPENER_RE.match(stripped)
            if m:
                hits.append((lineno, "paragraph-opener", excerpt(stripped, m.start(), m.end())))

        # sentence length, and single em dash per sentence
        titled_item = is_titled_list_item(line)
        for sentence in sentences_of(line):
            words = sentence.split()
            if len(words) > 40:
                hits.append((lineno, "long-sentence", sentence[:80]))
            if sentence.count("—") == 1 and not in_further and not titled_item:
                hits.append((lineno, "em-dash", sentence[:80]))

        # audiovisual / hyphenated audio-visual / auditory-visual
        # (quoted or *italicised* mentions of the word itself do not count)
        examples_masked = mask_examples(line)
        for m in AUDIOVISUAL_RE.finditer(examples_masked):
            window = line[max(0, m.start() - 15):m.end() + 15]
            if "Audiovisual Rhythms" in window:
                continue
            hits.append((lineno, "audiovisual", excerpt(line, m.start(), m.end())))
        for rx in (AUDIO_HYPHEN_RE, AUDITORY_HYPHEN_RE):
            m = rx.search(examples_masked)
            if m:
                hits.append((lineno, "audiovisual", excerpt(line, m.start(), m.end())))

        # first-person singular (quoted or *italicised* examples excluded)
        for m in FIRST_PERSON_RE.finditer(examples_masked):
            hits.append((lineno, "first-person", excerpt(line, m.start(), m.end())))

        # the lecturer's "we" (report-only)
        m = WE_RE.search(line)
        if m:
            hits.append((lineno, "lecturer-we", excerpt(line, m.start(), m.end())))

        # exclamation marks in prose (excluding the "!" of a Markdown image ![alt](...))
        for m in re.finditer(r"!(?!\[)", line):
            hits.append((lineno, "exclamation", excerpt(line, m.start(), m.end())))

    return hits


def resolve_files(args):
    if args.files:
        return [(f, f) for f in args.files]
    return [(rel, os.path.join(args.book, rel)) for rel in toc_files(args.book)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="book")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--files", nargs="+", default=None,
                     help="check these files directly instead of the book's TOC")
    args = ap.parse_args()

    allowlist = load_allowlist()
    totals = {c: 0 for c in CATEGORIES}
    any_blocking = False

    for rel, path in resolve_files(args):
        if not os.path.exists(path):
            print(f"{rel}: missing file")
            continue
        hits = check_text(text_of(path), allowlist)
        counts = {c: 0 for c in CATEGORIES}
        for lineno, category, snippet in hits:
            counts[category] += 1
            print(f"{rel}:{lineno}: {category}: {snippet}")
        summary = ", ".join(f"{c}={counts[c]}" for c in CATEGORIES if counts[c])
        print(f"{rel}: {{{summary}}}" if summary else f"{rel}: clean")
        for c in CATEGORIES:
            totals[c] += counts[c]
            if c != "lecturer-we" and counts[c]:
                any_blocking = True

    total_summary = ", ".join(f"{c}={totals[c]}" for c in CATEGORIES)
    print(f"TOTAL: {{{total_summary}}}")

    if args.strict and any_blocking:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
