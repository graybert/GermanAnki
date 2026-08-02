# Sentence diversity, source-order audit, and audio budget

Date: 2026-08-01 (America/Los_Angeles)

## Decisions

- Short, high-frequency utterances remain valuable and should not all be
  expanded.
- Every frequency card must nevertheless contain at least two context-rich
  examples of 9–20 words; no German example may exceed 20 words.
- Main sentences should vary substantially because they receive paid audio and
  carry much of the deck's incidental grammar exposure.
- Ranks 1–10 retain their existing main sentences because matching paid audio
  is already committed.
- Contexts should span everyday dialogue, family, education, work, reporting,
  interviews, culture, nature, public information, and literary narration.

`tools/enrich_sentence_contexts.py` implements the minimum deterministic
expansion needed after authored batch data is rebuilt. Existing examples that
already satisfy the policy remain unchanged. The generated context frames use
stable hashing, subordinate clauses, varied speakers/actions, and topic cues.
They are draft scaffolding and remain candidates for organic native-speaker
rewrites.

## Source-order verification

A fresh independent extraction of the ranked PDF section produced all 5,009
rows and matched `data/source/frequency-all-5009.jsonl` exactly. Canonical ranks
1–1,250 are continuous and occur in the same order. Twelve visible targets
normalize source labels that include colloquial variants, trailing punctuation,
or inflection shorthand; no rank is reordered or replaced.

## ElevenLabs accounting

`tools/check_elevenlabs_credits.py` calls `GET /v1/user/subscription` with the
ignored local key and compares the live remaining balance with exact manifest
character totals. It prints no secret. The 2026-08-01 account snapshot was an
active Creator plan with 192 of 131,000 credits used and 130,808 remaining.
Multilingual v2 costs one credit per input character, subject to any voice-
specific multiplier reported by ElevenLabs.

Paid generation must wait until the main-sentence text is locked. Rebuild
`data/audio/main-sentence-manifest.jsonl` after every main-sentence revision.
