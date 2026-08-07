"""Verify generated ElevenLabs media against manifests and request receipts."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIO_DIR = ROOT / "data" / "audio" / "generated"
DEFAULT_MANIFESTS = (
    ROOT / "data" / "audio" / "main-sentence-manifest.jsonl",
    ROOT / "data" / "audio" / "headword-manifest.jsonl",
)
DEFAULT_VOICE_CONFIG = ROOT / "data" / "audio" / "voice-profiles.json"


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio-dir", type=Path, default=DEFAULT_AUDIO_DIR)
    parser.add_argument("--receipts", type=Path)
    parser.add_argument("--start-rank", type=int, default=1)
    parser.add_argument("--end-rank", type=int, default=1250)
    parser.add_argument("--voice-config", type=Path, default=DEFAULT_VOICE_CONFIG)
    parser.add_argument("--model-id", default="eleven_multilingual_v2")
    parser.add_argument("--headword-model-id", default="eleven_flash_v2_5")
    parser.add_argument("--headword-language-code", default="de")
    parser.add_argument("--output-format", default="mp3_44100_128")
    parser.add_argument(
        "--allow-extra-files",
        action="store_true",
        help="permit MP3s outside the selected rank range in a shared directory",
    )
    parser.add_argument(
        "--ffprobe",
        action="store_true",
        help="require ffprobe and decode-probe every expected MP3",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.start_rank < 1 or args.end_rank < args.start_rank:
        raise SystemExit("Invalid rank range")

    errors: list[str] = []
    jobs = [
        job
        for manifest in DEFAULT_MANIFESTS
        for job in read_jsonl(manifest)
        if args.start_rank <= int(job["frequency_rank"]) <= args.end_rank
    ]
    expected_count = (args.end_rank - args.start_rank + 1) * 2
    if len(jobs) != expected_count:
        errors.append(f"expected {expected_count} manifest jobs, found {len(jobs)}")

    filenames = [job["audio_filename"] for job in jobs]
    if len(set(filenames)) != len(filenames):
        errors.append("manifest audio filenames are not unique")
    keys = [(job["semantic_id"], job["audio_kind"]) for job in jobs]
    if len(set(keys)) != len(keys):
        errors.append("manifest semantic-ID/audio-kind pairs are not unique")

    profiles = json.loads(args.voice_config.read_text(encoding="utf-8"))["profiles"]
    if not profiles:
        errors.append("voice configuration contains no profiles")

    receipts_path = args.receipts or args.audio_dir / "generation-receipts.jsonl"
    receipts = read_jsonl(receipts_path) if receipts_path.is_file() else []
    latest_receipt = {
        receipt.get("audio_filename"): receipt
        for receipt in receipts
        if receipt.get("audio_filename")
    }

    expected_files = set(filenames)
    actual_files = {path.name for path in args.audio_dir.glob("*.mp3") if path.is_file()}
    for filename in sorted(expected_files - actual_files):
        errors.append(f"missing MP3: {filename}")
    if not args.allow_extra_files:
        for filename in sorted(actual_files - expected_files):
            errors.append(f"unexpected MP3: {filename}")

    ffprobe = shutil.which("ffprobe") if args.ffprobe else None
    if args.ffprobe and not ffprobe:
        errors.append("--ffprobe requested but ffprobe was not found on PATH")

    for job in jobs:
        filename = job["audio_filename"]
        path = args.audio_dir / filename
        if path.is_file() and path.stat().st_size == 0:
            errors.append(f"empty MP3: {filename}")

        receipt = latest_receipt.get(filename)
        if receipt is None:
            errors.append(f"missing receipt: {filename}")
        else:
            profile = profiles[(int(job["curriculum_order"]) - 1) % len(profiles)]
            expected = {
                "semantic_id": job["semantic_id"],
                "frequency_rank": job["frequency_rank"],
                "audio_kind": job["audio_kind"],
                "audio_filename": filename,
                "text": job["text"],
                "voice_key": profile["key"],
                "voice_name": profile["display_name"],
                "voice_id": profile["voice_id"],
                "model_id": (
                    args.headword_model_id
                    if job["audio_kind"] == "headword"
                    else args.model_id
                ),
                "language_code": (
                    args.headword_language_code
                    if job["audio_kind"] == "headword"
                    else None
                ),
                "output_format": args.output_format,
            }
            for field, value in expected.items():
                if receipt.get(field) != value:
                    errors.append(
                        f"receipt mismatch for {filename}: {field} is "
                        f"{receipt.get(field)!r}, expected {value!r}"
                    )
            if path.is_file() and receipt.get("file_bytes") != path.stat().st_size:
                errors.append(
                    f"receipt mismatch for {filename}: file_bytes is "
                    f"{receipt.get('file_bytes')!r}, expected {path.stat().st_size}"
                )

        if ffprobe and path.is_file() and path.stat().st_size:
            result = subprocess.run(
                [ffprobe, "-v", "error", "-show_entries", "stream=codec_name", path],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode or "codec_name=mp3" not in result.stdout:
                detail = result.stderr.strip() or "not identified as MP3"
                errors.append(f"ffprobe failed for {filename}: {detail}")

    if errors:
        preview = "\n".join(f"- {error}" for error in errors[:100])
        remainder = len(errors) - 100
        if remainder:
            preview += f"\n- ... and {remainder} more errors"
        raise SystemExit(f"Generated-audio verification failed ({len(errors)} errors):\n{preview}")

    print(
        f"Verified {len(jobs)} jobs and {len(expected_files)} selected MP3s for ranks "
        f"{args.start_rank}-{args.end_rank}; receipts, voices, model, output, "
        f"and file sizes match" + ("; ffprobe passed." if ffprobe else ".")
    )


if __name__ == "__main__":
    main()
