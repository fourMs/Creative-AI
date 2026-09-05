#!/usr/bin/env python3
"""Build the bundled word-vector file for the word-vector explorer app.

Source: GloVe 6B, 50-dimensional vectors, trained by Pennington, Socher, and
Manning (2014) on a 6-billion-token corpus (Wikipedia 2014 + Gigaword 5),
released under the Public Domain Dedication and License (PDDL) v1.0.
Downloaded once from https://nlp.stanford.edu/data/glove.6B.zip (about
822 MB; the request is redirected to
https://downloads.cs.stanford.edu/nlp/data/glove.6B.zip, which this script
follows automatically).

The zip contains four files (50d, 100d, 200d, 300d); only glove.6B.50d.txt
is extracted. That file lists one word per line, most frequent word first
(the GloVe authors built the vocabulary in frequency order), each followed
by 50 space-separated floating-point vector components. This script keeps
only the first 7 000 lines (the 7 000 most frequent words), quantises each
component to one decimal place to shrink the output, and writes
book/apps/word-vectors/vectors.json as
{"words": [...], "vectors": [[...], ...], "note": "..."}.

The downloaded zip (and the extracted .txt, which is about 65 MB for just
the 50d file) are deleted at the end of a successful run; neither is meant
to be committed.

Usage: python scripts/build-word-vectors.py
"""
import io
import json
import os
import sys
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "book", "apps", "word-vectors")
OUT_PATH = os.path.join(OUT_DIR, "vectors.json")
WORK_DIR = os.path.join(ROOT, "scripts", "_word-vectors-build")
ZIP_PATH = os.path.join(WORK_DIR, "glove.6B.zip")
TXT_NAME = "glove.6B.50d.txt"
TXT_PATH = os.path.join(WORK_DIR, TXT_NAME)

GLOVE_URL = "https://nlp.stanford.edu/data/glove.6B.zip"
NUM_WORDS = 7000
DIMS = 50
NOTE = (
    "GloVe 6B 50d, Pennington, Socher, and Manning 2014, "
    "Public Domain Dedication and License; first 7 000 words"
)


def download(url, dest):
    print("Downloading {} ...".format(url), file=sys.stderr)
    req = urllib.request.Request(url, headers={"User-Agent": "Creative-AI-textbook-build/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as out:
        total = 0
        chunk = resp.read(1 << 20)
        while chunk:
            out.write(chunk)
            total += len(chunk)
            chunk = resp.read(1 << 20)
    print("Downloaded {} bytes to {}".format(total, dest), file=sys.stderr)


def extract_50d(zip_path, txt_name, dest_path):
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(txt_name) as src, open(dest_path, "wb") as dst:
            data = src.read(1 << 20)
            while data:
                dst.write(data)
                data = src.read(1 << 20)


def build_vectors_json(txt_path, out_path, num_words, dims):
    words = []
    vectors = []
    with io.open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            if len(words) >= num_words:
                break
            parts = line.rstrip("\n").split(" ")
            if len(parts) != dims + 1:
                continue
            word = parts[0]
            try:
                vec = [round(float(x), 1) for x in parts[1:]]
            except ValueError:
                continue
            words.append(word)
            vectors.append(vec)

    if len(words) < num_words:
        print(
            "warning: only found {} usable words (wanted {})".format(len(words), num_words),
            file=sys.stderr,
        )

    payload = {"words": words, "vectors": vectors, "note": NOTE}

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with io.open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))

    size = os.path.getsize(out_path)
    print("Wrote {} words x {} dims to {} ({} bytes)".format(len(words), dims, out_path, size), file=sys.stderr)
    return size


def main():
    os.makedirs(WORK_DIR, exist_ok=True)
    try:
        if not os.path.exists(ZIP_PATH):
            download(GLOVE_URL, ZIP_PATH)
        else:
            print("Reusing existing download at {}".format(ZIP_PATH), file=sys.stderr)

        print("Extracting {} ...".format(TXT_NAME), file=sys.stderr)
        extract_50d(ZIP_PATH, TXT_NAME, TXT_PATH)

        size = build_vectors_json(TXT_PATH, OUT_PATH, NUM_WORDS, DIMS)
        if size > 2 * 1024 * 1024:
            print("ERROR: vectors.json is {} bytes, over the 2 MB limit".format(size), file=sys.stderr)
            sys.exit(1)
    finally:
        for path in (TXT_PATH, ZIP_PATH):
            if os.path.exists(path):
                os.remove(path)
                print("Deleted {}".format(path), file=sys.stderr)
        try:
            os.rmdir(WORK_DIR)
        except OSError:
            pass


if __name__ == "__main__":
    main()
