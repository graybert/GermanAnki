# First card completed for review — 2026-07-20

## Content decision

The first `wer` card is now a self-contained micro-lesson:

- Main sentence: `Wer ist das?` / `Who is that?`
- Complete case paradigm: `wer`, `wen`, `wem`, `wessen`
- Two nominative, two accusative, two dative, and one genitive extra example
- Natural English translations rather than artificial uses of “whom”
- A concise usage note connecting the forms to grammatical case

`Wer ist das?` was selected as the main sentence because it is extremely common,
short, immediately usable, and keeps the target unambiguous. The more complex
forms live in the optional teaching material rather than burdening the primary
review prompt.

## Interaction decision

“More examples” is a parent reveal. Each German example inside it is its own
nested reveal, allowing the learner to attempt comprehension before opening that
sentence’s English translation. Case labels (`Nom.`, `Akk.`, `Dat.`, `Gen.`)
make the reason for the changing form visible without putting grammar on the
front of the card.

The case paradigm is a compact table in a separate “Case forms” reveal. This
keeps the back scannable while making all requested forms available.

## Validation

- The canonical JSONL parses successfully as schema version 2.
- All four forms and seven bilingual examples are present in structured data.
- A headless Chrome render verified that the full card fits in light and dark
  layouts.
- Rendering exposed a CSS cascade that tinted nested summaries whenever the
  parent was open; the selector was corrected from all descendant summaries to
  only the direct parent summary.
- The corrected card was rendered again and visually checked. Nested rows remain
  neutral and readable in both themes, and a right-hand chevron now makes their
  hidden translations discoverable.
- No audio or paid APIs were used.
