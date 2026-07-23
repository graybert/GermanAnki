# V6 sentence-speed audition — 2026-07-23

The package is `dist/German-Core-Audio-Speed-Test-V6-10-Cards.apkg`, with the
internal deck name `German Core Audio Speed Test V6 - 10 Cards`. It has new test
deck/model IDs and V6-namespaced GUIDs, so it imports beside earlier tests.

Only the `der` card has audio. Its existing sentence MP3 is referenced by a new
hidden `SentenceAudioFile` field. Both card faces provide 0.5×, 0.6× and 0.7×
buttons that play that same media file through HTML audio playback-rate control.
This avoids generating or packaging three redundant files. The standard word
and sentence controls and the word-then-sentence autoplay order remain intact.

Validation confirms 18 fields per note, exactly two packaged media files, three
speed buttons on each side of `der`, and no speed controls on ranks 2–10.
