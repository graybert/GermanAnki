"""Strictly merge reviewed contextual rewrites into a policy-1 baseline.

The merge is incremental by rank. It never treats the current canonical files
as source material: every output file is reconstructed from commit 7894d18,
then reviewed rewrites are applied through the requested cutoff.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from prepare_contextual_rewrites import (
    CLEAN_COMMIT,
    ENRICHED_COMMIT,
    SELECTION_SEED,
    examples,
    git_cards,
    selected_semantic_ids,
    stable_hash,
)


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "tmp" / "contextual-rewrites" / "ranks-0001-1250"
CANONICAL = ROOT / "data" / "canonical"
FOCUSED_OVERRIDE_BATCHES = {
    "rewrite-0001-0100-richness-override-v1": {
        (27, "main"),
        (39, "extra2"),
        (50, "extra1"),
        (58, "extra1"),
    },
    "rewrite-0001-0500-rejected-override-v1": {
        (240, "extra3"),
    },
    "rewrite-0001-0500-identity-override-v1": {
        (237, "main"),
        (237, "extra1"),
    },
    "rewrite-0001-0500-identity-override-v2": {
        (238, "extra2"),
        (238, "extra3"),
        (456, "main"),
        (456, "extra2"),
        (460, "extra1"),
        (460, "extra2"),
        (462, "main"),
    },
    "rewrite-0001-0500-richness-override-v2": {
        (112, "extra2"),
        (143, "extra1"),
        (405, "main"),
    },
}
FOCUSED_OVERRIDE_KEYS = set().union(*FOCUSED_OVERRIDE_BATCHES.values())


class MergeError(RuntimeError):
    pass


def git_canonical_files() -> dict[str, list[dict]]:
    listing = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ENRICHED_COMMIT, "data/canonical"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.splitlines()
    result: dict[str, list[dict]] = {}
    for repository_path in listing:
        if not repository_path.endswith(".jsonl"):
            continue
        content = subprocess.run(
            ["git", "show", f"{ENRICHED_COMMIT}:{repository_path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout
        result[Path(repository_path).name] = [
            json.loads(line) for line in content.splitlines() if line.strip()
        ]
    if not result:
        raise MergeError(f"no canonical JSONL files found at {ENRICHED_COMMIT}")
    return result


def load_json(path: Path) -> dict:
    if not path.exists():
        raise MergeError(f"missing {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise MergeError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def slot_pair(card: dict, slot: str) -> tuple[str, str]:
    item = examples(card).get(slot)
    if item is None:
        raise MergeError(f"rank {card.get('frequency_rank')}: invalid slot {slot}")
    return item["german"], item["english"]


def set_slot(card: dict, slot: str, german: str, english: str) -> None:
    if not german.strip() or not english.strip():
        raise MergeError(f"rank {card['frequency_rank']} {slot}: empty reviewed text")
    if slot == "main":
        card["german_sentence"] = german
        card["english_sentence"] = english
        return
    try:
        index = int(slot.removeprefix("extra")) - 1
        example = card["extra_examples"][index]
    except (ValueError, IndexError) as exc:
        raise MergeError(f"rank {card['frequency_rank']}: invalid slot {slot}") from exc
    example["german"] = german
    example["english"] = english


def index_baseline(files: dict[str, list[dict]]) -> dict[int, dict]:
    cards: dict[int, dict] = {}
    for rows in files.values():
        for card in rows:
            rank = card.get("frequency_rank")
            if isinstance(rank, int):
                if rank in cards:
                    raise MergeError(f"duplicate baseline rank {rank}")
                cards[rank] = card
    return cards


def validated_rewrites(
    baseline: dict[int, dict],
    clean_cards: dict[int, dict],
    through_rank: int,
    selected_ids: set[str],
) -> tuple[dict[tuple[int, str], dict], int]:
    manifest = load_json(STAGING / "selection-manifest.json")
    if manifest.get("enriched_commit") != ENRICHED_COMMIT:
        raise MergeError("selection manifest enriched commit mismatch")
    if manifest.get("selection_seed") != SELECTION_SEED:
        raise MergeError("selection manifest seed mismatch")

    manifest_selection = {
        card["semantic_id"] for card in manifest["cards"] if card["selected"]
    }
    if manifest_selection != selected_ids:
        raise MergeError("selection manifest does not match deterministic selection")

    desired: set[tuple[int, str]] = set()
    for rank, card in baseline.items():
        slots = card.get("sentence_design", {}).get("enriched_slots", [])
        if rank <= through_rank and card["semantic_id"] in selected_ids:
            desired.update((rank, slot) for slot in slots)

    merged: dict[tuple[int, str], dict] = {}
    loaded_batches = 0
    for summary in manifest["batches"]:
        batch_id = summary["batch_id"]
        input_path = STAGING / "batches" / f"{batch_id}.json"
        input_bytes = input_path.read_bytes() if input_path.exists() else b""
        if hashlib.sha256(input_bytes).hexdigest() != summary["input_sha256"]:
            raise MergeError(f"{batch_id}: staged input hash mismatch")
        batch_input = load_json(input_path)
        input_keys: set[tuple[int, str]] = set()
        for staged_card in batch_input["cards"]:
            rank = staged_card["frequency_rank"]
            base = baseline.get(rank)
            if base is None or base["semantic_id"] != staged_card["semantic_id"]:
                raise MergeError(f"{batch_id}: baseline identity mismatch at rank {rank}")
            clean = clean_cards.get(rank)
            if clean is None or clean["semantic_id"] != staged_card["semantic_id"]:
                raise MergeError(f"{batch_id}: clean identity mismatch at rank {rank}")
            for slot in staged_card["rewrite_slots"]:
                key = (rank, slot)
                if key in input_keys:
                    raise MergeError(f"{batch_id}: duplicate input key {key}")
                input_keys.add(key)
                german, english = slot_pair(clean, slot)
                actual_hash = stable_hash(german + "\0" + english)
                if staged_card["original_slot_sha256"].get(slot) != actual_hash:
                    raise MergeError(f"{batch_id}: original hash mismatch for {key}")

        relevant = input_keys & desired
        if not relevant:
            continue
        loaded_batches += 1
        generation = load_json(STAGING / "outputs" / f"{batch_id}.json")
        if generation.get("batch_id") != batch_id:
            raise MergeError(f"{batch_id}: generation batch_id mismatch")
        generated: dict[tuple[int, str], dict] = {}
        for candidate in generation.get("rewrites", []):
            key = (candidate.get("frequency_rank"), candidate.get("slot"))
            if key in generated:
                raise MergeError(f"{batch_id}: duplicate generation key {key}")
            if key not in input_keys:
                raise MergeError(f"{batch_id}: unexpected generation key {key}")
            staged_card = next(
                card for card in batch_input["cards"]
                if card["frequency_rank"] == key[0]
            )
            if (
                candidate.get("semantic_id") != staged_card["semantic_id"]
                and key not in FOCUSED_OVERRIDE_KEYS
            ):
                raise MergeError(f"{batch_id}: semantic_id mismatch for {key}")
            generated[key] = candidate
        if set(generated) != input_keys:
            raise MergeError(f"{batch_id}: generation keys do not match batch input")

        review = load_json(STAGING / "reviews" / f"{batch_id}.json")
        reviewed: dict[tuple[int, str], dict] = {}
        for item in review.get("reviews", []):
            key = (item.get("frequency_rank"), item.get("slot"))
            if key in reviewed:
                raise MergeError(f"{batch_id}: duplicate review key {key}")
            if key not in generated:
                raise MergeError(f"{batch_id}: unexpected review key {key}")
            reviewed[key] = item
        if set(reviewed) != set(generated):
            raise MergeError(f"{batch_id}: review keys do not match generation")

        for key in relevant:
            candidate = generated[key]
            item = reviewed[key]
            if key in FOCUSED_OVERRIDE_KEYS:
                continue
            decision = item.get("decision")
            if decision == "reject":
                raise MergeError(f"{batch_id}: reviewer rejected {key}")
            if decision == "accept":
                german, english = candidate.get("german", ""), candidate.get("english", "")
            elif decision == "fix":
                german = item.get("corrected_german", "")
                english = item.get("corrected_english", "")
            else:
                raise MergeError(f"{batch_id}: invalid review decision for {key}")
            if key in merged:
                raise MergeError(f"selected key appears in multiple batches: {key}")
            merged[key] = {
                "german": german,
                "english": english,
                "decision": decision,
                "batch_id": batch_id,
                "structure": candidate["structure"],
                "genre": candidate["genre"],
                "confidence": candidate["confidence"],
            }

    for override_batch, override_keys in FOCUSED_OVERRIDE_BATCHES.items():
        relevant_overrides = desired & override_keys
        if not relevant_overrides:
            continue
        generation = load_json(
            STAGING / "outputs" / f"{override_batch}.json"
        )
        if generation.get("batch_id") != override_batch:
            raise MergeError(f"{override_batch}: override generation batch_id mismatch")
        generated = {}
        for candidate in generation.get("rewrites", []):
            key = (candidate.get("frequency_rank"), candidate.get("slot"))
            if key in generated or key not in override_keys:
                raise MergeError(f"{override_batch}: override has invalid key {key}")
            base = baseline.get(key[0])
            if base is None or candidate.get("semantic_id") != base["semantic_id"]:
                raise MergeError(f"{override_batch}: override identity mismatch for {key}")
            generated[key] = candidate
        if set(generated) != override_keys:
            raise MergeError(f"{override_batch}: override generation key mismatch")

        review = load_json(
            STAGING / "reviews" / f"{override_batch}.json"
        )
        reviewed = {}
        for item in review.get("reviews", []):
            key = (item.get("frequency_rank"), item.get("slot"))
            if key in reviewed or key not in generated:
                raise MergeError(f"{override_batch}: override review has invalid key {key}")
            reviewed[key] = item
        if set(reviewed) != set(generated):
            raise MergeError(f"{override_batch}: override review key mismatch")

        for key in relevant_overrides:
            candidate = generated[key]
            item = reviewed[key]
            decision = item.get("decision")
            if decision == "reject":
                raise MergeError(f"{override_batch}: override reviewer rejected {key}")
            if decision == "accept":
                german = candidate.get("german", "")
                english = candidate.get("english", "")
            elif decision == "fix":
                german = item.get("corrected_german", "")
                english = item.get("corrected_english", "")
            else:
                raise MergeError(f"{override_batch}: invalid override decision for {key}")
            merged[key] = {
                "german": german,
                "english": english,
                "decision": decision,
                "batch_id": override_batch,
                "structure": candidate["structure"],
                "genre": candidate["genre"],
                "confidence": candidate["confidence"],
            }
    missing = desired - merged.keys()
    extra = merged.keys() - desired
    if missing or extra:
        raise MergeError(
            f"reviewed coverage mismatch: {len(missing)} missing, {len(extra)} extra"
        )
    return merged, loaded_batches


def build_expected(through_rank: int) -> tuple[dict[str, bytes], dict[str, int]]:
    files = git_canonical_files()
    baseline = index_baseline(files)
    clean_cards = git_cards(CLEAN_COMMIT)
    if set(baseline) != set(range(1, 1251)):
        raise MergeError("policy-1 baseline does not contain exactly ranks 1-1250")
    selected_ids = selected_semantic_ids(baseline)
    rewrites, loaded_batches = validated_rewrites(
        baseline, clean_cards, through_rank, selected_ids
    )

    applied_slots = 0
    retained_policy1_slots = 0
    finalized_cards = 0
    for rank in sorted(baseline):
        card = baseline[rank]
        design = dict(card.get("sentence_design", {}))
        enriched_slots = list(design.get("enriched_slots", []))
        if rank <= through_rank:
            finalized_cards += 1
            selected = card["semantic_id"] in selected_ids
            slot_audit = {}
            for slot in enriched_slots:
                key = (rank, slot)
                if selected:
                    rewrite = rewrites[key]
                    set_slot(card, slot, rewrite["german"], rewrite["english"])
                    applied_slots += 1
                    slot_audit[slot] = {
                        "review_decision": rewrite["decision"],
                        "generation_batch": rewrite["batch_id"],
                        "structure": rewrite["structure"],
                        "genre": rewrite["genre"],
                        "confidence": rewrite["confidence"],
                    }
                else:
                    retained_policy1_slots += 1
            design["policy_version"] = 3
            design["contextual_rewrite"] = {
                "status": "finalized",
                "finalized_through_rank": through_rank,
                "selection_seed": SELECTION_SEED,
                "selected": selected,
                "rewritten_slots": enriched_slots if selected else [],
                "retained_policy1_slots": [] if selected else enriched_slots,
                "slot_audit": slot_audit,
            }
            card["sentence_design"] = design
        else:
            if design.get("policy_version") != 1:
                raise MergeError(f"rank {rank}: baseline is not policy version 1")
            retained_policy1_slots += len(enriched_slots)

    serialized = {
        filename: "".join(
            json.dumps(card, ensure_ascii=False) + "\n" for card in rows
        ).encode("utf-8")
        for filename, rows in files.items()
    }
    stats = {
        "finalized_cards": finalized_cards,
        "applied_slots": applied_slots,
        "retained_policy1_slots": retained_policy1_slots,
        "loaded_batches": loaded_batches,
    }
    return serialized, stats


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--through-rank", type=int, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.through_rank <= 1250:
        parser.error("--through-rank must be between 1 and 1250")
    try:
        expected, stats = build_expected(args.through_rank)
        if args.check:
            errors = []
            for filename, content in expected.items():
                path = CANONICAL / filename
                if not path.exists():
                    errors.append(f"missing data/canonical/{filename}")
                elif path.read_bytes() != content:
                    errors.append(f"stale data/canonical/{filename}")
            if errors:
                raise MergeError("; ".join(errors))
            action = "Checked"
        else:
            for filename, content in expected.items():
                atomic_write(CANONICAL / filename, content)
            action = "Merged"
    except (MergeError, subprocess.CalledProcessError, OSError, json.JSONDecodeError) as exc:
        print(f"contextual merge failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print(
        f"{action} through rank {args.through_rank}: "
        f"{stats['finalized_cards']} finalized cards, "
        f"{stats['applied_slots']} reviewed slots applied, "
        f"{stats['retained_policy1_slots']} policy-1 slots preserved, "
        f"{stats['loaded_batches']} staging batches used."
    )


if __name__ == "__main__":
    main()
