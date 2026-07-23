# German Core Deck

This repository contains a complete formatting prototype plus the first 200
fully developed draft cards from a 5,009-entry frequency curriculum. No paid audio
has been generated.

Try the public browser demo at
[graybert.github.io/GermanAnki](https://graybert.github.io/GermanAnki/).

Open `prototype/card-preview.html` to review the proposed front, back, light,
dark, desktop, and mobile layouts. The Anki-native templates are in
`prototype/anki/` and the sole prototype note is in
`data/canonical/prototype-note.jsonl`.

Rebuild the batches with `python tools/build_batch_001.py` and
`python tools/build_batch_002.py`, then `python tools/build_batch_003.py` and
run `python tools/build_curriculum_order.py` followed by
`python tools/validate_cards.py`.
The validator checks the full canonical corpus and rejects reused German
sentences.

The repository currently contains structured Anki note data and Anki-compatible
HTML/CSS templates, but it does not yet produce an importable `.apkg` deck.
