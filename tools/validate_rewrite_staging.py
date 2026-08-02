"""Validate a generated rewrite batch and its independent review."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)
SPEECH_STRUCTURES = {"direct_speech", "reported_speech"}


def key(item: dict) -> tuple[int, str]:
    return item["frequency_rank"], item["slot"]


def normalized(text: str) -> str:
    return " ".join(text.casefold().strip().rstrip(".!?").split())


def indexed(items: list[dict], label: str, errors: list[str]) -> dict[tuple[int, str], dict]:
    result = {}
    for item in items:
        item_key = key(item)
        if item_key in result:
            errors.append(f"duplicate {label} key: {item_key}")
        result[item_key] = item
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("generation", type=Path)
    parser.add_argument("review", type=Path)
    parser.add_argument("--max-structure-share", type=float, default=0.25)
    parser.add_argument("--max-speech-share", type=float, default=0.15)
    args = parser.parse_args()

    generation = json.loads(args.generation.read_text(encoding="utf-8-sig"))
    review = json.loads(args.review.read_text(encoding="utf-8-sig"))
    errors: list[str] = []
    rewrites = indexed(generation.get("rewrites", []), "generation", errors)
    reviews = indexed(review.get("reviews", []), "review", errors)
    missing = sorted(rewrites.keys() - reviews.keys())
    unexpected = sorted(reviews.keys() - rewrites.keys())
    if missing:
        errors.append(f"missing reviews: {missing}")
    if unexpected:
        errors.append(f"reviews without candidates: {unexpected}")

    final_sentences: dict[str, tuple[int, str]] = {}
    decisions: Counter[str] = Counter()
    issues: Counter[str] = Counter()
    structures = Counter(item.get("structure", "") for item in rewrites.values())
    for item_key in sorted(rewrites.keys() & reviews.keys()):
        candidate, assessment = rewrites[item_key], reviews[item_key]
        decision = assessment.get("decision")
        decisions[decision] += 1
        issues.update(assessment.get("issues", []))
        if decision == "accept":
            german, english = candidate.get("german", ""), candidate.get("english", "")
            if assessment.get("corrected_german") or assessment.get("corrected_english"):
                errors.append(f"accepted review has correction text: {item_key}")
        elif decision == "fix":
            german = assessment.get("corrected_german", "")
            english = assessment.get("corrected_english", "")
            if not german.strip() or not english.strip():
                errors.append(f"fix lacks corrected pair: {item_key}")
        elif decision == "reject":
            errors.append(f"rejected candidate has no publishable final value: {item_key}")
            continue
        else:
            errors.append(f"unknown decision {decision!r}: {item_key}")
            continue

        count = len(WORD_RE.findall(german))
        if not 9 <= count <= 20:
            errors.append(f"final German word count {count} outside 9-20: {item_key}")
        if not english.strip():
            errors.append(f"empty final English: {item_key}")
        sentence_key = normalized(german)
        if sentence_key in final_sentences:
            errors.append(f"duplicate final German: {final_sentences[sentence_key]} and {item_key}")
        final_sentences[sentence_key] = item_key

    total = len(rewrites)
    if total:
        for structure, count in sorted(structures.items()):
            share = count / total
            if share > args.max_structure_share:
                errors.append(f"structure {structure!r} share {share:.1%} exceeds {args.max_structure_share:.1%}")
        speech_share = sum(structures[name] for name in SPEECH_STRUCTURES) / total
        if speech_share >= args.max_speech_share:
            errors.append(f"direct/reported speech share {speech_share:.1%} is not below {args.max_speech_share:.1%}")

    print(f"Generation prompt version: {generation.get('prompt_version')}")
    print(f"Candidates: {len(rewrites)}; reviews: {len(reviews)}; final unique: {len(final_sentences)}")
    print(f"Decisions: {dict(sorted(decisions.items()))}")
    print(f"Issues: {dict(sorted(issues.items()))}")
    print(f"Structures: {dict(sorted(structures.items()))}")
    if errors:
        raise SystemExit("\n".join(errors))
    print("Rewrite staging validation passed.")


if __name__ == "__main__":
    main()
