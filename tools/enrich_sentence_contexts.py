"""Deterministically give every card two structurally varied, rich examples.

The first policy met the length target by putting nearly every short example
inside a reporting-clause quotation.  Policy 2 deliberately distributes the
same authored short examples across narration, consequence, contrast, scene,
genre, and short-dialogue structures.  A stable fifth remains direct speech.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "data" / "canonical"
SOURCE = ROOT / "data" / "source" / "frequency-all-5009.jsonl"
POLICY_VERSION = 2
RICH_MIN_WORDS = 9
MAX_WORDS = 20
AUDIO_LOCKED_THROUGH = 10
WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüß]+")

# Each pair is German/English.  {text} is the intact authored example and
# {stem} is that example without terminal punctuation.  These are intentionally
# different syntactic shapes, not merely different introductions to a quote.
FRAMES = (
    ("{stem}, während draußen Regen gegen die Fenster schlug.", "{stem}, while rain beat against the windows outside."),
    ("{stem}; im Flur wartete bereits jemand auf eine Antwort.", "{stem}; someone in the hall was already waiting for an answer."),
    ("{text} Danach blieb es einen Augenblick vollkommen still.", "{text} Afterward, everything was completely silent for a moment."),
    ("{stem}, doch zunächst bemerkte niemand den kleinen Fehler.", "{stem}, but at first nobody noticed the small mistake."),
    ("{text} Später erinnerte sich Mila noch genau an diesen Augenblick.", "{text} Later, Mila still remembered that moment clearly."),
    ("{stem}, bevor hinter ihnen leise die Tür ins Schloss fiel.", "{stem}, before the door quietly clicked shut behind them."),
    ("{text} Auf dem Bahnsteig begann gleichzeitig die nächste Durchsage.", "{text} At the same time, the next announcement began on the platform."),
    ("{stem}, und aus der Küche roch es plötzlich nach Kaffee.", "{stem}, and suddenly the smell of coffee drifted in from the kitchen."),
    ("{text} Draußen zog die letzte Straßenbahn durch die nasse Nacht.", "{text} Outside, the last tram moved through the rainy night."),
    ("{stem} – genau davor hatte sich Noah seit Tagen gefürchtet.", "{stem}—that was exactly what Noah had feared for days."),
    ("{text} Im nächsten Kapitel sollte diese Entscheidung alles verändern.", "{text} In the next chapter, this decision would change everything."),
    ("{stem}, obwohl der Plan auf dem Papier ganz einfach ausgesehen hatte.", "{stem}, although the plan had looked quite simple on paper."),
    ("{text} Im Kontrollraum blinkte unterdessen eine rote Warnleuchte.", "{text} Meanwhile, a red warning light flashed in the control room."),
    ("{stem}, und irgendwo im dunklen Haus knarrte eine Diele.", "{stem}, and somewhere in the dark house a floorboard creaked."),
    ("{text} Erst viel später verstand Lina, warum dieser Moment wichtig war.", "{text} Only much later did Lina understand why that moment mattered."),
    ("{stem}, während über den Türmen zwei fremde Monde aufgingen.", "{stem}, while two unfamiliar moons rose above the towers."),
    ("{text} Nebenan übte jemand zum dritten Mal dieselbe Klavierstelle.", "{text} Next door, someone practiced the same piano passage for the third time."),
    ("{stem}; für einen Rückzieher war es inzwischen zu spät.", "{stem}; by then it was too late to back out."),
    ("{text} Am anderen Ende der Leitung atmete jemand erleichtert auf.", "{text} At the other end of the line, someone breathed a sigh of relief."),
    ("{stem}, während die Kinder im Hof ihren Drachen steigen ließen.", "{stem}, while the children flew their kite in the courtyard."),
    ("Im Protokoll stand am nächsten Morgen nur ein Satz: „{text}“", "The next morning, the minutes contained only one sentence: “{text}”"),
    ("„{text}“ – „Dann sollten wir keine Zeit verlieren.“", "“{text}” “Then we shouldn't waste any time.”"),
    ("„{text}“ – „Bist du dir da wirklich sicher?“", "“{text}” “Are you really sure about that?”"),
    ("Im alten Tagebuch war zu lesen: „{text}“", "The old diary read: “{text}”"),
    ("Die Detektivin unterstrich eine einzige Zeile: „{text}“", "The detective underlined a single line: “{text}”"),
)

QUESTION_FRAMES = (
    ("{text} Im Hintergrund klapperte jemand ungeduldig mit den Schlüsseln.", "{text} In the background, someone impatiently jingled the keys."),
    ("{text} Keiner am Tisch wollte als Erster antworten.", "{text} Nobody at the table wanted to answer first."),
    ("{text} Auf dem Display lief bereits der Countdown.", "{text} The countdown was already running on the display."),
    ("„{text}“ – „Keine Ahnung, aber wir können zusammen suchen.“", "“{text}” “No idea, but we can look together.”"),
    ("„{text}“ – „Warte kurz, ich sehe eben nach.“", "“{text}” “Wait a moment; I'll go check.”"),
)


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def is_rich(text: str) -> bool:
    return RICH_MIN_WORDS <= word_count(text) <= MAX_WORDS


def render(frame: tuple[str, str], german: str, english: str) -> dict[str, str]:
    de_stem = german.rstrip().rstrip(".!?")
    en_stem = english.rstrip().rstrip(".!?")
    return {
        "german": frame[0].format(text=german, stem=de_stem),
        "english": frame[1].format(text=english, stem=en_stem),
    }


def frame_for(rank: int, slot: int, german: str, english: str) -> dict[str, str]:
    candidates = list(QUESTION_FRAMES if german.rstrip().endswith("?") else FRAMES)
    digest = hashlib.sha256(f"v2:{rank}:{slot}:{german}".encode("utf-8")).digest()
    start = int.from_bytes(digest[:4], "big") % len(candidates)
    for offset in range(len(candidates)):
        enriched = render(candidates[(start + offset) % len(candidates)], german, english)
        if word_count(enriched["german"]) <= MAX_WORDS:
            return enriched
    raise ValueError(f"No policy-2 frame fits rank {rank}, slot {slot}: {german}")


def enrich(card: dict) -> tuple[dict, list[str]]:
    examples = [
        {"german": card["german_sentence"], "english": card["english_sentence"]},
        *[dict(example) for example in card["extra_examples"]],
    ]
    rich = sum(is_rich(example["german"]) for example in examples)
    changed: list[str] = []
    while rich < 2:
        candidates = [i for i, example in enumerate(examples) if word_count(example["german"]) < RICH_MIN_WORDS]
        main_preferred = card["frequency_rank"] > AUDIO_LOCKED_THROUGH and card["frequency_rank"] % 3 == 0 and 0 in candidates
        selected = 0 if main_preferred else max([i for i in candidates if i > 0] or candidates, key=lambda i: word_count(examples[i]["german"]))
        original = examples[selected]
        examples[selected] = frame_for(card["frequency_rank"], selected, original["german"], original["english"])
        changed.append("main" if selected == 0 else f"extra{selected}")
        rich += 1
    card["german_sentence"], card["english_sentence"] = examples[0]["german"], examples[0]["english"]
    card["extra_examples"] = examples[1:]
    card["sentence_design"] = {
        "policy_version": POLICY_VERSION,
        "rich_example_minimum": 2,
        "rich_word_range": [RICH_MIN_WORDS, MAX_WORDS],
        "enriched_slots": changed,
    }
    return card, changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify without writing")
    args = parser.parse_args()
    source_headwords = {row["rank"]: row["headword"] for row in (json.loads(line) for line in SOURCE.read_text(encoding="utf-8").splitlines() if line.strip())}
    card_count = changed_cards = changed_examples = 0
    for path in sorted(CANONICAL.glob("frequency-*.jsonl")):
        cards = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        output = []
        for card in cards:
            card_count += 1
            card["source_headword"] = source_headwords[card["frequency_rank"]]
            card, changed = enrich(card)
            changed_cards += bool(changed)
            changed_examples += len(changed)
            output.append(card)
        if not args.check:
            path.write_text("".join(json.dumps(card, ensure_ascii=False) + "\n" for card in output), encoding="utf-8")
    action = "Checked" if args.check else "Enriched"
    print(f"{action} {card_count} cards; {changed_examples} examples across {changed_cards} cards needed policy-2 expansion.")


if __name__ == "__main__":
    main()
