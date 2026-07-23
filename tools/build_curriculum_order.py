"""Build a deterministic learning order from frequency cards and theme bundles."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLES = ROOT / "curriculum" / "bundles.json"
OUTPUT = ROOT / "data" / "curriculum" / "current-order.json"


def load_cards() -> list[dict]:
    cards = []
    for path in sorted((ROOT / "data" / "canonical").glob("frequency-*.jsonl")):
        cards.extend(
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    return sorted(cards, key=lambda card: card["frequency_rank"])


def member_key(member: dict) -> tuple[str, int | str]:
    if "frequency_rank" in member:
        return ("frequency_rank", member["frequency_rank"])
    return ("semantic_id", member["supplemental_id"])


def build() -> dict:
    config = json.loads(BUNDLES.read_text(encoding="utf-8"))
    cards = load_cards()
    by_rank = {card["frequency_rank"]: card for card in cards}
    by_id = {card["semantic_id"]: card for card in cards}
    claimed: set[tuple[str, int | str]] = set()
    active = []
    pending = []

    for bundle in config["bundles"]:
        resolved = []
        missing = []
        for member in bundle["members"]:
            key = member_key(member)
            if key in claimed:
                raise ValueError(f"Card reference appears in multiple bundles: {key}")
            claimed.add(key)
            card = (
                by_rank.get(key[1])
                if key[0] == "frequency_rank"
                else by_id.get(key[1])
            )
            if card is None:
                missing.append(member)
            else:
                resolved.append(card)
        if missing:
            pending.append({
                "unit_id": bundle["unit_id"],
                "title": bundle["title"],
                "available": len(resolved),
                "required": len(bundle["members"]),
                "missing": missing,
            })
        else:
            active.append((bundle, resolved))

    active_ids = {
        card["semantic_id"]
        for _bundle, resolved in active
        for card in resolved
    }
    base = [card for card in cards if card["semantic_id"] not in active_ids]
    insertions: dict[int, list[tuple[dict, list[dict]]]] = {}
    for bundle, resolved in active:
        insertions.setdefault(bundle["insert_after_frequency_rank"], []).append(
            (bundle, resolved)
        )

    ordered = []
    units = []
    for card in base:
        ordered.append((card, None))
        for bundle, resolved in insertions.get(card["frequency_rank"], []):
            start = len(ordered) + 1
            ordered.extend((member, bundle["unit_id"]) for member in resolved)
            units.append({
                "unit_id": bundle["unit_id"],
                "title": bundle["title"],
                "start": start,
                "end": len(ordered),
            })

    if len(ordered) != len(cards):
        raise ValueError("Curriculum order lost or duplicated cards")
    semantic_ids = [card["semantic_id"] for card, _unit_id in ordered]
    if len(semantic_ids) != len(set(semantic_ids)):
        raise ValueError("Curriculum order contains duplicate semantic IDs")

    return {
        "schema_version": 1,
        "card_count": len(ordered),
        "active_units": units,
        "pending_units": pending,
        "cards": [
            {
                "curriculum_order": index,
                "semantic_id": card["semantic_id"],
                "frequency_rank": card["frequency_rank"],
                "unit_id": unit_id,
            }
            for index, (card, unit_id) in enumerate(ordered, 1)
        ],
    }


def main() -> None:
    result = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {result['card_count']} ordered cards, "
        f"{len(result['active_units'])} active bundles, and "
        f"{len(result['pending_units'])} pending bundles to "
        f"{OUTPUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
