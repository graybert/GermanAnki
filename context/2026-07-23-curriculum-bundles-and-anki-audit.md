# Curriculum bundles and Anki audit — 2026-07-23

The first deterministic thematic bundles are defined in
`curriculum/bundles.json`: core numbers (1–20, tens through 100, and 1,000),
weekdays, and months. Each member is tied to an explicit frequency rank rather
than found by an ambiguous text search. `siebzehn` and `neunzehn` are absent
from the 5,009-entry source list and therefore have stable supplemental IDs.

`tools/build_curriculum_order.py` implements an `when_complete` policy. A unit
remains pending until all members have canonical cards; once complete, its
members are removed from their scattered frequency positions and inserted
after the configured rank-200 anchor in declared pedagogical order. All other
cards retain their relative frequency order, every semantic ID appears exactly
once, and the card validator checks the generated order.

At 200 completed frequency cards, the number bundle has three available
members, while the weekday and month members are all beyond the authored
range. No incomplete bundle is therefore active yet. The browser reviewer now
reads the generated curriculum order, so completed bundles will affect the
demo automatically after rebuilding.

The Anki audit found that the project has canonical note data and Anki-native
front, back, and CSS templates, but no exporter, note model construction, media
packaging, or `.apkg` artifact. The repository is not currently importable as
an Anki deck; a dedicated export pipeline is required.

Using the current average main-sentence length of 35.23 characters, 500 main
sentences project to about 17,615 TTS characters. At the checked ElevenLabs API
rates, that is approximately $0.88 with Flash/Turbo or $1.76 with Multilingual
v2/v3 before taxes, custom voice multipliers, or changed-parameter
regenerations.
