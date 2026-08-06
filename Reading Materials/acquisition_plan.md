# Acquisition plan

## 1. Target composition

Use quotas at the **filtered reference-corpus** stage, not the raw-download stage.

| Slice | Target share | Purpose |
|---|---:|---|
| Contemporary authentic Germany written prose | 45–55% | General usage, collocations, syntax, polysemy |
| Official/practical/professional German | 15–20% | Forms, procedures, workplace, customer service, civic life |
| Spoken or transcript-aligned German | 15–20% | Questions, particles, ellipsis, requests, disagreement, narration |
| Native-reviewed learner material | 10–15% | Reliable A1–B2 coverage and controlled communicative functions |
| Advanced academic/scientific/technical | 10–15% | C1 syntax, terminology, evidence, hedging and formal argument |
| Austrian + Swiss Standard German | 5–8% combined | Regional awareness without dominating Germany Standard German |
| Historical/creative specialty slice | 1–3% | Narrative and stylistic breadth, always year/register labeled |

The percentages overlap conceptually because a source can be both spoken and professional; enforce quotas using primary labels and monitor secondary labels.

## 2. Download order

### Wave 1 — maximum breadth per unit of effort

1. Leipzig 1M News, 1M Web and 1M Wikipedia sentence packages.
2. German Wikipedia, Wikivoyage and Wikibooks dumps.
3. Bundestag XML for the 19th–21st legislative terms and a selective current-law XML set.
4. Clone DEPlain, Simple German Corpus, DWIE and PoTeC.
5. Download the official PDFs/transcripts from DW Nicos Weg, Top-Thema and Video-Thema; add Goethe/vhs downloadable materials.
6. Download BAMF orientation material, Verbraucherzentrale model letters and a cross-sector BERUFENET sample.

### Wave 2 — topic and register completion

1. gesund.bund patient information, RKI expert guidance and GMS German articles.
2. UBA reports, Destatis releases, SSOAR and peDOCS licence-filtered academic documents.
3. OPUS EMEA, TED2020, Europarl and software localization; use hard caps.
4. Recent Austrian and Swiss parliamentary samples.
5. PlainMedScale after reviewing its new release licence/source conditions.

### Wave 3 — controlled supplements

1. OpenSubtitles only after a strict filter pipeline.
2. Small year-labeled TextGrid selection for narrative/dialogue.
3. Restricted/request-only GGPONC and GermaParl only when their terms fit the project.

## 3. Repo folder layout

```text
corpus/
  raw/<source_id>/                 # untouched downloads; excluded from Git
  extracted/<source_id>/           # extracted documents, still source-specific
  normalized/<source_id>/          # normalized JSONL, never source-merged blindly
  metadata/<source_id>/            # licence snapshot, URLs, checksums, acquisition log
  candidates/                      # filtered sentence candidates
  indexes/                         # lemma/collocation/valency indexes
  manifests/                       # copied manifest versions
  logs/
```

Recommended normalized JSONL record:

```json
{
  "sentence_id": "source_id:document_id:paragraph:sentence",
  "text": "...",
  "left_context": "...",
  "right_context": "...",
  "source_id": "...",
  "document_id": "...",
  "url": "...",
  "title": "...",
  "date": "YYYY-MM-DD",
  "speaker": null,
  "genre": ["news"],
  "topics": ["economy"],
  "register": "neutral_journalistic",
  "cefr_estimate": "B2",
  "variety": "DE",
  "modality": "written",
  "translated": false,
  "rights_status": "internal_reference_only",
  "extractor_version": "..."
}
```

## 4. Quality pipeline

1. Extract documents and paragraphs before sentence segmentation; preserve speaker turns.
2. Run German language identification and reject mixed-language/navigation fragments.
3. Reject sentences that are incomplete, mostly punctuation, mostly names/numbers, menu fragments, code, citation lists or malformed OCR.
4. Normalize Unicode and whitespace, but retain German quotation marks, apostrophes and meaningful punctuation.
5. Exact- and near-deduplicate within and across sources. Keep a provenance list when duplicates occur.
6. Label likely translation/subtitle/localization text and cap it separately.
7. Score sentence completeness, naturalness, contextual sufficiency, lexical usefulness and source trust.
8. Assign genre/topic/register/variety/modality and a probabilistic CEFR estimate.
9. Index lemmas, dependency relations, separable-prefix verbs, prepositional complements, case frames, compounds, collocations and multiword expressions.
10. For every target lemma, diversify by sense, part of speech, construction, register, sentence type, topic and source family.

## 5. Sentence-selection constraints for the Anki generator

- Require at least three independent source families for high-frequency polysemous words.
- Prefer attested collocations and valency patterns; validate uncertain government with DWDS/DeReKo and reputable dictionaries.
- Do not copy source sentences into the deck automatically. Use the corpus as evidence/context, then generate or adapt and perform a second native-quality review.
- Keep examples self-contained enough for a card but not semantically empty.
- Balance sentence lengths and avoid making advanced words appear only in legal/academic prose.
- Tag regional examples and never silently teach Austrian/Swiss wording as universal Germany usage.
- Maintain a blacklist of boilerplate, sensational subtitle lines, unsafe personal data, malformed OCR and outdated/historical usage.

## 6. Quantitative acceptance gates

Before calling coverage adequate, require:

- at least 90% of the 5,009 lemmas with 20+ candidate attestations;
- at least 75% with candidates from 3+ source families;
- all common verbs checked for transitivity, governed case/preposition and separability;
- all high-frequency polysemous words represented by multiple senses;
- no single source family above 20% of selected card evidence;
- translated/subtitle/localization material below 15% of final evidence unless explicitly tagged;
- AT+CH combined near 5–8%, with Germany Standard German dominant;
- manual review samples for every source and every automated quality bucket.
