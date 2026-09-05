#!/usr/bin/env python3
"""Train a byte-level BPE vocabulary for the tokeniser explorer app.

Corpus: the two Gutenberg/Wikisource text samples already embedded as
JavaScript string constants in book/apps/next-token-sampler/index.html
(extracted here, not re-downloaded), plus about 20 000 words each of
English and Norwegian Wikipedia text fetched once from the MediaWiki API.

Writes book/apps/tokeniser-explorer/vocab.json as
{"merges": [["a", "b"], ...], "note": "..."} with merges in learned order,
byte-level (each leaf token is a single UTF-8 byte, spelled as one Latin-1
character; a leading "▁" ('lower one eighth block', used the way
SentencePiece uses it) marks the start of a word).

Caveats:
- The word budget in collect_wikipedia_corpus() is only checked between
  whole articles (after each fetch), not within one, so the corpus can
  overshoot WORDS_PER_LANGUAGE by up to one article's worth of words --
  this is why the built vocab.json's English and Norwegian shares are not
  exactly equal.
- Wikipedia extracts are fetched live, at build time, and are not pinned to
  a revision. Re-running this script will hit whatever the ten articles say
  at the time, so it will not reproduce today's vocab.json byte for byte
  even though the code is unchanged.

Usage: python scripts/build-tokeniser-vocab.py
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLER_HTML = os.path.join(ROOT, "book", "apps", "next-token-sampler", "index.html")
OUT_PATH = os.path.join(ROOT, "book", "apps", "tokeniser-explorer", "vocab.json")

NUM_MERGES = 4000
WORD_START = "▁"  # '▁', marks the first byte of a word (SentencePiece convention)

EN_TITLES = [
    "Oslo", "Music", "Photography", "Artificial intelligence", "Norway",
    "University of Oslo", "Painting", "Film", "Language", "Computer",
]
NO_TITLES = [
    "Oslo", "Musikk", "Fotografi", "Kunstig intelligens", "Norge",
    "Universitetet i Oslo", "Maleri", "Film", "Språk", "Datamaskin",
]
WORDS_PER_LANGUAGE = 20000


def fetch_wikipedia_extract(host, title):
    """Fetch the plain-text extract of one Wikipedia article."""
    url = (
        "https://{}/w/api.php?action=query&prop=extracts&explaintext=1"
        "&format=json&titles={}"
    ).format(host, urllib.parse.quote(title))
    req = urllib.request.Request(url, headers={"User-Agent": "Creative-AI-textbook-build/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        return page.get("extract", "") or ""
    return ""


def collect_wikipedia_corpus(host, titles, word_budget):
    """Fetch articles from `host` until roughly `word_budget` words are collected."""
    chunks = []
    total_words = 0
    for title in titles:
        if total_words >= word_budget:
            break
        try:
            text = fetch_wikipedia_extract(host, title)
        except Exception as exc:  # network hiccups shouldn't kill the whole build
            print("  warning: failed to fetch {!r} from {}: {}".format(title, host, exc), file=sys.stderr)
            continue
        text = text.strip()
        if not text:
            print("  warning: no extract for {!r} from {}".format(title, host), file=sys.stderr)
            continue
        words = text.split()
        total_words += len(words)
        chunks.append(text)
        print("  fetched {!r} from {}: {} words (running total {})".format(title, host, len(words), total_words))
    return "\n\n".join(chunks)


def extract_js_string_constant(html, var_name):
    """Pull a single-quoted JS string literal assigned to `var_name` out of the
    next-token-sampler HTML, and decode its JS escapes back to text."""
    pattern = re.compile(r"var\s+" + re.escape(var_name) + r"\s*=\s*'((?:[^'\\]|\\.)*)';")
    m = pattern.search(html)
    if not m:
        raise ValueError("could not find JS string constant {}".format(var_name))
    raw = m.group(1)
    # The literal only uses \\ and \' as JS escapes; unescape via a tiny map
    # rather than pulling in a JS parser.
    return raw.replace("\\'", "'").replace("\\\\", "\\")


def load_gutenberg_samples():
    with open(SAMPLER_HTML, "r", encoding="utf-8") as f:
        html = f.read()
    alice = extract_js_string_constant(html, "ALICE_TEXT")
    dukkehjem = extract_js_string_constant(html, "DUKKEHJEM_TEXT")
    return alice, dukkehjem


def word_to_symbols(word):
    """A word's UTF-8 bytes, each as one Latin-1 character (so a byte value
    0-255 round-trips through JSON as a single-character string); the first
    symbol is prefixed with the word-start marker."""
    b = word.encode("utf-8")
    symbols = [chr(x) for x in b]
    symbols[0] = WORD_START + symbols[0]
    return symbols


def build_word_freqs(text):
    """Split text on whitespace; count occurrences of each resulting word."""
    freqs = {}
    for word in text.split():
        freqs[word] = freqs.get(word, 0) + 1
    return freqs


def train_bpe(word_freqs, num_merges):
    """Pure-Python byte-level BPE: start from per-word symbol sequences (UTF-8
    bytes with a word-start marker on the first byte of each word), repeatedly
    merge the most frequent adjacent symbol pair across the whole corpus, and
    record merges in the order they were learned."""
    corpus = {}  # tuple(symbols) -> count
    for word, count in word_freqs.items():
        symbols = tuple(word_to_symbols(word))
        corpus[symbols] = corpus.get(symbols, 0) + count

    merges = []
    for step in range(num_merges):
        pair_counts = {}
        for symbols, count in corpus.items():
            for i in range(len(symbols) - 1):
                pair = (symbols[i], symbols[i + 1])
                pair_counts[pair] = pair_counts.get(pair, 0) + count
        if not pair_counts:
            break
        best_pair = max(pair_counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
        if pair_counts[best_pair] < 2:
            break
        merges.append(list(best_pair))
        merged_token = best_pair[0] + best_pair[1]

        new_corpus = {}
        for symbols, count in corpus.items():
            new_symbols = []
            i = 0
            n = len(symbols)
            while i < n:
                if i < n - 1 and symbols[i] == best_pair[0] and symbols[i + 1] == best_pair[1]:
                    new_symbols.append(merged_token)
                    i += 2
                else:
                    new_symbols.append(symbols[i])
                    i += 1
            new_symbols = tuple(new_symbols)
            new_corpus[new_symbols] = new_corpus.get(new_symbols, 0) + count
        corpus = new_corpus

        if (step + 1) % 200 == 0 or step == num_merges - 1:
            print("  merge {}/{}: {!r} + {!r} (count {})".format(
                step + 1, num_merges, best_pair[0], best_pair[1], pair_counts[best_pair]))

    return merges


def main():
    start = time.time()

    print("Loading Gutenberg/Wikisource samples from next-token-sampler...")
    alice, dukkehjem = load_gutenberg_samples()
    print("  Alice (English): {} words".format(len(alice.split())))
    print("  Et dukkehjem (Norwegian): {} words".format(len(dukkehjem.split())))

    print("Fetching English Wikipedia extracts...")
    en_wiki = collect_wikipedia_corpus("en.wikipedia.org", EN_TITLES, WORDS_PER_LANGUAGE)
    print("Fetching Norwegian Wikipedia extracts...")
    no_wiki = collect_wikipedia_corpus("no.wikipedia.org", NO_TITLES, WORDS_PER_LANGUAGE)

    corpus_text = "\n\n".join([alice, dukkehjem, en_wiki, no_wiki])
    word_freqs = build_word_freqs(corpus_text)
    print("Corpus: {} words total, {} distinct word forms".format(
        len(corpus_text.split()), len(word_freqs)))

    print("Training byte-level BPE ({} merges)...".format(NUM_MERGES))
    merges = train_bpe(word_freqs, NUM_MERGES)

    note = (
        "Byte-level BPE, {} merges, trained on: Lewis Carroll, \"Alice's "
        "Adventures in Wonderland\" (Project Gutenberg eBook #11, public "
        "domain); Henrik Ibsen, \"Et dukkehjem\" Act One (Norwegian "
        "Wikisource, public domain); and English- and Norwegian-language "
        "Wikipedia extracts for the articles {} (en.wikipedia.org) and {} "
        "(no.wikipedia.org), text available under CC-BY-SA 4.0, "
        "https://creativecommons.org/licenses/by-sa/4.0/. "
        "Word-start marker: U+2581 LOWER ONE EIGHTH BLOCK ('▁')."
    ).format(len(merges), ", ".join(EN_TITLES), ", ".join(NO_TITLES))

    out = {"merges": merges, "note": note}
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    elapsed = time.time() - start
    size = os.path.getsize(OUT_PATH)
    print("Wrote {} ({} merges, {:.1f} KB) in {:.1f}s".format(
        OUT_PATH, len(merges), size / 1024.0, elapsed))
    if size >= 500 * 1024:
        print("WARNING: vocab.json is at or over the 500 KB budget!", file=sys.stderr)


if __name__ == "__main__":
    main()
