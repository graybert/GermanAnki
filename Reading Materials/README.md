# German Reference Corpus Acquisition Bundle

This bundle is a repo-ready source manifest and acquisition scaffold for a German Anki example-sentence system. It contains **58 verified source entries** spanning contemporary Germany-dominant Standard German, controlled CEFR material, official/public-service prose, news, speech transcripts, science, technology, health, academic writing, limited DACH regional material, and carefully bounded creative/historical sources.

## What is included

- `manifests/source_manifest.csv` — human-readable manifest with every requested source field.
- `manifests/source_manifest.json` — the same manifest for scripts/agents.
- `manifests/coverage_matrix.csv` — current strengths, weak areas and gap-filling actions.
- `manifests/acquisition_queue.csv` — ordered acquisition workstreams.
- `docs/source_catalog.md` — readable source-by-source catalog with every requested field.
- `docs/coverage_matrix.md` — readable rendering of the coverage matrix.
- `docs/acquisition_plan.md` — concrete corpus mix, folder design, filtering and QA plan.
- `docs/licensing_and_provenance.md` — rules for keeping restricted/copyrighted material out of Git.
- `tools/acquire.py` — Windows/macOS/Linux helper that creates directories, clones open repositories, downloads Wikimedia dumps, and produces link/command queues for manual or restricted sources.
- `tools/inventory.py` — inventories downloaded files with size and SHA-256 hashes.

## First run on Windows PowerShell

```powershell
cd path\to\your\repo
Expand-Archive german_reference_corpus_bundle.zip -DestinationPath corpus_tools
cd corpus_tools
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python tools\acquire.py init --root ..\corpus
python tools\acquire.py list --tier 1
python tools\acquire.py fetch deplain simple_german_corpus dwie potec --root ..\corpus
python tools\acquire.py fetch dewiki_dump dewikivoyage_dump dewikibooks_dump --root ..\corpus
python tools\acquire.py queue --tier 1 --root ..\corpus
python tools\inventory.py ..\corpus
```

The downloader deliberately does **not** blindly mirror websites or bypass authenticated/restricted access. It downloads only explicit open files/repositories and creates a queue for sources that require manual selection, terms review, an account, or an access request.

## Recommended raw-corpus target

Start with 5–20 million raw sentences, then filter to roughly 1–3 million diverse candidates and retain 250,000–750,000 high-quality reference sentences. This is intentionally much larger than 5,009 cards: the value comes from having multiple senses, registers, valency patterns, collocations and contexts for every lemma rather than one sentence per word.

## Non-negotiable metadata

Every extracted sentence should retain `source_id`, document URL/ID, title, date, author/speaker where available, paragraph/speaker-turn context, genre, topic, register, estimated CEFR, German variety, modality, translation status, rights status and extraction version. Never merge raw text without provenance.
