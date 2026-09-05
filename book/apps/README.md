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
| next-token-sampler | 2, 4 | Gutenberg text (public domain) |
