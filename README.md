# German Core Deck

This repository contains a complete formatting prototype plus the first 50
fully developed draft cards from a 500-word frequency curriculum. No paid audio
has been generated.

Open `prototype/card-preview.html` to review the proposed front, back, light,
dark, desktop, and mobile layouts. The Anki-native templates are in
`prototype/anki/` and the sole prototype note is in
`data/canonical/prototype-note.jsonl`.

Rebuild the batches with `python tools/build_batch_001.py` and
`python tools/build_batch_002.py`, then run `python tools/validate_cards.py`.
The validator checks the full canonical corpus and rejects reused German
sentences.
