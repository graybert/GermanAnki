#!/usr/bin/env python3
"""Inventory acquired corpus files with stable paths, sizes, and SHA-256 hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    rows = []
    for path in sorted((root / "raw").rglob("*")):
        if path.is_file() and ".git" not in path.parts:
            rows.append({
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            })
    output = root / "metadata" / "inventory.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(f"Inventoried {len(rows)} files ({sum(row['bytes'] for row in rows)} bytes) in {output}")


if __name__ == "__main__":
    main()
