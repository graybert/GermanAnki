# Local ElevenLabs API key

The API key is a token, not a PEM certificate. Store it only in:

`secrets/elevenlabs-api-key.txt`

That directory is ignored by Git. Paste the key by itself on the first line,
replacing the instructional comments in the local file. The audio generator
reads this file automatically when `ELEVENLABS_API_KEY` is not set.

Verify that Git will ignore it:

```powershell
git check-ignore -v secrets/elevenlabs-api-key.txt
```

Never paste the key into chat, documentation, source code, command arguments,
screenshots, or a committed file. If it is ever exposed, revoke it immediately
in ElevenLabs and create a replacement.
