"""Stage structurally necessary contextual rewrites from a compact batch file.

The output is deterministic and read-only with respect to canonical card data.
It selects the longest sub-nine-word examples until each card would have two
examples in the configured 9-20-word rich range.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)
DELIMITER = " § "
SLOTS = (("main", 6, 7), ("extra1", 8, 9), ("extra2", 10, 11), ("extra3", 12, 13))


def count(text: str) -> int:
    return len(WORD_RE.findall(text))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    batch = args.batch if args.batch.is_absolute() else ROOT / args.batch
    output = args.output if args.output.is_absolute() else ROOT / args.output
    cards = []
    for raw in batch.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        fields = raw.split(DELIMITER)
        if len(fields) != 14:
            raise SystemExit(f"expected 14 fields, found {len(fields)}")
        rank = int(fields[0])
        examples = {
            slot: {"german": fields[de], "english": fields[en], "word_count": count(fields[de])}
            for slot, de, en in SLOTS
        }
        rich = sum(9 <= item["word_count"] <= 20 for item in examples.values())
        choices = sorted(
            (slot for slot, item in examples.items() if item["word_count"] < 9),
            key=lambda slot: (-examples[slot]["word_count"], slot),
        )
        rewrite_slots = choices[: max(0, 2 - rich)]
        if rewrite_slots:
            cards.append({
                "frequency_rank": rank,
                "semantic_id": f"de-DE:{fields[2].replace(' ', '-').replace('/', '-')}:{fields[1]}:{rank:04}",
                "target": fields[1],
                "part_of_speech": fields[2],
                "meaning": fields[3],
                "forms": fields[4],
                "usage_note": fields[5],
                "examples": examples,
                "rewrite_slots": rewrite_slots,
            })
    payload = {
        "schema_version": 1,
        "batch_id": f"rewrite-{cards[0]['frequency_rank']:04}-{cards[-1]['frequency_rank']:04}-v1" if cards else "empty",
        "source": str(batch.relative_to(ROOT)).replace("\\", "/"),
        "card_count": len(cards),
        "slot_count": sum(len(card["rewrite_slots"]) for card in cards),
        "cards": cards,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Staged {payload['card_count']} cards and {payload['slot_count']} slots in {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
