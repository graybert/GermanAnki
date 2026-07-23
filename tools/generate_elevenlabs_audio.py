"""Generate canonical main-sentence MP3s with the ElevenLabs API.

The script is resumable: existing non-empty files are skipped unless
--overwrite is supplied. API keys are read only from ELEVENLABS_API_KEY.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "audio" / "main-sentence-manifest.jsonl"
DEFAULT_WORD_MANIFEST = ROOT / "data" / "audio" / "headword-manifest.jsonl"
DEFAULT_OUTPUT = ROOT / "data" / "audio" / "generated"
DEFAULT_VOICE_CONFIG = ROOT / "data" / "audio" / "voice-profiles.json"
DEFAULT_API_KEY_FILE = ROOT / "secrets" / "elevenlabs-api-key.txt"
API_BASE = "https://api.elevenlabs.io/v1/text-to-speech"


def load_jobs(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_api_key(path: Path) -> str:
    environment_key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if environment_key:
        return environment_key
    if not path.is_file():
        return ""
    return next(
        (
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ),
        "",
    )


def load_voice_profiles(path: Path) -> list[dict]:
    config = json.loads(path.read_text(encoding="utf-8"))
    profiles = config.get("profiles", [])
    if not profiles:
        raise SystemExit(f"No voice profiles configured in {path}")
    for profile in profiles:
        for key in ("key", "display_name", "voice_id"):
            if not profile.get(key):
                raise SystemExit(f"Voice profile is missing {key}: {profile}")
    return profiles


def assigned_voice(job: dict, profiles: list[dict]) -> dict:
    position = int(job["curriculum_order"])
    return profiles[(position - 1) % len(profiles)]


def generate(
    *,
    text: str,
    voice_id: str,
    model_id: str,
    output_format: str,
    api_key: str,
    timeout: int,
) -> tuple[bytes, dict]:
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
        return response.read(), {
            "character_cost": response.headers.get("character-cost"),
            "request_id": response.headers.get("request-id"),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--include-headwords", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--voice-id")
    parser.add_argument("--voice-config", type=Path, default=DEFAULT_VOICE_CONFIG)
    parser.add_argument("--api-key-file", type=Path, default=DEFAULT_API_KEY_FILE)
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
    manifest_paths = [args.manifest]
    if args.include_headwords:
        manifest_paths.append(DEFAULT_WORD_MANIFEST)
    jobs = [
        job
        for manifest_path in manifest_paths
        for job in load_jobs(manifest_path)
        if job["frequency_rank"] >= args.start_rank
        and (args.end_rank is None or job["frequency_rank"] <= args.end_rank)
    ]
    if args.limit is not None:
        jobs = jobs[: args.limit]
    profiles = (
        [{
            "key": "command_line_voice",
            "display_name": "Command-line voice",
            "voice_id": args.voice_id,
        }]
        if args.voice_id
        else load_voice_profiles(args.voice_config)
    )
    jobs.sort(key=lambda job: (job["curriculum_order"], job["audio_kind"]))
    total_characters = sum(len(job["text"]) for job in jobs)
    print(
        f"Selected {len(jobs)} audio jobs ({total_characters} characters), "
        f"model={args.model_id}, voices="
        f"{', '.join(profile['display_name'] for profile in profiles)}"
    )
    if args.dry_run:
        for job in jobs:
            voice = assigned_voice(job, profiles)
            print(
                job["audio_filename"],
                f"[{job['audio_kind']}]",
                f"[{voice['display_name']} | {voice['voice_id']}]",
                job["text"],
            )
        return

    api_key = load_api_key(args.api_key_file)
    if not api_key:
        raise SystemExit(
            "Set ELEVENLABS_API_KEY or paste the key into "
            f"{args.api_key_file} before generating paid audio."
        )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    receipts_path = args.output_dir / "generation-receipts.jsonl"
    generated = skipped = 0
    charged_credits = 0
    for index, job in enumerate(jobs, 1):
        voice = assigned_voice(job, profiles)
        destination = args.output_dir / job["audio_filename"]
        if destination.is_file() and destination.stat().st_size > 0 and not args.overwrite:
            skipped += 1
            print(f"[{index}/{len(jobs)}] skip {destination.name}")
            continue
        print(
            f"[{index}/{len(jobs)}] generate {destination.name} "
            f"with {voice['display_name']}"
        )
        try:
            audio, response_metadata = generate(
                text=job["text"],
                voice_id=voice["voice_id"],
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
        raw_cost = response_metadata["character_cost"]
        request_cost = int(raw_cost) if raw_cost and raw_cost.isdigit() else None
        if request_cost is not None:
            charged_credits += request_cost
        receipt = {
            "generated_at_utc": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat(),
            "semantic_id": job["semantic_id"],
            "frequency_rank": job["frequency_rank"],
            "audio_kind": job["audio_kind"],
            "audio_filename": job["audio_filename"],
            "text": job["text"],
            "text_characters": len(job["text"]),
            "voice_key": voice["key"],
            "voice_name": voice["display_name"],
            "voice_id": voice["voice_id"],
            "model_id": args.model_id,
            "output_format": args.output_format,
            "character_cost": request_cost,
            "request_id": response_metadata["request_id"],
            "file_bytes": len(audio),
        }
        with receipts_path.open("a", encoding="utf-8") as receipts:
            receipts.write(json.dumps(receipt, ensure_ascii=False) + "\n")
        generated += 1
        if index < len(jobs):
            time.sleep(args.pause_seconds)
    print(
        f"Done: {generated} generated, {skipped} already present, "
        f"{charged_credits} credits reported by ElevenLabs."
    )


if __name__ == "__main__":
    main()
