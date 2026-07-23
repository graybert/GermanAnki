# Complete frequency extraction and ranks 51–200 — 2026-07-23

The PDF's continuous ranked section was verified to contain 5,009 entries.
`tools/extract_frequency_headwords.py` now extracts ranks 1–5,009 from PDF pages
20–255 into the ignored local file
`data/source/frequency-all-5009.jsonl`. The output retains only rank, headword,
coarse part of speech, and source page; dictionary definitions and examples are
discarded.

Ranks 51 (`mein`) through 200 (`vier`) were independently authored as 150
complete text-only draft cards. The compact authored inputs are split into
three reviewed text files under `tools/`, and `tools/build_batch_003.py`
reproducibly generates `data/canonical/frequency-0051-0200.jsonl`. Display
labels from the source such as `andere (r, s)` were normalized to card lemmas
such as `andere`, while frequency rank remains authoritative.

The public viewer now loads all 200 frequency cards. The validator was expanded
to require unique continuous frequency ranks, a main English translation,
exactly three translated extra examples per frequency card, and globally unique
German sentences. The completed corpus contains 201 records including the
earlier `wer` prototype and 808 unique German sentences.

Next: obtain community and human language review for ranks 1–200 before locking
text or generating audio. Continue using the complete local extraction rather
than selecting future headwords ad hoc.
