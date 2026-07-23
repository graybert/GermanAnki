# Audio pipeline

Each note has independent `WordAudio` and `SentenceAudio` fields. On the card
front, the word sound appears beside the headword and the sentence sound below
it. Because the two Anki sound references occur in that order, Anki queues them
as word first, sentence second. Both sides retain normal replay buttons.

## V5 layout test

Only rank 1 (`der`) has audio in the V5 package:

- Word: `De-der.ogg`, speaker joni, downloaded as Wikimedia's MP3 transcode,
  CC BY-SA 3.0.
- Temporary sentence-layout sample: `Wo ist das Buch? Es liegt auf dem Tisch.`,
  speaker Jeuwre, downloaded as Wikimedia's MP3 transcode, CC BY-SA 4.0.

The temporary sentence recording does **not** match the card's canonical
sentence. It exists only to test sequencing and controls and must not be used in
a production deck.

Source pages:

- https://commons.wikimedia.org/wiki/File:De-der.ogg
- https://commons.wikimedia.org/wiki/File:De-Wo_ist_das_Buch._Es_liegt_auf_dem_Tisch..ogg

## Main-sentence generation

`data/audio/main-sentence-manifest.jsonl` is the canonical queue. It contains
every completed card's exact main sentence, sentence hash, semantic ID,
frequency rank, curriculum order, and deterministic MP3 filename.

Preview a paid run without calling the API:

```powershell
python tools/build_audio_manifest.py
python tools/generate_elevenlabs_audio.py `
  --voice-id YOUR_APPROVED_GERMAN_VOICE_ID `
  --limit 5 `
  --dry-run
```

Generate the first five after setting the secret locally:

```powershell
$env:ELEVENLABS_API_KEY = "your-key"
python tools/generate_elevenlabs_audio.py `
  --voice-id YOUR_APPROVED_GERMAN_VOICE_ID `
  --limit 5
```

The default model is `eleven_multilingual_v2` and the output is
`mp3_44100_128`. Existing files are skipped, so interrupted runs resume safely.
Generated files go to the ignored `data/audio/generated/` directory. Review
pronunciation before packaging:

```powershell
python tools/export_anki.py `
  --audio-dir data\audio\generated `
  --require-audio
```

Do not commit an API key. Before a bulk run, choose a voice whose verified
language/accent is German, generate a small review batch, and have a German
speaker approve it.
