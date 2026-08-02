"""Validate canonical JSONL cards, including corpus-wide sentence uniqueness."""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüß]+")
REQUIRED = {
    "schema_version", "semantic_id", "sequence", "target", "lemma", "sense_id",
    "part_of_speech", "meaning", "forms", "german_sentence", "english_sentence",
    "extra_examples", "usage_note", "register", "variety", "text_status",
}


def normalized(sentence: str) -> str:
    return " ".join(sentence.casefold().strip().rstrip(".!?").split())


def main() -> None:
    paths = sorted((ROOT / "data" / "canonical").glob("*.jsonl"))
    source_path = ROOT / "data" / "source" / "frequency-all-5009.jsonl"
    source_headwords = {
        row["rank"]: row["headword"]
        for row in (
            json.loads(line)
            for line in source_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }
    errors: list[str] = []
    sentence_owners: dict[str, list[str]] = defaultdict(list)
    semantic_ids: set[str] = set()
    sequences: set[int] = set()
    frequency_ranks: dict[int, str] = {}
    sentence_design_versions: dict[int, int] = {}
    frequency_semantic_ids: set[str] = set()
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
                if isinstance(sid, str):
                    frequency_semantic_ids.add(sid)
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
            if frequency_rank is not None:
                design = card.get("sentence_design", {})
                policy_version = design.get("policy_version")
                if policy_version not in {1, 3}:
                    errors.append(
                        f"{label}: sentence-design policy must be pending v1 or finalized v3"
                    )
                else:
                    sentence_design_versions[frequency_rank] = policy_version
                if policy_version == 3:
                    contextual = design.get("contextual_rewrite", {})
                    if contextual.get("status") != "finalized":
                        errors.append(f"{label}: policy v3 is not contextually finalized")
                    if contextual.get("selection_seed") != "semantic-diversity-v3":
                        errors.append(f"{label}: policy v3 selection seed mismatch")
                    enriched_slots = design.get("enriched_slots", [])
                    rewritten = contextual.get("rewritten_slots", [])
                    retained = contextual.get("retained_policy1_slots", [])
                    if sorted([*rewritten, *retained]) != sorted(enriched_slots):
                        errors.append(
                            f"{label}: contextual rewritten/retained slots do not partition enriched_slots"
                        )
                    if contextual.get("selected") != bool(rewritten):
                        errors.append(
                            f"{label}: contextual selected flag does not match rewritten slots"
                        )
                    audit = contextual.get("slot_audit", {})
                    if set(audit) != set(rewritten):
                        errors.append(f"{label}: contextual slot audit mismatch")
                expected_source = source_headwords.get(frequency_rank)
                if card.get("source_headword") != expected_source:
                    errors.append(
                        f"{label}: source_headword {card.get('source_headword')!r} "
                        f"does not match rank {frequency_rank} source {expected_source!r}"
                    )
                word_counts = [len(WORD_RE.findall(sentence)) for _, sentence in examples]
                if any(count > 20 for count in word_counts):
                    errors.append(f"{label}: German example exceeds 20 words: {word_counts}")
                if sum(9 <= count <= 20 for count in word_counts) < 2:
                    errors.append(
                        f"{label}: fewer than two context-rich 9-20-word examples: {word_counts}"
                    )
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
        finalized_ranks = sorted(
            rank for rank, version in sentence_design_versions.items() if version == 3
        )
        if not finalized_ranks:
            errors.append("no contextually finalized policy-v3 rank prefix")
        else:
            cutoff = finalized_ranks[-1]
            if finalized_ranks != list(range(1, cutoff + 1)):
                errors.append("policy-v3 ranks are not a continuous prefix")
            pending_versions = {
                sentence_design_versions.get(rank) for rank in range(cutoff + 1, maximum_rank + 1)
            }
            if pending_versions - {1}:
                errors.append("ranks after the policy-v3 cutoff are not pending policy v1")
            recorded_cutoffs = {
                card_cutoff
                for path in paths
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()
                for card in [json.loads(line)]
                if card.get("sentence_design", {}).get("policy_version") == 3
                for card_cutoff in [
                    card.get("sentence_design", {})
                    .get("contextual_rewrite", {})
                    .get("finalized_through_rank")
                ]
            }
            if recorded_cutoffs != {cutoff}:
                errors.append(
                    f"policy-v3 finalized_through_rank values do not equal cutoff {cutoff}"
                )
    curriculum_path = ROOT / "data" / "curriculum" / "current-order.json"
    if curriculum_path.exists():
        curriculum = json.loads(curriculum_path.read_text(encoding="utf-8"))
        ordered_cards = curriculum.get("cards", [])
        ordered_ids = [entry.get("semantic_id") for entry in ordered_cards]
        ordered_positions = [
            entry.get("curriculum_order") for entry in ordered_cards
        ]
        if set(ordered_ids) != frequency_semantic_ids:
            errors.append(
                "curriculum order semantic IDs do not match frequency cards"
            )
        if len(ordered_ids) != len(set(ordered_ids)):
            errors.append("curriculum order contains duplicate semantic IDs")
        if ordered_positions != list(range(1, len(ordered_cards) + 1)):
            errors.append("curriculum_order values are not continuous from 1")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"Validated {count} cards and {len(sentence_owners)} unique German sentences across {len(paths)} files.")


if __name__ == "__main__":
    main()
