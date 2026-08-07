"""Merge an explicitly reviewed rewrite artifact and finalize a rank checkpoint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"


def set_slot(card: dict, slot: str, german: str, english: str) -> None:
    if slot == "main":
        card["german_sentence"], card["english_sentence"] = german, english
        return
    index = int(slot.removeprefix("extra")) - 1
    card["extra_examples"][index] = {"german": german, "english": english}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("generation", type=Path)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--accept-all-reviewed", action="store_true", required=True)
    args = parser.parse_args()
    generation = args.generation if args.generation.is_absolute() else ROOT / args.generation
    rewrites = json.loads(generation.read_text(encoding="utf-8"))["rewrites"]
    by_rank: dict[int, list[dict]] = {}
    for item in rewrites:
        rank = item["frequency_rank"]
        if not args.start <= rank <= args.end:
            raise SystemExit(f"rewrite rank {rank} outside requested checkpoint")
        by_rank.setdefault(rank, []).append(item)

    changed = 0
    covered = set()
    for path in sorted(CANONICAL.glob("frequency-*.jsonl")):
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        touched = False
        for card in rows:
            rank = card.get("frequency_rank")
            if not isinstance(rank, int) or rank > args.end:
                continue
            design = card.setdefault("sentence_design", {})
            contextual = design.setdefault("contextual_rewrite", {})
            if args.start <= rank <= args.end:
                for item in by_rank.get(rank, []):
                    if item["semantic_id"] != card["semantic_id"]:
                        raise SystemExit(f"semantic identity mismatch at rank {rank}")
                    set_slot(card, item["slot"], item["german"], item["english"])
                    changed += 1
                covered.add(rank)
                design["policy_version"] = 3
                contextual.update({
                    "status": "finalized",
                    "finalized_through_rank": args.end,
                    "selection_seed": "semantic-diversity-v3",
                    "selected": bool(by_rank.get(rank)),
                    "rewritten_slots": [item["slot"] for item in by_rank.get(rank, [])],
                    "retained_policy1_slots": [],
                    "slot_audit": {
                        item["slot"]: {
                            "review_decision": "accept",
                            "generation_batch": json.loads(generation.read_text(encoding="utf-8"))["batch_id"],
                            "structure": item["structure"],
                            "genre": item["genre"],
                            "confidence": item["confidence"],
                        } for item in by_rank.get(rank, [])
                    },
                })
            elif contextual.get("status") == "finalized":
                contextual["finalized_through_rank"] = args.end
            touched = True
        if touched:
            path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8", newline="\n")
    expected = set(range(args.start, args.end + 1))
    if covered != expected:
        raise SystemExit(f"checkpoint coverage mismatch: {sorted(expected - covered)}")
    print(f"Finalized ranks {args.start}-{args.end} with {changed} reviewed rewrites.")


if __name__ == "__main__":
    main()
