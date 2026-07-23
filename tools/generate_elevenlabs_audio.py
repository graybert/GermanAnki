"""Generate canonical main-sentence MP3s with the ElevenLabs API.

The script is resumable: existing non-empty files are skipped unless
--overwrite is supplied. API keys are read only from ELEVENLABS_API_KEY.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "audio" / "main-sentence-manifest.jsonl"
DEFAULT_OUTPUT = ROOT / "data" / "audio" / "generated"
API_BASE = "https://api.elevenlabs.io/v1/text-to-speech"


def load_jobs(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def generate(
    *,
    text: str,
    voice_id: str,
    model_id: str,
    output_format: str,
    api_key: str,
    timeout: int,
) -> bytes:
    url = f"{API_BASE}/{voice_id}?output_format={output_format}"
    body = json.dumps(
        {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True,
                "speed": 0.92,
            },
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "xi-api-key": api_key,
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--voice-id", required=True)
    parser.add_argument("--model-id", default="eleven_multilingual_v2")
    parser.add_argument("--output-format", default="mp3_44100_128")
    parser.add_argument("--start-rank", type=int, default=1)
    parser.add_argument("--end-rank", type=int)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--pause-seconds", type=float, default=0.25)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    jobs = [
        job
        for job in load_jobs(args.manifest)
        if job["frequency_rank"] >= args.start_rank
        and (args.end_rank is None or job["frequency_rank"] <= args.end_rank)
    ]
    if args.limit is not None:
        jobs = jobs[: args.limit]
    total_characters = sum(len(job["german_sentence"]) for job in jobs)
    print(
        f"Selected {len(jobs)} main sentences ({total_characters} characters), "
        f"model={args.model_id}, voice={args.voice_id}"
    )
    if args.dry_run:
        for job in jobs:
            print(job["audio_filename"], job["german_sentence"])
        return

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise SystemExit("Set ELEVENLABS_API_KEY before generating paid audio.")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    generated = skipped = 0
    for index, job in enumerate(jobs, 1):
        destination = args.output_dir / job["audio_filename"]
        if destination.is_file() and destination.stat().st_size > 0 and not args.overwrite:
            skipped += 1
            print(f"[{index}/{len(jobs)}] skip {destination.name}")
            continue
        print(f"[{index}/{len(jobs)}] generate {destination.name}")
        try:
            audio = generate(
                text=job["german_sentence"],
                voice_id=args.voice_id,
                model_id=args.model_id,
                output_format=args.output_format,
                api_key=api_key,
                timeout=args.timeout,
            )
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise SystemExit(f"ElevenLabs HTTP {exc.code}: {details}") from exc
        if not audio:
            raise RuntimeError(f"ElevenLabs returned no audio for {job['semantic_id']}")
        temporary = destination.with_suffix(destination.suffix + ".part")
        temporary.write_bytes(audio)
        temporary.replace(destination)
        generated += 1
        if index < len(jobs):
            time.sleep(args.pause_seconds)
    print(f"Done: {generated} generated, {skipped} already present.")


if __name__ == "__main__":
    main()
