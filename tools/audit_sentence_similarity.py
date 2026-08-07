"""Deterministically flag repeated or near-duplicate German example patterns.

This is deliberately lexical rather than embedding-based: results are stable,
offline, explainable, and cheap enough to run before every paid audio batch.
It complements (but does not replace) semantic/native review.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
WORD_RE = re.compile(r"[a-zäöüß]+", re.IGNORECASE)


def normalize(text: str) -> list[str]:
    text = unicodedata.normalize("NFC", text).casefold()
    return WORD_RE.findall(text)


def features(tokens: list[str]) -> set[str]:
    result = {f"w:{token}" for token in tokens}
    result.update(
        "b:" + " ".join(tokens[index:index + 2])
        for index in range(len(tokens) - 1)
    )
    compact = " ".join(tokens)
    result.update(
        "c:" + compact[index:index + 5]
        for index in range(max(0, len(compact) - 4))
    )
    return result


def load_examples(start: int, end: int) -> list[dict]:
    examples = []
    for path in sorted(CANONICAL.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            card = json.loads(line)
            rank = card.get("frequency_rank")
            if not isinstance(rank, int) or not start <= rank <= end:
                continue
            pairs = [("main", card["german_sentence"])] + [
                (f"extra{index}", item["german"])
                for index, item in enumerate(card["extra_examples"], 1)
            ]
            for slot, sentence in pairs:
                tokens = normalize(sentence)
                examples.append({
                    "rank": rank,
                    "slot": slot,
                    "sentence": sentence,
                    "tokens": tokens,
                    "features": features(tokens),
                })
    return examples


def cosine(left: dict[str, float], right: dict[str, float]) -> float:
    common = left.keys() & right.keys()
    dot = sum(left[key] * right[key] for key in common)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


def audit(examples: list[dict], threshold: float, opening_limit: int) -> dict:
    document_frequency = Counter(
        feature for item in examples for feature in item["features"]
    )
    total = len(examples)
    vectors = []
    postings: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(examples):
        vector = {
            feature: math.log((total + 1) / (document_frequency[feature] + 1)) + 1
            for feature in item["features"]
        }
        vectors.append(vector)
        for feature in item["features"]:
            if document_frequency[feature] <= max(100, total // 20):
                postings[feature].append(index)

    candidates: set[tuple[int, int]] = set()
    for indexes in postings.values():
        for offset, left in enumerate(indexes):
            for right in indexes[offset + 1:]:
                if examples[left]["rank"] != examples[right]["rank"]:
                    candidates.add((left, right))

    similar = []
    for left, right in sorted(candidates):
        score = cosine(vectors[left], vectors[right])
        if score >= threshold:
            similar.append({
                "score": round(score, 4),
                "left": {key: examples[left][key] for key in ("rank", "slot", "sentence")},
                "right": {key: examples[right][key] for key in ("rank", "slot", "sentence")},
            })
    similar.sort(key=lambda item: (-item["score"], item["left"]["rank"], item["right"]["rank"]))

    openings: dict[str, list[dict]] = defaultdict(list)
    for item in examples:
        if len(item["tokens"]) >= 4:
            opening = " ".join(item["tokens"][:4])
            openings[opening].append({key: item[key] for key in ("rank", "slot", "sentence")})
    repeated_openings = [
        {"opening": opening, "count": len(items), "examples": items}
        for opening, items in openings.items() if len(items) >= opening_limit
    ]
    repeated_openings.sort(key=lambda item: (-item["count"], item["opening"]))
    return {
        "schema_version": 1,
        "example_count": len(examples),
        "similarity_threshold": threshold,
        "similar_pairs": similar,
        "opening_repeat_limit": opening_limit,
        "repeated_openings": repeated_openings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=5009)
    parser.add_argument("--threshold", type=float, default=0.82)
    parser.add_argument("--opening-limit", type=int, default=3)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on-findings", action="store_true")
    args = parser.parse_args()
    report = audit(load_examples(args.start, args.end), args.threshold, args.opening_limit)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(
        f"Audited {report['example_count']} examples: "
        f"{len(report['similar_pairs'])} similar pairs, "
        f"{len(report['repeated_openings'])} repeated openings."
    )
    return int(args.fail_on_findings and bool(
        report["similar_pairs"] or report["repeated_openings"]
    ))


if __name__ == "__main__":
    raise SystemExit(main())
