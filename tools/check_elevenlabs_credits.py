"""Report live ElevenLabs credits and exact manifest requirements safely."""

from __future__ import annotations

import argparse
import datetime
import json
import os
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_KEY_FILE = ROOT / "secrets" / "elevenlabs-api-key.txt"
MANIFESTS = (
    ROOT / "data" / "audio" / "main-sentence-manifest.jsonl",
    ROOT / "data" / "audio" / "headword-manifest.jsonl",
)


def api_key() -> str:
    value = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if value:
        return value
    if not API_KEY_FILE.is_file():
        return ""
    return next(
        (line.strip() for line in API_KEY_FILE.read_text(encoding="utf-8").splitlines()
         if line.strip() and not line.lstrip().startswith("#")),
        "",
    )


def manifest_cost(path: Path) -> tuple[int, int]:
    jobs = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return len(jobs), sum(len(job["text"]) for job in jobs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--offline", action="store_true", help="show manifest cost without querying the account")
    args = parser.parse_args()
    costs = {path.name: manifest_cost(path) for path in MANIFESTS}
    required = sum(characters for _, characters in costs.values())
    for name, (jobs, characters) in costs.items():
        print(f"{name}: {jobs} jobs, {characters} Multilingual v2 credits")
    print(f"Total planned requirement: {required} credits")
    if args.offline:
        return
    key = api_key()
    if not key:
        raise SystemExit("No ElevenLabs API key found; use --offline or configure the ignored local key file.")
    request = urllib.request.Request(
        "https://api.elevenlabs.io/v1/user/subscription",
        headers={"xi-api-key": key},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            subscription = json.load(response)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"ElevenLabs subscription query failed with HTTP {exc.code}.") from exc
    used = int(subscription["character_count"])
    limit = int(subscription["character_limit"])
    remaining = limit - used
    reset = subscription.get("next_character_count_reset_unix")
    reset_text = (
        datetime.datetime.fromtimestamp(reset, datetime.timezone.utc).isoformat()
        if reset else "unknown"
    )
    print(f"Plan: {subscription.get('tier')} ({subscription.get('status')})")
    print(f"Live usage: {used} of {limit}; {remaining} credits remain; reset {reset_text}")
    print(f"Margin after all planned jobs: {remaining - required} credits")


if __name__ == "__main__":
    main()
