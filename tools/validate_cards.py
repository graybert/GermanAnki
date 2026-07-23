"""Validate canonical JSONL cards, including corpus-wide sentence uniqueness."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "schema_version", "semantic_id", "sequence", "target", "lemma", "sense_id",
    "part_of_speech", "meaning", "forms", "german_sentence", "english_sentence",
    "extra_examples", "usage_note", "register", "variety", "text_status",
}


def normalized(sentence: str) -> str:
    return " ".join(sentence.casefold().strip().rstrip(".!?").split())


def main() -> None:
    paths = sorted((ROOT / "data" / "canonical").glob("*.jsonl"))
    errors: list[str] = []
    sentence_owners: dict[str, list[str]] = defaultdict(list)
    semantic_ids: set[str] = set()
    sequences: set[int] = set()
    frequency_ranks: dict[int, str] = {}
    count = 0
    for path in paths:
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            count += 1
            label = f"{path.name}:{line_no}"
            try:
                card = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{label}: invalid JSON: {exc}")
                continue
            missing = sorted(REQUIRED - card.keys())
            if missing:
                errors.append(f"{label}: missing {', '.join(missing)}")
            sid = card.get("semantic_id")
            if sid in semantic_ids:
                errors.append(f"{label}: duplicate semantic_id {sid}")
            semantic_ids.add(sid)
            sequence = card.get("sequence")
            if sequence in sequences:
                errors.append(f"{label}: duplicate sequence {sequence}")
            sequences.add(sequence)
            frequency_rank = card.get("frequency_rank")
            if frequency_rank is not None:
                if not isinstance(frequency_rank, int) or frequency_rank < 1:
                    errors.append(f"{label}: invalid frequency_rank {frequency_rank!r}")
                elif frequency_rank in frequency_ranks:
                    errors.append(
                        f"{label}: duplicate frequency_rank {frequency_rank}; "
                        f"first used by {frequency_ranks[frequency_rank]}"
                    )
                else:
                    frequency_ranks[frequency_rank] = label
            extras = card.get("extra_examples", [])
            if len(extras) != 3 and frequency_rank is not None:
                errors.append(
                    f"{label}: frequency card must have exactly 3 extra examples"
                )
            if not card.get("english_sentence", "").strip():
                errors.append(f"{label}: empty main English translation")
            for i, example in enumerate(extras, 1):
                if not example.get("english", "").strip():
                    errors.append(f"{label}: empty extra {i} English translation")
            examples = [("main", card.get("german_sentence", ""))]
            examples += [
                (f"extra {i}", ex.get("german", ""))
                for i, ex in enumerate(extras, 1)
            ]
            for kind, sentence in examples:
                if not sentence:
                    errors.append(f"{label}: empty {kind} German sentence")
                else:
                    sentence_owners[normalized(sentence)].append(f"{label} {kind}")
    for sentence, owners in sentence_owners.items():
        if len(owners) > 1:
            errors.append(f"duplicate German sentence '{sentence}': {'; '.join(owners)}")
    if frequency_ranks:
        maximum_rank = max(frequency_ranks)
        missing_ranks = sorted(set(range(1, maximum_rank + 1)) - frequency_ranks.keys())
        if missing_ranks:
            errors.append(
                "frequency ranks are not continuous through "
                f"{maximum_rank}: missing {missing_ranks}"
            )
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"Validated {count} cards and {len(sentence_owners)} unique German sentences across {len(paths)} files.")


if __name__ == "__main__":
    main()
