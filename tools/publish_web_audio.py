"""Publish only manifest-approved audio files and a browser lookup table."""
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "data" / "audio" / "generated"
PUBLIC = ROOT / "data" / "audio" / "web"
WORD_MANIFEST = ROOT / "data" / "audio" / "headword-manifest.jsonl"
SENTENCE_MANIFEST = ROOT / "data" / "audio" / "main-sentence-manifest.jsonl"
LOOKUP = ROOT / "viewer" / "audio-files.js"

def rows(path: Path, through_rank: int) -> list[dict]:
    return [row for row in (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()) if row["frequency_rank"] <= through_rank]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--through-rank", type=int, required=True)
    args = parser.parse_args()
    words = {row["frequency_rank"]: row for row in rows(WORD_MANIFEST, args.through_rank)}
    sentences = {row["frequency_rank"]: row for row in rows(SENTENCE_MANIFEST, args.through_rank)}
    expected_ranks = set(range(1, args.through_rank + 1))
    if set(words) != expected_ranks or set(sentences) != expected_ranks:
        raise SystemExit("Audio manifests are not continuous through the requested rank.")
    expected_files: set[str] = set()
    lookup: dict[int, list[str]] = {}
    for rank in sorted(expected_ranks):
        pair = [words[rank]["audio_filename"], sentences[rank]["audio_filename"]]
        for filename in pair:
            source = GENERATED / filename
            if not source.is_file() or source.stat().st_size == 0:
                raise SystemExit(f"Missing generated audio: {filename}")
            expected_files.add(filename)
        lookup[rank] = pair
    PUBLIC.mkdir(parents=True, exist_ok=True)
    if PUBLIC.resolve() != (ROOT / "data" / "audio" / "web").resolve():
        raise SystemExit("Refusing to prune an unexpected public-audio directory.")
    for existing in PUBLIC.glob("*.mp3"):
        if existing.name not in expected_files:
            existing.unlink()
    for filename in sorted(expected_files):
        shutil.copy2(GENERATED / filename, PUBLIC / filename)
    LOOKUP.write_text("const audioFiles = " + json.dumps(lookup, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    print(f"Published {len(expected_files)} MP3s for ranks 1-{args.through_rank} and wrote {LOOKUP.relative_to(ROOT)}.")

if __name__ == "__main__":
    main()
