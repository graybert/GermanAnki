# First importable APKG test deck — 2026-07-23

`tools/export_anki.py` now turns canonical frequency cards into an Anki package
with a stable deck ID, note-model ID, semantic-ID-derived note GUIDs, generated
curriculum due order, and the existing native templates and CSS. The first
artifact is `dist/German-Core-Test-0001-0010.apkg`.

The package contains 10 notes and 10 German-to-English recognition cards for
ranks 1–10. It contains one note model with 16 fields, including hidden identity,
ordering, rank, status, and future `SentenceAudio` metadata. The package has no
scheduling history and currently contains no media.

`tools/validate_apkg.py` verifies ZIP members, the SQLite integrity check,
note/card counts, unique GUIDs, field counts, note model and deck presence, and
agreement between `[sound:...]` field references and the package media map. The
test package passes all checks.

`tools/build_audio_manifest.py` produces a 200-record work queue with exact main
sentences, sentence hashes, and deterministic MP3 names. The exporter includes
matching MP3 files and inserts their Anki sound markup when `--audio-dir` is
provided; `--require-audio` makes missing files fatal. A temporary one-file
media-package test passed without generating or retaining actual audio.

Problems encountered and their disposition:

- The project previously had no package exporter; one is now implemented.
- `genanki` is an external dependency; version 0.13.1 is pinned and installed
  locally under ignored `.deps/`.
- That generator lacks modern field/template IDs, so current Anki must use its
  documented name-matching fallback during updates. Field names are now treated
  as stable.
- Windows prevented SQLite from reopening an active `NamedTemporaryFile`; the
  validator now uses a temporary directory and closes the database before
  cleanup.
- The user's live Anki collection was locked and was not touched. Structural
  testing is isolated; a manual import into a separate profile remains required
  for final visual and interaction testing.

Next: import the 10-card `.apkg` into a test profile, inspect all cards in
desktop and mobile review modes, and confirm that rebuilding/reimporting updates
the same notes before exporting the full 200-card draft deck.
