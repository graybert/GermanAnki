# German Core Deck — Current Context

Last updated: 2026-08-07 (America/Los_Angeles)

## Purpose

Build a reproducible, text-first local pipeline for an independently authored,
5,009-note German Anki course inspired only by the pedagogical
structure of Japanese Core 2k/6k. The intended learner is a native English
speaker with roughly 100–200 known German words. Public-release licensing,
stable identities, staged approval, auditability, and current Anki compatibility
are core requirements.

The full originating specification is preserved in the conversation that began
this repository. This file records the current working state and decisions so a
new conversation can resume without relying on chat history.

## Current stage

The **first 2,500 frequency cards** have been independently authored as complete
drafts, alongside the earlier `wer` prototype. All 5,009 continuous ranks and
headwords have been extracted as local curriculum metadata. A fresh extraction
on 2026-08-01 matched the saved 5,009 source rows exactly; canonical ranks
1–1,250 are continuous and in source order. Twelve learner-facing targets
normalize source labels containing variants or inflection shorthand, without
changing their ranks.
The hidden `source_headword` field is checked against the extracted row on every
validation run, so later edits cannot silently drift from the official order.

A corpus-wide validator rejects duplicate German sentences and enforces
continuous unique ranks, complete translations, exactly three extra examples,
a 20-word ceiling, and at least two context-rich 9–20-word examples per card.
The current corpus has 5,000 unique German examples for the 1,250 frequency
cards. Deterministic enrichment preserves useful short phrases and adds varied
context only where a card lacks two longer examples.

A public-preview landing page, continuous browser demo, validated 1,250-card
text `.apkg`, verified 2,200-card dual-voice audio `.apkg`, and GitHub Pages
deployment workflow are live. Repository
changes should now be committed after each completed change and pushed whenever
a remote is available.

Deterministic curriculum bundles are defined for core numbers, weekdays, and
months. A generated curriculum-order artifact leaves a unit pending until every
member has a canonical card, then moves the complete unit after its configured
anchor without changing frequency metadata.

## Sentence design policy

- Knowing the headword is sufficient to grade the recognition card; the main
  sentence is the backbone for acquiring grammar and natural usage over time.
- Preserve genuinely common short utterances such as greetings, warnings, and
  fixed phrases. Do not lengthen sentences merely to hit a uniform average.
- Keep German examples at 20 words or fewer and give every card at least two
  examples of 9–20 words. These may be the main sentence, extra examples, or one
  of each.
- Vary person, tense, mood, clause structure, dialogue, narration, and register.
  Draw settings from casual conversation, family life, school, work, news,
  podcasts, museums, nature documentaries, formal prose, fiction, cartoons,
  instructions, and public information.
- `tools/enrich_sentence_contexts.py` applies the minimum deterministic context
  expansion after the authored batch builders run. It uses hundreds of stable
  lead/action combinations and topic cues, leaves ranks 1–10 main sentences
  locked to their paid audio, and never replaces an already qualifying example.
- Deterministic expansions are draft scaffolding, not a substitute for native
  review. Prefer an organically authored longer sentence whenever one is
  available, and record that sentence in the compact batch source so it survives
  rebuilding.
- Before generating paid audio, lock the exact main sentence. Any later main-
  sentence edit requires regenerating that audio.

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
- The front prominently shows the German target with optional headword and main-
  sentence audio controls. Paid audio currently exists for ranks 1–10.
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

- 2026-08-02 sentence-diversity rework is in progress. The policy-1 enrichment
  was confirmed to overuse reporting-clause quotations. A first policy-2
  mechanical experiment passed structural checks but failed semantic review
  because generic scene continuations could be unrelated to the authored
  sentence. It must not be released or voiced. No new ElevenLabs generation
  was started; paid coverage remains ranks 1-10 only.

- Ranks 1–1,250 have complete draft text and are pending human/native review.
- `dist/German-Core-Dual-Voice-Audio-Test-V8-10-Cards.apkg` is the current verified dual-voice audio package:
  ten notes/cards, stable note identities, 20 paid MP3s, and draft text.
- `tools/export_anki.py` builds rank-bounded packages and can include
  deterministic sentence-audio MP3s later; `tools/validate_apkg.py` inspects
  package structure without touching a user collection.
- Paid ElevenLabs generation now covers ranks 1–100: 100 headwords and 100 main
  sentences alternate between Marlene Lark and Markus. Ranks 1–10 were reused
  after receipt/text verification; ranks 11–100 added 180 MP3s. The 2026-08-02
  account snapshot showed 2,671 of 131,000 credits used and 128,329 remaining.
- `python tools/check_elevenlabs_credits.py` queries the live subscription and
  compares remaining credits with the exact current headword and main-sentence
  manifests. Multilingual v2 is budgeted at one credit per text character.
- The frequency PDF was identified as the copyrighted 2020 Routledge second
  edition by Erwin Tschirner and Jupp Möhring (315 PDF pages). Its ranking may be
  used as a private curriculum reference, but its definitions and examples must
  not be copied into public artifacts.
- PDF extraction succeeded for all ranks 1–5,009. The local parser dependency is in
  ignored `.vendor/`; extraction is slow but reproducible.
- The source `.apkg` and PDF have not been modified.
- The project is versioned on the public GitHub repository and deployed from
  `main`; preserve unrelated local worktree edits when committing scoped work.
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
6. Every validated audio milestone must also publish its downloadable `.apkg`
   and manifest-approved browser MP3s on the website; update the viewer coverage
   message and landing-page links in the same release.
7. Isolated headwords must never rely on automatic language detection. Generate
   them with a language-enforcement-capable model and `language_code: "de"`;
   verify both fields from receipts before packaging or website publishing.
8. Keep milestones small and public: commit and push text work in 50-100-card
   checkpoints and audio work in roughly 100-card checkpoints after validation.
9. Never hand-edit a generic finished flag. Run
   `python tools/build_completion_status.py`; completion is derived from the
   finalized contextual review and deterministic published audio files.

## Next action

Audio generation, receipt verification, and Anki packaging are complete through
rank 2,200. The package contains 2,200 notes/cards and 4,400 MP3s. The public
download remains the verified `v1600-audio` release until the 2,200-card package
is uploaded as a release asset.

The finalized canonical checkpoint reaches rank 2,500, while verified audio
reaches rank 2,200. ElevenLabs stopped during rank 2,201–2,250 generation with
19 credits remaining, so no partial browser-audio checkpoint was published.
Next, author and review new frequency-aligned source beginning at rank 2,501.
Ranks 2,401–2,500 continue through `build_batch_008.py`; ranks 2,501–3,000
use `build_batch_009.py`. Both builders reject any target that does not exactly
match `data/source/frequency-all-5009.jsonl` at its rank.
Batch builders support `--through` plus `--preserve-existing` for safe bounded
milestones.

Continue independent review and guarded merging above rank 100 before generating
more sentence audio. Ranks 1–100 are finalized under contextual sentence policy
3 and available as `dist/German-Core-Audio-0001-0100.apkg`; ranks 101–1,250
remain on policy 1 until their staged rewrites pass review.

Review the deterministic context expansions, replacing any merely serviceable
wrapper with a more organic example when possible. Then rebuild and publish the
1,250-card `.apkg` and browser demo. Continue authored cards at rank 1,251 while
preserving source order, sentence-design policy, explicit polysemy notes, and
global uniqueness. The reproducible sequence is: run all applicable batch
builders, `python tools/enrich_sentence_contexts.py`,
`python tools/build_curriculum_order.py`, `python tools/build_audio_manifest.py`,
and `python tools/validate_cards.py`. Commit and push every completed change.
