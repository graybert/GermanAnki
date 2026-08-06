"""Build deterministic per-card completion state from canonical text and audio files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
AUDIO = ROOT / "data" / "audio"
GENERATED = AUDIO / "generated"
PUBLISHED = AUDIO / "web"
OUT = ROOT / "data" / "status" / "card-completion.jsonl"


def jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(audio_dir: Path) -> list[dict]:
    cards = []
    for path in sorted(CANONICAL.glob("frequency-*.jsonl")):
        cards.extend(jsonl(path))
    words = {row["frequency_rank"]: row for row in jsonl(AUDIO / "headword-manifest.jsonl")}
    sentences = {row["frequency_rank"]: row for row in jsonl(AUDIO / "main-sentence-manifest.jsonl")}
    rows = []
    for card in sorted(cards, key=lambda item: item["frequency_rank"]):
        rank = card["frequency_rank"]
        jobs = {"headword": words.get(rank), "main_sentence": sentences.get(rank)}
        audio = {}
        for kind, job in jobs.items():
            path = audio_dir / job["audio_filename"] if job else None
            present = bool(path and path.is_file() and path.stat().st_size > 0)
            published = PUBLISHED / job["audio_filename"] if job else None
            published_matches = bool(
                present
                and published
                and published.is_file()
                and path.stat().st_size == published.stat().st_size
                and sha256(path) == sha256(published)
            )
            audio[kind] = {
                "expected": bool(job),
                "present": present,
                "filename": job["audio_filename"] if job else "",
                "text_sha256": job["text_sha256"] if job else "",
                "file_sha256": sha256(path) if present else "",
                "file_bytes": path.stat().st_size if present else 0,
                "published_matches": published_matches,
            }
        text_authored = card.get("text_status") == "draft_complete_pending_human_review"
        rewrite = card.get("sentence_design", {}).get("contextual_rewrite", {})
        text_reviewed = (
            rewrite.get("status") == "finalized"
            and rewrite.get("finalized_through_rank", 0) >= rank
        )
        audio_ready = all(
            item["expected"] and item["present"] and item["published_matches"]
            for item in audio.values()
        )
        rows.append({
            "schema_version": 1,
            "frequency_rank": rank,
            "semantic_id": card["semantic_id"],
            "text_status": card.get("text_status", ""),
            "text_authored": text_authored,
            "text_reviewed": text_reviewed,
            "audio": audio,
            "audio_ready": audio_ready,
            "card_state": "complete" if text_reviewed and audio_ready else "incomplete",
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio-dir", type=Path, default=PUBLISHED)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rows = build(args.audio_dir)
    content = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    if args.check:
        if not OUT.is_file() or OUT.read_text(encoding="utf-8") != content:
            raise SystemExit(f"Stale completion index: run {Path(__file__).name}")
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(content, encoding="utf-8")
        complete = sum(row["card_state"] == "complete" for row in rows)
        print(f"Wrote {len(rows)} states to {OUT}; {complete} complete, {len(rows) - complete} incomplete.")


if __name__ == "__main__":
    main()
