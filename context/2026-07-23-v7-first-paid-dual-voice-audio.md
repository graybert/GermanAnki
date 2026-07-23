# V7 first paid dual-voice audio — 2026-07-23

The package is `dist/German-Core-Dual-Voice-Audio-Test-V7-10-Cards.apkg`.
Its internal deck name is `German Core Dual Voice Audio Test V7 - 10 Cards`.
V7 uses new test identities and imports beside previous releases.

The ElevenLabs Creator subscription authenticated with a 131,000-credit limit
and zero prior use. Generation produced 20 MP3s: one isolated headword and one
exact main sentence for each of ranks 1–10. Odd curriculum positions use
Marlene Lark; even positions use Markus. Receipt validation confirms each
word/sentence pair shares the same voice.

ElevenLabs reported 192 credits charged from 346 raw input characters:
21 credits for the 10 headwords and 171 for the 10 sentences. The subscription
reported 130,808 credits remaining afterward. The committed aggregate record is
`data/audio/generation-batches/2026-07-23-first-10.json`; secret-bearing and
request-level data stays ignored locally.

The package imports as 10 notes/cards with 19 fields and exactly 20 media files.
Every card has word audio, sentence audio, deterministic voice metadata, normal
word-then-sentence autoplay, and 0.5×/0.6×/0.7× runtime sentence controls. Slow
playback adds no media or ElevenLabs credits.
