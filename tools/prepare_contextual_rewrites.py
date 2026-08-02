"""Prepare deterministic, read-only staging inputs for contextual rewrites.

Canonical working-tree files are deliberately ignored. Clean card content and
policy-1 enriched-slot metadata are read from pinned Git commits, and all
artifacts are written below the ignored ``tmp/contextual-rewrites`` directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "tmp" / "contextual-rewrites"
CLEAN_COMMIT = "940d9d5"
ENRICHED_COMMIT = "7894d18"
SELECTION_SEED = "semantic-diversity-v3"
SELECTION_RATE = 0.80
STRATUM_SIZE = 50
MAX_BATCH_CARDS = 25
TARGET_BATCH_SLOTS = 45
CANONICAL_FILES = (
    "frequency-0001-0010.jsonl",
    "frequency-0011-0050.jsonl",
    "frequency-0051-0200.jsonl",
    "frequency-0201-0500.jsonl",
    "frequency-0501-1000.jsonl",
    "frequency-1001-1500.jsonl",
)
WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüß]+")


def git_cards(commit: str) -> dict[int, dict]:
    cards: dict[int, dict] = {}
    for filename in CANONICAL_FILES:
        path = f"data/canonical/{filename}"
        result = subprocess.run(
            ["git", "show", f"{commit}:{path}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            card = json.loads(line)
            rank = card.get("frequency_rank")
            if isinstance(rank, int):
                if rank in cards:
                    raise ValueError(f"duplicate rank {rank} at {commit}")
                cards[rank] = card
    return cards


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def stratum_start(rank: int) -> int:
    return ((rank - 1) // STRATUM_SIZE) * STRATUM_SIZE + 1


def selected_semantic_ids(enriched: dict[int, dict]) -> set[str]:
    strata: dict[int, list[dict]] = defaultdict(list)
    for card in enriched.values():
        slots = card.get("sentence_design", {}).get("enriched_slots", [])
        if slots:
            strata[stratum_start(card["frequency_rank"])].append(card)

    selected: set[str] = set()
    for cards in strata.values():
        ordered = sorted(
            cards,
            key=lambda card: stable_hash(
                f"{SELECTION_SEED}|{card['semantic_id']}"
            ),
        )
        count = int(len(ordered) * SELECTION_RATE + 0.5)
        selected.update(card["semantic_id"] for card in ordered[:count])
    return selected


def examples(card: dict) -> dict[str, dict[str, str]]:
    result = {
        "main": {
            "german": card["german_sentence"],
            "english": card["english_sentence"],
            "german_word_count": len(WORD_RE.findall(card["german_sentence"])),
        }
    }
    for index, example in enumerate(card["extra_examples"], 1):
        result[f"extra{index}"] = {
            "german": example["german"],
            "english": example["english"],
            "german_word_count": len(WORD_RE.findall(example["german"])),
        }
    return result


def build_card_input(clean: dict, enriched: dict) -> dict:
    original_examples = examples(clean)
    slots = list(enriched["sentence_design"]["enriched_slots"])
    slot_hashes = {
        slot: stable_hash(
            original_examples[slot]["german"]
            + "\0"
            + original_examples[slot]["english"]
        )
        for slot in slots
    }
    return {
        "frequency_rank": clean["frequency_rank"],
        "semantic_id": clean["semantic_id"],
        "selection_hash": stable_hash(
            f"{SELECTION_SEED}|{clean['semantic_id']}"
        ),
        "style_seed": stable_hash(
            f"contextual-style-v1|{clean['semantic_id']}"
        )[:16],
        "target": clean["target"],
        "lemma": clean["lemma"],
        "sense_id": clean["sense_id"],
        "part_of_speech": clean["part_of_speech"],
        "meaning": clean["meaning"],
        "forms": clean["forms"],
        "usage_note": clean["usage_note"],
        "register": clean["register"],
        "variety": clean["variety"],
        "example_focus": clean.get("example_focus", ""),
        "original_examples": original_examples,
        "rewrite_slots": slots,
        "original_slot_sha256": slot_hashes,
    }


def make_batches(cards: list[dict]) -> list[list[dict]]:
    batches: list[list[dict]] = []
    current: list[dict] = []
    slots = 0
    for card in cards:
        card_slots = len(card["rewrite_slots"])
        if current and (
            len(current) >= MAX_BATCH_CARDS
            or slots + card_slots > TARGET_BATCH_SLOTS
        ):
            batches.append(current)
            current = []
            slots = 0
        current.append(card)
        slots += card_slots
    if current:
        batches.append(current)
    return batches


def prompt_for(batch_id: str, input_path: str) -> str:
    return f"""# German contextual rewrite batch - prompt version 4

Work read-only. Read `{input_path}` and rewrite every listed `rewrite_slots`
entry, returning exactly one result per listed slot and no others. Batch ID must
be `{batch_id}` and prompt version must be 4.

Use the entire staged card as semantic authority. Produce original, idiomatic
Germany Standard German examples of 9-20 words and faithful natural English
translations. Preserve the intended target sense and make a valid surface form
pedagogically salient. Every clause must belong to one plausible scene or
logical relationship; never append unrelated atmosphere merely to add length.

Count the German words after drafting and revise every result outside 9-20
words. Match propositions exactly across languages: preserve polarity, tense,
modality, participants, number, time, place, and causal relations; do not add
or omit information merely to make the English smoother. Prefer conservative,
idiomatic German collocations over clever but questionable phrasing. Every
pronoun must have a recoverable antecedent within the self-contained example.

