"""Apply explicitly reviewed staged rewrites to a compact batch source."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DELIMITER = " § "
SLOT_COLUMNS = {"main": (6, 7), "extra1": (8, 9), "extra2": (10, 11), "extra3": (12, 13)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch", type=Path)
    parser.add_argument("generation", type=Path)
    parser.add_argument("--accept-all-reviewed", action="store_true", required=True)
    args = parser.parse_args()
    batch = args.batch if args.batch.is_absolute() else ROOT / args.batch
    generation = args.generation if args.generation.is_absolute() else ROOT / args.generation
    payload = json.loads(generation.read_text(encoding="utf-8"))
    rewrites = {(item["frequency_rank"], item["slot"]): item for item in payload["rewrites"]}
    seen = set()
    output = []
    for raw in batch.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            output.append(raw)
            continue
        fields = raw.split(DELIMITER)
        if len(fields) != 14:
            raise SystemExit(f"rank field {fields[0]!r}: expected 14 columns, got {len(fields)}")
        rank = int(fields[0])
        for slot, columns in SLOT_COLUMNS.items():
            item = rewrites.get((rank, slot))
            if item:
                if item["semantic_id"].split(":")[-1] != str(rank):
                    raise SystemExit(f"semantic identity mismatch at rank {rank} {slot}")
                fields[columns[0]] = item["german"]
                fields[columns[1]] = item["english"]
                seen.add((rank, slot))
        output.append(DELIMITER.join(fields))
    missing = set(rewrites) - seen
    if missing:
        raise SystemExit(f"rewrites not found in source: {sorted(missing)}")
    batch.write_text("\n".join(output) + "\n", encoding="utf-8", newline="\n")
    print(f"Applied {len(seen)} reviewed rewrites to {batch.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
