# German Core Deck — Current Context

Last updated: 2026-07-23 (America/Los_Angeles)

## Purpose

Build a reproducible, text-first local pipeline for an independently authored,
approximately 6,000-note German Anki course inspired only by the pedagogical
structure of Japanese Core 2k/6k. The intended learner is a native English
speaker with roughly 100–200 known German words. Public-release licensing,
stable identities, staged approval, auditability, and current Anki compatibility
are core requirements.

The full originating specification is preserved in the conversation that began
this repository. This file records the current working state and decisions so a
new conversation can resume without relying on chat history.

## Current stage

The **first 200 frequency cards** have been independently authored as complete
text-only drafts, alongside the earlier `wer` prototype. All 5,009 continuous
ranks and headwords have been extracted as local curriculum metadata. A
corpus-wide validator rejects duplicate German sentences and now enforces
continuous unique ranks, complete translations, and three extra examples per
frequency card. Audio and paid APIs remain out of scope.

A public-preview landing page, continuous 200-card browser demo, GitHub Pages
deployment workflow, and draft r/German feedback post are ready. Repository
changes should now be committed after each completed change and pushed whenever
a remote is available.

Deterministic curriculum bundles are defined for core numbers, weekdays, and
months. A generated curriculum-order artifact leaves a unit pending until every
member has a canonical card, then moves the complete unit after its configured
anchor without changing frequency metadata.

Current prototype note:

- Sequence: 1
- Target: `wer`
- Meaning: `who`
- Part of speech: interrogative pronoun
- Forms: nominative `wer`, accusative `wen`, dative `wem`, genitive `wessen`
- Main example: `Wer ist das?` / `Who is that?`
- Seven extra examples cover all four forms. Each German example has its own
  nested reveal for the natural English translation.
- The usage note explains the case changes and why English normally translates
  `wen` and `wem` as “who” rather than formal “whom.”
- Variety/register: neutral Germany Standard German

## Existing artifacts

- `data/canonical/prototype-note.jsonl` — sole prototype note.
- `data/source/frequency-all-5009.jsonl` — rank/headword/POS/page metadata only;
  dictionary definitions and examples are deliberately excluded.
- `data/canonical/frequency-0001-0010.jsonl` — ten complete draft cards with
  forms, original main and extra examples, translations, and usage notes.
- `data/canonical/frequency-0011-0050.jsonl` — forty more complete draft cards
  in the same canonical schema.
- `data/canonical/frequency-0051-0200.jsonl` — 150 complete draft cards in the
  same canonical schema.
- `tools/extract_frequency_headwords.py` — reproducible metadata extractor.
- `tools/build_batch_001.py` — compact authored source and canonical builder.
- `tools/build_batch_002.py` — authored source and canonical builder for ranks
  11–50.
- `tools/build_batch_003.py` and its three text data files — authored source and
  canonical builder for ranks 51–200.
- `tools/validate_cards.py` — required fields, identity, sequence, and global
  German-sentence uniqueness checks.
- `curriculum/bundles.json` and `tools/build_curriculum_order.py` — deterministic
  theme definitions and generated learning order.
- `prototype/card-preview.html` — standalone visual review of front/back in
  light/dark layouts; audio controls are nonfunctional layout mocks.
- `prototype/card-preview.png` and `prototype/card-preview-v2.png` — rendered
  screenshots of prototype iterations.
- `prototype/card-preview-v3.png` — rendered complete-card review with the extra
  examples expanded in the corrected light/dark layout.
- `prototype/anki/front.html`, `back.html`, and `style.css` — Anki-native
  template prototype with optional audio fields.
- `Source Materials/Core 2k_6k Optimized Japanese Vocabulary (3).apkg` — source
  reference, must remain unmodified and must not contribute copyrighted content.
- `Source Materials/German Frequency Dictionary.pdf` — source reference, must
  remain unmodified; redistribution/extraction depends on licensing.

## Current card behavior

- One German-to-English recognition card.
- The front prominently shows only the German target plus an optional sentence
  audio control; no audio exists yet.
- The back repeats the target, then uses tap-to-reveal sections for meaning and
  translation.
- The German example remains visible on the back.
- Extra examples, forms, and usage notes are collapsible secondary sections.
- Inside “More examples,” each German sentence is a nested reveal whose English
  translation stays hidden until tapped.
- Styling is responsive and includes light/dark mode.
- Empty audio fields are conditionally hidden by Anki template sections.
- Frequency rank is retained in canonical metadata and the review controls, but
  is no longer printed on the learner-facing card back.

## Important status and cautions

- Ranks 1–200 have complete draft text and are pending human review.
- `dist/German-Core-Audio-Test-V5-10-Cards.apkg` is the verified audio test package:
  ten notes/cards, stable note identities, no audio, and draft text.
- `tools/export_anki.py` builds rank-bounded packages and can include
  deterministic sentence-audio MP3s later; `tools/validate_apkg.py` inspects
  package structure without touching a user collection.
- No paid API calls or TTS generation have occurred.
- The frequency PDF was identified as the copyrighted 2020 Routledge second
  edition by Erwin Tschirner and Jupp Möhring (315 PDF pages). Its ranking may be
  used as a private curriculum reference, but its definitions and examples must
  not be copied into public artifacts.
- PDF extraction succeeded for all ranks 1–5,009. The local parser dependency is in
  ignored `.vendor/`; extraction is slow but reproducible.
- The source `.apkg` and PDF have not been modified.
- The repository is currently uncommitted (`README.md`, `Source Materials/`,
  `data/`, and `prototype/` are untracked at this checkpoint).
- PowerShell display showed mojibake for UTF-8 punctuation in file output
  (`·` and `▶`); verify whether this is console decoding or file corruption
  before treating it as a template defect.

## Durable-context protocol

For every material change:

1. Update this file with the new current state, decisions, open questions, and
   next action.
2. Add or update a focused Markdown record under `context/` when the change is
   an iteration, decision, research result, test result, or milestone.
3. Never rely on chat history as the sole record of a decision.
4. Keep this file concise enough to read at the start of every future session;
   put detail and history in `context/`.
5. Do not store secrets, copyrighted source extracts, or paid/generated media in
   context files.

## Next action

Confirm the GitHub Pages deployment at `https://graybert.github.io/GermanAnki/`
and request community review using `REDDIT_POST.md`. Review ranks 1–200 in the
local viewer and revise or lock the text. Run
`python tools/validate_cards.py` after every change; never reuse a full German
sentence. After the text pattern is approved, test audio on a small sample
before selecting a deck-wide TTS pipeline. Human-test the 10-card package in a
separate Anki profile before exporting all 200 draft cards.
