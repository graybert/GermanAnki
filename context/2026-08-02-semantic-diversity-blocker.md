# Semantic diversity rework — 2026-08-02

User review correctly identified that policy-1 long examples overuse a setup +
speaker + direct-quotation structure. The requested release target is ranks
1–1,250 with structurally diverse main and extra examples, followed by paid
dual-voice ElevenLabs generation for all 1,250 cards.

Audit results before revision:

- 1,250 frequency cards and 5,000 German examples.
- 399 main slots and 1,917 extra slots had been expanded by policy 1.
- Current ElevenLabs manifests contained 2,500 jobs and required about 84,105
  Multilingual-v2 characters.
- Live balance was 130,808 credits, so the run was affordable.

A mechanical policy-2 prototype showed why structural validation alone is not
enough: generic atmospheric continuations sometimes had no semantic connection
to the original example. Paid generation was stopped before any API calls.
Every replacement must instead be authored or generated from the whole card
context (target, sense, grammar note, and other examples), then checked for
meaning, translation, target inclusion, uniqueness, word count, and structural
distribution. The experimental corpus is not release-ready and must not be
voiced.

## Context-aware pilot

A 100-card pilot was split across five rank quintiles. Read-only Codex workers
use commit `940d9d5` for clean pre-enrichment cards and commit `7894d18` only
to identify policy-1-expanded slots. Workers return strict JSON and cannot edit
canonical files. The initial schema was rejected before inference because a
constant lacked an explicit JSON type; adding `type: integer` fixed it.

All three generation segments then returned complete results: 191 rewrites for
191 expected rank/slot pairs, with no missing or unexpected items. Structure
labels span narration, description, cause/consequence, contrast, procedural
language, genre scenes, questions, internal monologue, messages, and a small
amount of reported speech. This is materially more varied than policy 1.

Across the complete pilot, independent review accepted 160 of 191 candidates
unchanged, fixed 31, and rejected none. It found several 7–8-word candidates,
German
idiom/collocation problems, and four translation nuances. The review schema had
only `too_long`, so the reviewer used that label for short candidates; a
`too_short` label was added before further review. This shows that model review
must be paired with deterministic word counts and that worker self-confidence
is not an acceptance signal. No context non sequiturs, wrong senses, missing
targets, or formulaic-pattern failures were found in this first segment.
The other segments found one genuine wrong-sense error, two context non
sequiturs, and additional subtle translation/idiom issues; reviewers supplied
complete corrected pairs. The 16.2% correction rate proves that independent
review is essential even when generators claim high confidence. Prompt version
4 must emphasize deterministic minimum length, exact bilingual proposition
matching, and conservative idiomatic word choice before scaling.

## First 100 finalized and voiced

Independent review of the four boundary batches covering ranks 1–100 processed
177 candidates: 142 accepted, 35 fixed, and none rejected. The guarded merge
applied 141 selected slots within ranks 1–100 and intentionally retained 37
policy-1 quotation slots. Four cards (27, 39, 50, 58) initially failed the
two-rich-example invariant; a focused generator and a separate reviewer supplied
four accepted replacements. The merge then passed the full 1,251-note / 5,008-
unique-example validator without weakening any gate.

The rebuilt ranks 1–100 manifests selected 200 jobs and 5,268 raw characters.
Receipt validation allowed the existing 20 ranks-1–10 MP3s to be reused. The
paid no-overwrite run generated 180 new files and reported 2,706 charged credits.
The subsequent subscription snapshot increased total account usage from 192 to
2,671 (a 2,479-credit delta), so aggregate job-reported charges and subscription
usage do not exactly agree; retain both measurements rather than silently
normalizing them. The account had 128,329 credits remaining.

`tools/verify_generated_audio.py` confirmed all 200 files against their latest
receipts, exact text, semantic IDs, kind, alternating voice, model, output
format, and byte counts. `ffprobe` was unavailable, so codec decoding was not
independently probed. `dist/German-Core-Audio-0001-0100.apkg` contains 100 notes,
100 cards, and 200 media files; isolated current-Anki import and rendering pass.

## Isolated-headword language failure and fix

Human listening found that isolated `also`, `all`, and `so` could be pronounced
with English phonology even though the same voices pronounced them correctly
inside German sentences. The spelling-only requests did not provide enough
language context. ElevenLabs documents that `language_code` is ignored by
`eleven_multilingual_v2`, so merely adding `de` to the old requests would have
created false confidence.

The durable policy now separates job types: sentences use Multilingual v2;
every isolated headword uses `eleven_flash_v2_5` with `language_code: "de"`.
Both model and language code are written to receipts and enforced by the audio
verifier. Three diagnostic requests (`so`, `all`, `also`) proved the API
accepted the forced-German configuration. All 100 headwords were then
regenerated uniformly rather than relying on an incomplete blacklist of
English-looking spellings. ElevenLabs reported 114 credits for the 100
replacements (399 raw characters). Future headword generation without explicit
German enforcement must fail release verification.
