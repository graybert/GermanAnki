# First importable APKG test deck — 2026-07-23

`tools/export_anki.py` now turns canonical frequency cards into an Anki package
with a stable deck ID, note-model ID, semantic-ID-derived note GUIDs, generated
curriculum due order, and the existing native templates and CSS. The first
verified replacement is `dist/German-Core-Test-0001-0010-v3.apkg`.

The package contains 10 notes and 10 German-to-English recognition cards for
ranks 1–10. It contains one note model with 16 fields, including hidden identity,
ordering, rank, status, and future `SentenceAudio` metadata. The package has no
scheduling history and currently contains no media.

`tools/validate_apkg.py` performs a real import into a disposable collection
using Anki's current backend. It checks note/card counts, import warnings, field
counts, rendered fronts and backs, the note type, and imported audio references.
The test package passes all checks.

`tools/build_audio_manifest.py` produces a 200-record work queue with exact main
sentences, sentence hashes, and deterministic MP3 names. The exporter includes
matching MP3 files and inserts their Anki sound markup when `--audio-dir` is
provided; `--require-audio` makes missing files fatal. A temporary one-file
media-package test passed without generating or retaining actual audio.

Problems encountered and their disposition:

- The project previously had no package exporter; one is now implemented.
- `genanki==0.13.1` and `anki==26.5` are pinned and installed locally under
  ignored `.deps/`. Genanki produces the compatibility package; current Anki
  imports it into an isolated collection for validation and rendering tests.
- Version 2 put the real cards in `collection.anki21b`, while its
  `collection.anki2` compatibility database contained only Anki placeholders.
  Version 3 stores all 10 real cards in `collection.anki2` and uses the
  unambiguous flat deck name `German Core Test 0001-0010`.
- The user's live Anki collection was locked and was not touched. Import and
  rendering tests are isolated; a manual GUI check remains useful for final
  visual and interaction testing.

Next: import the 10-card `.apkg` into a test profile, inspect all cards in
desktop and mobile review modes, and confirm that rebuilding/reimporting updates
the same notes before exporting the full 200-card draft deck.