Vary syntax and setting genuinely: narration, description, causes,
conditionals, inversion, temporal sequencing, instructions, messages,
internal thought, brief exchanges, and self-contained original genre scenes.
Do not imitate copyrighted passages, franchises, or recognizable characters.
Avoid formulaic coffee, rain, doors, silence, meetings, reporters, unexplained
noises, and the policy-1 setup + speaker + quotation frame. Direct and reported
speech combined must stay below 15% of the batch, and no structure label may
exceed 25%. Avoid repeated openings and names. Preserve useful contrast among
the four examples on each card.

Silently verify German grammar, word count, semantic fit, translation
equivalence, target realization, self-contained coherence, and uniqueness.
Use low confidence rather than hiding uncertainty. Copy `frequency_rank`,
`semantic_id`, and slot identities exactly from the input.
"""


def serialized(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def expected_artifacts(start: int, end: int) -> tuple[Path, dict[Path, bytes], dict]:
    clean = git_cards(CLEAN_COMMIT)
    enriched = git_cards(ENRICHED_COMMIT)
    selected_ids = selected_semantic_ids(enriched)

    manifest_cards = []
    selected_inputs = []
    for rank in sorted(enriched):
        if not start <= rank <= end:
            continue
        enriched_card = enriched[rank]
        slots = enriched_card.get("sentence_design", {}).get("enriched_slots", [])
        if not slots:
            continue
        clean_card = clean.get(rank)
        if clean_card is None or clean_card["semantic_id"] != enriched_card["semantic_id"]:
            raise ValueError(f"historical card mismatch at rank {rank}")
        is_selected = enriched_card["semantic_id"] in selected_ids
        manifest_cards.append(
            {
                "frequency_rank": rank,
                "semantic_id": enriched_card["semantic_id"],
                "stratum_start": stratum_start(rank),
                "selection_hash": stable_hash(
                    f"{SELECTION_SEED}|{enriched_card['semantic_id']}"
                ),
                "selected": is_selected,
                "rewrite_slots": list(slots),
            }
        )
        if is_selected:
            selected_inputs.append(build_card_input(clean_card, enriched_card))

    run_dir = OUTPUT_ROOT / f"ranks-{start:04d}-{end:04d}"
    artifacts: dict[Path, bytes] = {}
    batches = make_batches(selected_inputs)
    batch_summaries = []
    for index, cards in enumerate(batches, 1):
        batch_id = f"rewrite-{start:04d}-{end:04d}-{index:04d}"
        relative_input = (
            f"tmp/contextual-rewrites/ranks-{start:04d}-{end:04d}/"
            f"batches/{batch_id}.json"
        )
        payload = {
            "batch_id": batch_id,
            "prompt_version": 4,
            "clean_commit": CLEAN_COMMIT,
            "enriched_commit": ENRICHED_COMMIT,
            "selection_seed": SELECTION_SEED,
            "card_count": len(cards),
            "slot_count": sum(len(card["rewrite_slots"]) for card in cards),
            "cards": cards,
        }
        input_bytes = serialized(payload)
        prompt_bytes = prompt_for(batch_id, relative_input).encode("utf-8")
        artifacts[run_dir / "batches" / f"{batch_id}.json"] = input_bytes
        artifacts[run_dir / "prompts" / f"{batch_id}.txt"] = prompt_bytes
        batch_summaries.append(
            {
                "batch_id": batch_id,
                "card_count": payload["card_count"],
                "slot_count": payload["slot_count"],
                "first_rank": cards[0]["frequency_rank"],
                "last_rank": cards[-1]["frequency_rank"],
                "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
                "prompt_sha256": hashlib.sha256(prompt_bytes).hexdigest(),
            }
        )

    manifest = {
        "schema_version": 1,
        "start_rank": start,
        "end_rank": end,
        "clean_commit": CLEAN_COMMIT,
        "enriched_commit": ENRICHED_COMMIT,
        "selection_seed": SELECTION_SEED,
        "selection_rate": SELECTION_RATE,
        "selection_unit": "affected_card_within_full_50_rank_stratum",
        "affected_card_count": len(manifest_cards),
        "selected_card_count": len(selected_inputs),
        "selected_slot_count": sum(
            len(card["rewrite_slots"]) for card in selected_inputs
        ),
        "batch_count": len(batches),
        "batches": batch_summaries,
        "cards": manifest_cards,
    }
    artifacts[run_dir / "selection-manifest.json"] = serialized(manifest)
    return run_dir, artifacts, manifest


def check_artifacts(run_dir: Path, artifacts: dict[Path, bytes]) -> list[str]:
    errors = []
    for path, expected in artifacts.items():
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
        elif path.read_bytes() != expected:
            errors.append(f"stale {path.relative_to(ROOT)}")
    expected_paths = {path.resolve() for path in artifacts}
    if run_dir.exists():
        for pattern in ("selection-manifest.json", "batches/*.json", "prompts/*.txt"):
            for path in run_dir.glob(pattern):
                if path.resolve() not in expected_paths:
                    errors.append(f"unexpected {path.relative_to(ROOT)}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=1250)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.start < 1 or args.end < args.start or args.end > 1250:
        parser.error("require 1 <= --start <= --end <= 1250")

    try:
        run_dir, artifacts, manifest = expected_artifacts(args.start, args.end)
    except (subprocess.CalledProcessError, ValueError, json.JSONDecodeError) as exc:
        print(f"failed to prepare rewrite inputs: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    if args.check:
        errors = check_artifacts(run_dir, artifacts)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            raise SystemExit(1)
        action = "Checked"
    else:
        for path, content in artifacts.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        action = "Prepared"

    print(
        f"{action} {manifest['selected_card_count']} of "
        f"{manifest['affected_card_count']} affected cards, "
        f"{manifest['selected_slot_count']} slots in "
        f"{manifest['batch_count']} batches at {run_dir.relative_to(ROOT)}."
    )


if __name__ == "__main__":
    main()
