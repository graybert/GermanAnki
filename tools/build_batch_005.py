"""Build fully developed frequency cards for ranks 501-1000."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
START = 501
END = 1000
SOURCE = ROOT / "data" / "source" / "frequency-all-5009.jsonl"
OUT = ROOT / "data" / "canonical" / "frequency-0501-1000.jsonl"
DATA_FILES = tuple(
    ROOT / "tools" / f"batch_005_{start:04}_{start + 49:04}.txt"
    for start in range(START, END + 1, 50)
)


def source_entries() -> dict[int, dict]:
    return {
        row["rank"]: row
        for row in (
            json.loads(line)
            for line in SOURCE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def read_entries() -> list[list[str]]:
    entries = []
    for path in DATA_FILES:
        if not path.exists():
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line or line.startswith("#"):
                continue
            fields = [field.strip() for field in line.split("§")]
            if len(fields) != 14:
                raise ValueError(f"{path.name}:{line_no}: expected 14 fields, got {len(fields)}")
            entries.append(fields)
    return entries


def build(through: int | None = None) -> list[dict]:
    source = source_entries()
    rows = []
    for fields in read_entries():
        (
            rank_text, target, pos, meaning, forms_text, note,
            main_de, main_en, extra1_de, extra1_en, extra2_de, extra2_en,
            extra3_de, extra3_en,
        ) = fields
        rank = int(rank_text)
        if through is not None and rank > through:
            continue
        expected = source[rank]["headword"]
        if target != expected:
            raise ValueError(f"Rank {rank}: target {target!r} does not match source {expected!r}")
        examples_by_slot = {
            "main": main_de,
            "extra1": extra1_de,
            "extra2": extra2_de,
            "extra3": extra3_de,
        }
        rich_slots = [
            slot
            for slot, sentence in examples_by_slot.items()
            if 9 <= len(sentence.rstrip(".!?").split()) <= 20
        ]
        rows.append({
            "schema_version": 2,
            "semantic_id": f"de-DE:{pos.replace(' ', '-').replace('/', '-')}:{target}:{rank:04}",
            "sequence": 10000 + rank,
            "frequency_rank": rank,
            "target": target,
            "lemma": target,
            "sense_id": f"core-{rank:04}",
            "part_of_speech": pos,
            "meaning": meaning,
            "forms": [{"key_forms": forms_text}] if forms_text else [],
            "german_sentence": main_de,
            "english_sentence": main_en,
            "literal_translation": "",
            "example_focus": "core and contrasting uses",
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
            "sentence_design": {
                "policy_version": 1,
                "rich_example_minimum": 2,
                "rich_word_range": [9, 20],
                "enriched_slots": rich_slots,
            },
            "source_headword": expected,
        })
    ranks = [row["frequency_rank"] for row in rows]
    if ranks and ranks != list(range(START, START + len(ranks))):
        raise ValueError(f"Authored ranks must be consecutive from {START}")
    return rows


def preserve_existing(rows: list[dict]) -> list[dict]:
    """Keep already-published records while appending a bounded milestone."""
    if not OUT.exists():
        return rows
    existing = {
        row["frequency_rank"]: row
        for row in (
            json.loads(line)
            for line in OUT.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }
    return [existing.get(row["frequency_rank"], row) for row in rows]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-through", type=int, default=START - 1)
    parser.add_argument(
        "--through",
        type=int,
        help="write only authored cards through this rank",
    )
    parser.add_argument(
        "--preserve-existing",
        action="store_true",
        help="retain existing canonical records while appending later ranks",
    )
    args = parser.parse_args()
    if args.through is not None and not START <= args.through <= END:
        raise ValueError(f"--through must be between {START} and {END}")
    rows = build(args.through)
    if args.preserve_existing:
        rows = preserve_existing(rows)
    if args.require_through >= START:
        expected_count = args.require_through - START + 1
        if len(rows) != expected_count:
            raise ValueError(
                f"Expected {expected_count} cards through rank {args.require_through}, "
                f"found {len(rows)}"
            )
    OUT.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(f"Wrote {len(rows)} cards through rank {START - 1 + len(rows)} to {OUT}")


if __name__ == "__main__":
    main()
