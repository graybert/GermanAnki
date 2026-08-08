"""Hydrate compact reviewed rewrite pairs with staged identity metadata."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("reviewed", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    paths = [path if path.is_absolute() else ROOT / path for path in (args.input, args.reviewed, args.output)]
    staged = json.loads(paths[0].read_text(encoding="utf-8"))
    reviewed = json.loads(paths[1].read_text(encoding="utf-8"))
    expected = {
        (card["frequency_rank"], slot): card["semantic_id"]
        for card in staged["cards"] for slot in card["rewrite_slots"]
    }
    hydrated = []
    seen = set()
    for item in reviewed["rewrites"]:
        key = (item["frequency_rank"], item["slot"])
        if key in seen or key not in expected:
            raise SystemExit(f"duplicate or unexpected rewrite {key}")
        seen.add(key)
        words = len(WORD_RE.findall(item["german"]))
        if not 9 <= words <= 20:
            raise SystemExit(f"{key}: German word count {words}, expected 9-20")
        if not item["english"].strip():
            raise SystemExit(f"{key}: empty English translation")
        hydrated.append({
            **item,
            "semantic_id": expected[key],
            "structure": item.get("structure", "contextualized_proposition"),
            "genre": item.get("genre", "general contemporary usage"),
            "confidence": item.get("confidence", "high"),
        })
    if seen != set(expected):
        raise SystemExit(f"coverage mismatch: missing {sorted(set(expected) - seen)}")
    payload = {"batch_id": staged["batch_id"], "rewrites": hydrated}
    paths[2].parent.mkdir(parents=True, exist_ok=True)
    paths[2].write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Hydrated {len(hydrated)} reviewed rewrites with complete staged coverage.")


if __name__ == "__main__":
    main()
