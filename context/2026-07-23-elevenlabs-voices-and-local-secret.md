# ElevenLabs voices and local secret — 2026-07-23

`data/audio/voice-profiles.json` records the selected voices:

- odd curriculum positions: Marlene Lark (`MTTjXkEpZepLTqO0xH0f`);
- even curriculum positions: Markus (`IeQubAjK1ujbppIdhJw4`).

`tools/generate_elevenlabs_audio.py` loads this configuration by default and
assigns voices deterministically from curriculum order. `--voice-id` remains an
explicit single-voice override. A 10-sentence dry run confirmed alternating
assignments without making paid API calls.

The ElevenLabs API key belongs in the local
`secrets/elevenlabs-api-key.txt`. The entire `secrets/` directory is ignored by
Git, and `git check-ignore` plus `git ls-files` confirmed that the file is
ignored and untracked. The generator checks `ELEVENLABS_API_KEY` first and then
this file. `SECRETS.md` documents safe handling and key rotation.
