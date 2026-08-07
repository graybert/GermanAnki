# Ranks 1601–1650 contextual and audio finalization — 2026-08-07

Ranks 1601–1650 were rebuilt from their compact batch source and reviewed under
contextual sentence policy 3. Forty-seven policy-1 instructional wrappers were
replaced with original, self-contained contextual examples. The accepted
rewrites were written back to `tools/batch_007_1601_1650.txt` so future builds
preserve them.

Corpus validation passes through rank 1,650 with 6,608 unique German examples.
The deterministic lexical-pattern audit reports seven high-similarity pairs and
31 repeated four-word openings across 6,600 frequency-card examples; these are
review leads rather than automatic failures.

Dual-voice ElevenLabs generation added 100 manifest-selected files for ranks
1,601–1,650. Receipt verification passes for the selected range, including
semantic identity, exact text, voice, model, explicit German language code for
headwords, output format, and file size. The generated corpus was republished to
the browser, and the 1,650-card package validates with 1,650 notes/cards and
3,300 media files under current-Anki import and rendering checks.

The standalone audio verifier now supports `--allow-extra-files`, allowing a
bounded checkpoint to be verified inside the shared generated-audio directory
without incorrectly rejecting valid files from earlier ranks.

Next: rewrite the structurally insufficient prepared cards at ranks 1,651–1,700
before finalization or audio generation. Do not voice their current drafts.
