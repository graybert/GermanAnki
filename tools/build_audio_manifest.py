"""Build the deterministic main-sentence audio work queue."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from export_anki import (
    ROOT,
    audio_filename,
    load_curriculum_order,
    load_frequency_cards,
    word_audio_filename,
)


OUTPUT = ROOT / "data" / "audio" / "main-sentence-manifest.jsonl"
WORD_OUTPUT = ROOT / "data" / "audio" / "headword-manifest.jsonl"


def main() -> None:
    order = load_curriculum_order()
    cards = sorted(
        load_frequency_cards(),
        key=lambda card: order[card["semantic_id"]],
    )
    records = []
    word_records = []
    for card in cards:
        sentence = card["german_sentence"]
        records.append({
            "schema_version": 1,
            "audio_kind": "main_sentence",
            "text": sentence,
            "semantic_id": card["semantic_id"],
            "frequency_rank": card["frequency_rank"],
            "curriculum_order": order[card["semantic_id"]],
            "german_sentence": sentence,
            "text_sha256": hashlib.sha256(sentence.encode("utf-8")).hexdigest(),
            "audio_filename": audio_filename(card),
            "audio_status": "not_generated",
            "provider": "",
            "model": "",
            "voice_id": "",
        })
        target = card["target"]
        word_records.append({
            "schema_version": 1,
            "audio_kind": "headword",
            "text": target,
            "semantic_id": card["semantic_id"],
            "frequency_rank": card["frequency_rank"],
            "curriculum_order": order[card["semantic_id"]],
            "target": target,
            "text_sha256": hashlib.sha256(target.encode("utf-8")).hexdigest(),
            "audio_filename": word_audio_filename(card),
            "audio_status": "not_generated",
            "provider": "",
            "model": "",
            "voice_id": "",
        })
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )
    WORD_OUTPUT.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in word_records),
        encoding="utf-8",
    )
    print(
        f"Wrote {len(records)} sentence jobs and {len(word_records)} headword jobs "
        f"to data/audio/"
    )


if __name__ == "__main__":
    main()
