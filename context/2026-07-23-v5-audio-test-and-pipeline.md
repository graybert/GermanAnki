# V5 audio test and generation pipeline — 2026-07-23

The test package is `dist/German-Core-Audio-Test-V5-10-Cards.apkg`. Its internal
deck name is `German Core Audio Test V5 - 10 Cards`, and both faces show
`GERMAN CORE AUDIO TEST V5`. New test deck/model IDs and V5-namespaced GUIDs
make it coexist with prior test releases.

The note schema now has independent `WordAudio` and `SentenceAudio` fields.
On both faces the word control is beside the target and the sentence control is
below it. On the front, field order queues word then sentence under Anki's
autoplay behavior. Both controls remain replayable.

Rank 1 embeds two Wikimedia Commons MP3 transcodes. The `der` recording is a
native pronunciation and reusable under CC BY-SA 3.0. The sentence recording is
a native German example under CC BY-SA 4.0 but does not match the canonical
sentence; it is explicitly a temporary sequencing/layout sample.

`data/audio/main-sentence-manifest.jsonl` holds all 200 exact main sentences,
hashes, identities, ranks, curriculum positions, and deterministic filenames.
`tools/generate_elevenlabs_audio.py` consumes it with dry-run, rank bounds,
limits, resumable skips, atomic partial files, and a local environment API key.
Generated paid audio is ignored by Git until reviewed and intentionally added.
