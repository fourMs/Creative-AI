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
| training-loop | 2 | none |
| next-token-sampler | 2, 4 | Alice (Project Gutenberg, public domain); Et dukkehjem (Norwegian Wikisource/Runeberg transcription, public domain) |
| tokeniser-explorer | 4 | vocab.json trained on Gutenberg (public domain) and Wikipedia (CC-BY-SA 4.0) text |
| diffusion-explorer | 2, 5 | sample.jpg (course cover render, CC-BY-4.0) |
| energy-estimator | 3 | none (defaults cite Luccioni et al. 2024) |
| provenance-inspector | 3 | none |
| word-vectors | 4 | vectors.json from GloVe 6B 50d (PDDL), first 7 000 words |
| markov-melody | 6 | none |
| agent-loop | 11 | none |
| rhythm-bot | 12 | none |
