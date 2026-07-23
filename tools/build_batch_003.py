"""Build independently authored, fully developed cards for ranks 51-200."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "canonical" / "frequency-0051-0200.jsonl"
DATA_FILES = (
    ROOT / "tools" / "batch_003_0051_0100.txt",
    ROOT / "tools" / "batch_003_0101_0150.txt",
    ROOT / "tools" / "batch_003_0151_0200.txt",
)


def read_entries() -> list[list[str]]:
    entries = []
    for path in DATA_FILES:
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line or line.startswith("#"):
                continue
            fields = [field.strip() for field in line.split("§")]
            if len(fields) != 14:
                raise ValueError(f"{path.name}:{line_no}: expected 14 fields, got {len(fields)}")
            entries.append(fields)
    return entries


def build() -> list[dict]:
    rows = []
    for fields in read_entries():
        (
            rank_text, target, pos, meaning, forms_text, note,
            main_de, main_en, extra1_de, extra1_en, extra2_de, extra2_en,
            extra3_de, extra3_en,
        ) = fields
        rank = int(rank_text)
        forms = [{"key_forms": forms_text}] if forms_text else []
        rows.append({
            "schema_version": 2,
            "semantic_id": f"de-DE:{pos.replace(' ', '-').replace('/', '-')}:"
                           f"{target}:{rank:04}",
            "sequence": 10000 + rank,
            "frequency_rank": rank,
            "target": target,
            "lemma": target,
            "sense_id": f"core-{rank:04}",
            "part_of_speech": pos,
            "meaning": meaning,
            "forms": forms,
            "german_sentence": main_de,
            "english_sentence": main_en,
            "literal_translation": "",
            "example_focus": "core uses",
            "extra_examples": [
                {"german": extra1_de, "english": extra1_en},
                {"german": extra2_de, "english": extra2_en},
                {"german": extra3_de, "english": extra3_en},
            ],
            "usage_note": note,
            "register": "neutral",
            "variety": "Germany Standard German",
            "sentence_audio": "",
            "text_status": "draft_complete_pending_human_review",
            "locked_fields": [],
            "created_for": "complete frequency curriculum",
        })
    return rows


def main() -> None:
    rows = build()
    expected = list(range(51, 201))
    actual = [row["frequency_rank"] for row in rows]
    if actual != expected:
        raise ValueError("Batch ranks must be consecutive from 51 through 200")
    OUT.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(f"Wrote {len(rows)} cards to {OUT}")


if __name__ == "__main__":
    main()
