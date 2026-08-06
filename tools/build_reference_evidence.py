"""Collect bounded, provenance-preserving corpus attestations for a rank range."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
DEFAULT_CORPUS = ROOT / "corpus" / "raw"
FREQUENCY_SOURCE = ROOT / "data" / "source" / "frequency-all-5009.jsonl"
TEXT_SUFFIXES = {".csv", ".json", ".jsonl", ".md", ".simple", ".src", ".tgt", ".tsv", ".txt", ".xml"}


def cards_between(start: int, end: int) -> list[dict]:
    cards = []
    for path in sorted(CANONICAL.glob("frequency-*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            card = json.loads(line)
            if start <= card["frequency_rank"] <= end:
                cards.append(card)
    by_rank = {card["frequency_rank"]: card for card in cards}
    if FREQUENCY_SOURCE.is_file():
        for line in FREQUENCY_SOURCE.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            rank = row["rank"]
            if start <= rank <= end and rank not in by_rank:
                by_rank[rank] = {"frequency_rank": rank, "target": row["headword"]}
    return [by_rank[rank] for rank in range(start, end + 1) if rank in by_rank]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-rank", type=int, required=True)
    parser.add_argument("--end-rank", type=int, required=True)
    parser.add_argument("--corpus-root", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--limit-per-card", type=int, default=20)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    cards = cards_between(args.start_rank, args.end_rank)
    targets = {
        re.sub(r"\s*\([^)]*\)\s*$", "", card["target"]).casefold(): card
        for card in cards
    }
    targets = {target: card for target, card in targets.items() if target}
    pattern = re.compile(
        r"(?<!\w)(?:" + "|".join(sorted((re.escape(value) for value in targets), key=len, reverse=True)) + r")(?!\w)",
        re.IGNORECASE,
    )
    evidence: dict[int, list[dict]] = defaultdict(list)
    for path in sorted(args.corpus_root.rglob("*")):
        if not path.is_file() or path.suffix.casefold() not in TEXT_SUFFIXES or ".git" in path.parts:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="strict").splitlines()
        except (UnicodeError, OSError):
            continue
        source_id = path.relative_to(args.corpus_root).parts[0]
        for line_no, line in enumerate(lines, 1):
            compact = " ".join(line.split())
            if not 20 <= len(compact) <= 500:
                continue
            for match in pattern.finditer(compact):
                card = targets[match.group(0).casefold()]
                rank = card["frequency_rank"]
                if len(evidence[rank]) < args.limit_per_card:
                    evidence[rank].append({
                        "source_id": source_id,
                        "path": path.relative_to(args.corpus_root).as_posix(),
                        "line": line_no,
                        "text": compact,
                    })
    rows = [{
        "frequency_rank": card["frequency_rank"],
        "target": card["target"],
        "attestation_count": len(evidence[card["frequency_rank"]]),
        "attestations": evidence[card["frequency_rank"]],
    } for card in cards]
    output = args.output or ROOT / "corpus" / "candidates" / f"evidence-{args.start_rank:04}-{args.end_rank:04}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    covered = sum(bool(row["attestations"]) for row in rows)
    print(f"Wrote evidence for {len(rows)} cards to {output}; {covered} have attestations.")


if __name__ == "__main__":
    main()
