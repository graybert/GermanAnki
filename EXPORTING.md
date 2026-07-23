# Exporting German Core to Anki

The current test artifact is:

`dist/German-Core-Audio-Speed-Test-V6-10-Cards.apkg`

It contains one German-to-English recognition card for each frequency rank from
1 through 10. Import it by double-clicking the file or using **File → Import**
in Anki Desktop; `.apkg` files can also be opened by AnkiMobile and AnkiDroid,
but not imported directly into the AnkiWeb website.

## Rebuilding

```powershell
python -m pip install --target .deps -r requirements-export.txt
python tools/build_curriculum_order.py
python tools/export_anki.py --audio-dir data\audio\demo-v5
python tools/validate_apkg.py dist/German-Core-Audio-Speed-Test-V6-10-Cards.apkg `
  --expected-notes 10 `
  --expected-deck "German Core Audio Speed Test V6 - 10 Cards" `
  --required-rendered-text "GERMAN CORE AUDIO TEST V6"
```

The pinned exporter dependencies are installed into the ignored `.deps/`
directory. The resulting `.apkg` is committed so testers do not need Python or
the repository.

## Stable identities and updates

- Deck ID: `2053940118`
- Note model ID: `1603739214`
- Note GUID: deterministically derived from each canonical `semantic_id`
- New-card due order: generated `curriculum_order`

Release V6 of the isolated 10-card audio test uses deck ID `2053940121`, model
ID `1603739217`, and `test-V6:`-namespaced note GUIDs. This deliberately allows it
to coexist with earlier tests and makes a successful new import obvious. The
production values above must remain stable. Rebuilding a production note with the same semantic ID
therefore preserves its note identity for later package imports. The note type
contains these 18 fields:

1. `SemanticID`
2. `CurriculumOrder`
3. `FrequencyRank`
4. `Target`
5. `Meaning`
6. `PartOfSpeech`
7. `GermanSentence`
8. `EnglishSentence`
9. `LiteralTranslation`
10. `ExtraExamples`
11. `Forms`
12. `UsageNote`
13. `WordAudio`
14. `SentenceAudio`
15. `SentenceAudioFile`
16. `Register`
17. `Variety`
18. `TextStatus`

Frequency rank remains metadata and is not used on the visible card template.
Do not rename, remove, or reorder fields casually: Anki may be unable to update
an imported note when its note type has changed.

## Audio-ready behavior

Run `python tools/build_audio_manifest.py` to generate
`data/audio/main-sentence-manifest.jsonl`. Every record contains:

- the exact German main sentence;
- a SHA-256 hash that detects later text changes;
- a deterministic MP3 filename;
- stable note and curriculum identifiers; and
- placeholders for provider, model, voice, and review status.

When audio exists, pass its directory to the exporter:

```powershell
python tools/export_anki.py --audio-dir path\to\approved-mp3
```

The exporter includes correctly named word and sentence MP3s and places Anki
sound references in `WordAudio` and `SentenceAudio`. Their front-template order
queues the word before the sentence when Anki autoplay is enabled, and Anki
provides replay controls on both sides. Use `--require-audio` for a release
build that must fail if any selected card lacks sentence audio. Missing fields
stay empty and their conditional controls remain hidden.

## Expanding the package

The exporter already accepts rank bounds:

```powershell
python tools/export_anki.py `
  --start-rank 1 `
  --end-rank 200 `
  --output dist\German-Core-0001-0200.apkg
```

We are intentionally publishing only the 10-card artifact first so its
appearance and import/update behavior can be tested safely before distributing
all draft cards.

## Problems and limitations encountered

1. The project originally had Anki-looking templates but no note model,
   database, media map, or package exporter; JSONL files cannot be imported as
   an Anki deck by themselves.
2. Creating `.apkg` files requires packaging dependencies. We pin
   `genanki==0.13.1` to construct the source notes and `anki==26.5` to import
   them into an isolated collection and export Anki's current package format.
3. The first artifact used genanki's legacy package format. Although a real
   current-Anki import test proved that it contained 10 working cards, GitHub
   cannot preview an `.apkg`, and its nested deck name made the result less
   obvious. Version 3 uses the flat deck name
   `German Core Test 0001-0010` and stores all real cards directly in the
   broadly compatible `collection.anki2` database. Anki's current backend is
   then used to test-import and render the finished file.
4. The validator now performs a real import into a disposable collection using
   Anki's current backend. It checks note/card counts, import warnings, field
   counts, rendered fronts and backs, the note type, and packaged audio
   references.
5. The installed user's Anki collection was open and locked, so it was
   deliberately not modified or used for testing. Package validation is
   isolated and cannot damage the user's collection.
6. Automated import and rendering pass in Anki's current backend. A human GUI
   check is still required to confirm interactive `<details>` behavior and
   visual rendering across Anki Desktop, AnkiMobile, and AnkiDroid.
7. The audio packaging path has been tested with a temporary placeholder file,
   but no pronunciation or real codec quality has been tested because actual
   TTS generation has not started.
8. All exported card text is still marked
   `draft_complete_pending_human_review`; package validity does not imply that
   every linguistic choice has been approved.
