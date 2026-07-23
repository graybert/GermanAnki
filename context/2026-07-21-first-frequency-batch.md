# First frequency batch complete — 2026-07-21

The frequency list was located on PDF page 20 and ranks 1–500 were extracted to
`data/source/frequency-first-500.jsonl`. Only rank, headword, coarse source POS,
and source page are retained; copyrighted definitions and examples are omitted.

Ranks 1–10 now have independently authored complete drafts in
`data/canonical/frequency-0001-0010.jsonl`. Each contains morphology or governed
case where relevant, one main example, three extra examples, natural English
translations, a usage note, register/variety metadata, and review status. These
are drafts pending human review, not locked or release-ready cards.

The global validator checked 11 records (including the earlier `wer` prototype)
and 48 unique German sentences. It found no duplicate sentences, semantic IDs,
or sequences. Frequency-card sequence IDs temporarily use 10001+ so the rank-1
card does not collide with the prototype's existing sequence 1; frequency rank
is stored separately and remains authoritative.

Next: review this batch, then author ranks 11 onward. Maintain distinct sentence
scenarios across the full corpus, not merely distinct wording within each card.
