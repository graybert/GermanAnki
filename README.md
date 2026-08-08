# German Core Deck

This repository contains a complete formatting prototype plus the first 2,800
fully developed draft cards from a 5,009-entry frequency curriculum. Verified
dual-voice word and sentence audio is verified through rank 2,200.

Try the public browser demo at
[graybert.github.io/GermanAnki](https://graybert.github.io/GermanAnki/).
The landing page offers an importable 1,250-card text preview and a verified
1,600-card dual-voice audio deck published as a GitHub Release asset; the next
2,200-card package is locally validated and awaiting release publication.

Open `prototype/card-preview.html` to review the proposed front, back, light,
dark, desktop, and mobile layouts. The Anki-native templates are in
`prototype/anki/` and the sole prototype note is in
`data/canonical/prototype-note.jsonl`.

Rebuild the batches with `python tools/build_batch_001.py`,
`python tools/build_batch_002.py`, `python tools/build_batch_003.py`, and
`python tools/build_batch_004.py --require-through 500`,
`python tools/build_batch_005.py --require-through 1000`,
`python tools/build_batch_006.py --require-through 1250`, then
run `python tools/enrich_sentence_contexts.py`,
`python tools/build_curriculum_order.py`, `python tools/build_audio_manifest.py`,
`python tools/validate_cards.py`, and `python tools/build_completion_status.py`.
The validator checks the full canonical corpus and rejects reused German
sentences. It also enforces the sentence-design policy: no example over 20
words and at least two context-rich 9–20-word examples per frequency card.
The completion index is derived rather than manually edited: a card is complete
only when its contextual text review is finalized and both deterministic audio
files are present in the published web corpus with matching hashes.

Check the exact live ElevenLabs balance and current manifest requirement with
`python tools/check_elevenlabs_credits.py`. The key remains in the ignored local
secret file and is never printed.

The repository currently contains structured Anki note data and Anki-compatible
HTML/CSS templates. To rebuild the test package:

```powershell
python -m pip install --target .deps -r requirements-export.txt
python tools/export_anki.py --audio-dir data\audio\test-v7-first-10 --require-audio
python tools/validate_apkg.py dist/German-Core-Dual-Voice-Audio-Test-V8-10-Cards.apkg `
  --expected-notes 10 `
  --expected-deck "German Core Dual Voice Audio Test V8 - 10 Cards" `
  --required-rendered-text "GERMAN CORE AUDIO TEST V8"
```

See `AUDIO.md` for sources and ElevenLabs generation, and `EXPORTING.md` for the
field schema, limitations, and path from 10 cards to the full curriculum.
