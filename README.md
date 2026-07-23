# German Core Deck

This repository contains a complete formatting prototype plus the first 350
fully developed draft cards from a 5,009-entry frequency curriculum. The V7
test deck contains paid dual-voice word and sentence audio for ranks 1–10.

Try the public browser demo at
[graybert.github.io/GermanAnki](https://graybert.github.io/GermanAnki/).
The landing page also offers an importable 10-card `.apkg` test deck.

Open `prototype/card-preview.html` to review the proposed front, back, light,
dark, desktop, and mobile layouts. The Anki-native templates are in
`prototype/anki/` and the sole prototype note is in
`data/canonical/prototype-note.jsonl`.

Rebuild the batches with `python tools/build_batch_001.py`,
`python tools/build_batch_002.py`, `python tools/build_batch_003.py`, and
`python tools/build_batch_004.py --require-through 350`, then
run `python tools/build_curriculum_order.py` followed by
`python tools/validate_cards.py`.
The validator checks the full canonical corpus and rejects reused German
sentences.

The repository currently contains structured Anki note data and Anki-compatible
HTML/CSS templates. To rebuild the test package:

```powershell
python -m pip install --target .deps -r requirements-export.txt
python tools/export_anki.py --audio-dir data\audio\test-v7-first-10 --require-audio
python tools/validate_apkg.py dist/German-Core-Dual-Voice-Audio-Test-V7-10-Cards.apkg `
  --expected-notes 10 `
  --expected-deck "German Core Dual Voice Audio Test V7 - 10 Cards" `
  --required-rendered-text "GERMAN CORE AUDIO TEST V7"
```

See `AUDIO.md` for sources and ElevenLabs generation, and `EXPORTING.md` for the
field schema, limitations, and path from 10 cards to the full curriculum.
