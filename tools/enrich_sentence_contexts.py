"""Deterministically ensure each frequency card has two rich examples.

Short, idiomatic examples remain valuable, so this does not lengthen every
sentence.  It preserves existing examples and wraps only as many as needed to
give each card at least two examples in the 9-20 word range.  Ranks 1-10 keep
their main sentences unchanged because paid audio already exists for them.
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
POLICY_VERSION = 1
RICH_MIN_WORDS = 9
MAX_WORDS = 20
AUDIO_LOCKED_THROUGH = 10

WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüß]+")

# These paired frames are intentionally broad enough to hold statements,
# questions, commands, and exclamations without changing the original clause.
STATEMENT_FRAMES = (
    ("Nach kurzem Zögern sagte Ava: „{text}“", "After hesitating briefly, Ava said, “{text}”"),
    ("Beim Abendessen erklärte ihr Vater ruhig: „{text}“", "During dinner, her father explained calmly, “{text}”"),
    ("Vor Unterrichtsbeginn schrieb die Lehrerin an die Tafel: „{text}“", "Before class began, the teacher wrote on the board, “{text}”"),
    ("Im Podcast fasste die Moderatorin den Punkt so zusammen: „{text}“", "In the podcast, the host summarized the point like this: “{text}”"),
    ("In den Abendnachrichten hieß es dazu: „{text}“", "The evening news reported the following about it: “{text}”"),
    ("Auf der Informationstafel im Museum steht: „{text}“", "The information panel in the museum says, “{text}”"),
    ("Im Naturfilm erklärt der Sprecher: „{text}“", "In the nature documentary, the narrator explains, “{text}”"),
    ("Im Epilog erinnert sich die Erzählerin: „{text}“", "In the epilogue, the narrator recalls, “{text}”"),
    ("In der letzten Szene flüstert die Hauptfigur: „{text}“", "In the final scene, the main character whispers, “{text}”"),
    ("Während alle zuhörten, sagte der Projektleiter: „{text}“", "While everyone listened, the project manager said, “{text}”"),
    ("Am Ende der Besprechung stellte Mia klar: „{text}“", "At the end of the meeting, Mia made it clear: “{text}”"),
    ("In seinem Brief schrieb der Großvater: „{text}“", "In his letter, the grandfather wrote, “{text}”"),
    ("Die Ärztin sah von ihren Notizen auf: „{text}“", "The doctor looked up from her notes: “{text}”"),
    ("Kurz vor Sendeschluss sagte der Reporter: „{text}“", "Shortly before the broadcast ended, the reporter said, “{text}”"),
    ("In der Sprechblase über der Figur steht: „{text}“", "The speech bubble above the character says, “{text}”"),
    ("Als es im Raum still wurde, begann Nora: „{text}“", "When the room fell silent, Nora began: “{text}”"),
    ("Im Gespräch mit ihrer Tochter sagte die Mutter: „{text}“", "While talking with her daughter, the mother said, “{text}”"),
    ("Der Reiseführer blieb vor dem alten Gebäude stehen: „{text}“", "The guide stopped in front of the old building: “{text}”"),
    ("Am Mikrofon erklärte der Gast seine Sicht: „{text}“", "At the microphone, the guest explained his view: “{text}”"),
    ("Die Überschrift des Artikels lautet: „{text}“", "The article's headline reads, “{text}”"),
)

QUESTION_FRAMES = (
    ("Nach kurzem Zögern fragte Ava: „{text}“", "After hesitating briefly, Ava asked, “{text}”"),
    ("Beim Abendessen wollte ihr Vater wissen: „{text}“", "During dinner, her father wanted to know, “{text}”"),
    ("Zu Beginn der Stunde fragte die Lehrerin: „{text}“", "At the beginning of class, the teacher asked, “{text}”"),
    ("Im Podcast stellte die Moderatorin eine einfache Frage: „{text}“", "In the podcast, the host asked a simple question: “{text}”"),
    ("Der Reporter hielt dem Minister das Mikrofon hin: „{text}“", "The reporter held the microphone toward the minister: “{text}”"),
    ("Vor der Informationstafel fragte ein Besucher: „{text}“", "In front of the information panel, a visitor asked, “{text}”"),
    ("Während der Naturfilm lief, fragte das Kind: „{text}“", "While the nature documentary played, the child asked, “{text}”"),
    ("Im letzten Kapitel fragt sich die Erzählerin: „{text}“", "In the final chapter, the narrator wonders, “{text}”"),
    ("In der letzten Szene fragt die Hauptfigur: „{text}“", "In the final scene, the main character asks, “{text}”"),
    ("Während alle zuhörten, fragte der Projektleiter: „{text}“", "While everyone listened, the project manager asked, “{text}”"),
    ("Am Ende der Besprechung wollte Mia wissen: „{text}“", "At the end of the meeting, Mia wanted to know, “{text}”"),
    ("In seinem Brief stellte der Großvater eine Frage: „{text}“", "In his letter, the grandfather asked a question: “{text}”"),
    ("Die Ärztin sah von ihren Notizen auf: „{text}“", "The doctor looked up from her notes: “{text}”"),
    ("Kurz vor Sendeschluss fragte der Reporter: „{text}“", "Shortly before the broadcast ended, the reporter asked, “{text}”"),
    ("In der Sprechblase über der Figur steht die Frage: „{text}“", "The speech bubble above the character contains the question: “{text}”"),
    ("Als es im Raum still wurde, fragte Nora: „{text}“", "When the room fell silent, Nora asked, “{text}”"),
)

EXCLAMATION_FRAMES = (
    ("Plötzlich rief Ava durch den ganzen Raum: „{text}“", "Suddenly, Ava called across the entire room, “{text}”"),
    ("Beim Abendessen sagte ihr Vater mit Nachdruck: „{text}“", "During dinner, her father said emphatically, “{text}”"),
    ("Kurz vor der Pause rief die Lehrerin: „{text}“", "Just before the break, the teacher called out, “{text}”"),
    ("Im Podcast wiederholte die Moderatorin den entscheidenden Satz: „{text}“", "In the podcast, the host repeated the crucial sentence: “{text}”"),
    ("Der Reporter wandte sich direkt an die Kamera: „{text}“", "The reporter turned directly toward the camera: “{text}”"),
    ("Vor der Informationstafel rief ein Besucher: „{text}“", "In front of the information panel, a visitor called out, “{text}”"),
    ("Während der Naturfilm lief, rief das Kind begeistert: „{text}“", "While the nature documentary played, the child exclaimed excitedly, “{text}”"),
    ("Im letzten Kapitel ruft die Erzählerin: „{text}“", "In the final chapter, the narrator exclaims, “{text}”"),
    ("In der letzten Szene ruft die Hauptfigur: „{text}“", "In the final scene, the main character calls out, “{text}”"),
    ("Während alle zuhörten, warnte der Projektleiter: „{text}“", "While everyone listened, the project manager warned, “{text}”"),
    ("Am Ende der Besprechung sagte Mia entschieden: „{text}“", "At the end of the meeting, Mia said firmly, “{text}”"),
    ("Die Ärztin sah von ihren Notizen auf: „{text}“", "The doctor looked up from her notes: “{text}”"),
)

TOPIC_KEYWORDS = {
    "work": ("arbeit", "büro", "firma", "projekt", "kolleg", "chef", "kund", "besprech", "vertrag", "sitzung"),
    "school": ("schule", "unterricht", "lehrer", "lehrerin", "lernen", "prüfung", "aufgabe", "student", "universität"),
    "news": ("regierung", "minister", "polizei", "gesetz", "wahl", "präsident", "polit", "bericht", "offiziell"),
    "museum": ("museum", "kunst", "gemälde", "ausstellung", "jahrhundert", "histor", "denkmal", "archäolog"),
    "nature": ("wald", "tier", "vogel", "pflanze", "baum", "meer", "fluss", "umwelt", "natur", "wetter"),
    "family": ("kind", "mutter", "vater", "eltern", "familie", "tochter", "sohn", "geburtstag", "großmutter", "großvater"),
    "medical": ("arzt", "ärztin", "krank", "gesund", "schmerz", "körper", "haut", "medizin", "patient"),
    "travel": ("zug", "bahn", "bus", "hotel", "reise", "flug", "flughafen", "bahnhof", "tourist", "reiseführer"),
}

# Frame indexes safe for any subject plus indexes whose setting is appropriate
# when the embedded sentence contains a matching topic cue.
FRAME_POOLS = {
    "statement": {
        "generic": (0, 7, 8, 9, 11, 12, 14, 15, 16, 18, 19),
        "work": (9, 10, 18), "school": (2,), "news": (3, 4, 13, 19),
        "museum": (5, 17), "nature": (6,), "family": (1, 11, 16),
        "medical": (12,), "travel": (17,),
    },
    "question": {
        "generic": (0, 3, 7, 8, 9, 11, 12, 14, 15),
        "work": (9, 10), "school": (2,), "news": (3, 4, 13),
        "museum": (5,), "nature": (6,), "family": (1, 11),
        "medical": (12,), "travel": (5,),
    },
    "exclamation": {
        "generic": (0, 3, 7, 8, 9, 10, 11),
        "work": (9, 10), "school": (2,), "news": (3, 4),
        "museum": (5,), "nature": (6,), "family": (1,),
        "medical": (11,), "travel": (0,),
    },
}

LEADS = (
    ("Nach kurzem Zögern", "After hesitating briefly"),
    ("Am Ende des Gesprächs", "At the end of the conversation"),
    ("Als es im Raum still wurde,", "When the room fell silent"),
    ("Nachdem alle Platz genommen hatten,", "After everyone had taken a seat"),
    ("Bevor das Gespräch zu Ende ging,", "Before the conversation ended"),
    ("Während die Aufnahme weiterlief,", "While the recording continued"),
    ("Obwohl die Zeit langsam knapp wurde,", "Although time was slowly running short"),
    ("Sobald die Kamera wieder eingeschaltet war,", "As soon as the camera was switched on again"),
    ("Weil noch eine Erklärung fehlte,", "Because an explanation was still missing"),
    ("Als die Diskussion wieder begann,", "When the discussion resumed"),
    ("Nachdem die Unterlagen verteilt worden waren,", "After the documents had been handed out"),
    ("Während draußen leise der Regen fiel,", "While rain fell quietly outside"),
    ("Kurz vor der nächsten Pause", "Shortly before the next break"),
    ("Zu Beginn der zweiten Runde", "At the beginning of the second round"),
    ("Nach einem langen Moment des Schweigens", "After a long moment of silence"),
    ("Unter dem Eindruck der neuen Informationen", "Under the impact of the new information"),
    ("Ohne noch einmal in die Notizen zu schauen,", "Without looking at the notes again"),
    ("Bevor jemand eine weitere Frage stellen konnte,", "Before anyone could ask another question"),
    ("Als die Tür hinter ihnen zufiel,", "When the door closed behind them"),
    ("Nachdem die Verbindung wiederhergestellt worden war,", "After the connection had been restored"),
    ("Im Laufe der weiteren Diskussion", "As the discussion continued"),
    ("Nach einer kurzen Unterbrechung", "After a brief interruption"),
    ("Während alle aufmerksam zuhörten,", "While everyone listened attentively"),
    ("Als der entscheidende Moment gekommen war,", "When the decisive moment had arrived"),
)

STATEMENT_ACTIONS = (
    ("sagte Ava schließlich", "Ava finally said"),
    ("fasste Mia ihren Gedanken zusammen", "Mia summarized her thought"),
    ("las Nora den Satz vor", "Nora read the sentence aloud"),
    ("erklärte der Gast seinen Standpunkt", "the guest explained his position"),
    ("wiederholte Leo die entscheidenden Worte", "Leo repeated the crucial words"),
    ("zitierte der Moderator eine frühere Aussage", "the host quoted an earlier statement"),
    ("erinnerte sich die Erzählerin an den Satz", "the narrator recalled the sentence"),
    ("schrieb der Reporter in sein Notizbuch", "the reporter wrote in his notebook"),
    ("antwortete Klara ohne zu zögern", "Klara answered without hesitation"),
    ("brachte der Gast sein Argument auf den Punkt", "the guest summed up his argument"),
    ("fügte Jonas noch einen Gedanken hinzu", "Jonas added one more thought"),
    ("formulierte Lina ihre Antwort sorgfältig", "Lina worded her answer carefully"),
)

QUESTION_ACTIONS = (
    ("fragte Ava schließlich", "Ava finally asked"),
    ("wollte Mia genauer wissen", "Mia wanted to know more precisely"),
    ("las Nora die Frage vor", "Nora read the question aloud"),
    ("wandte sich der Gast an die Runde", "the guest addressed the group"),
    ("stellte der Moderator die nächste Frage", "the host asked the next question"),
    ("hob Leo die Hand und fragte", "Leo raised his hand and asked"),
    ("stellte sich die Erzählerin eine Frage", "the narrator asked herself a question"),
    ("blickte die Reporterin in die Kamera", "the reporter looked into the camera"),
    ("fragte Klara ohne zu zögern", "Klara asked without hesitation"),
    ("bat Jonas die anderen um eine Antwort", "Jonas asked the others for an answer"),
)

EXCLAMATION_ACTIONS = (
    ("rief Ava plötzlich", "Ava suddenly called out"),
    ("sagte Mia mit Nachdruck", "Mia said emphatically"),
    ("las Nora den Ausruf vor", "Nora read the exclamation aloud"),
    ("wandte sich der Gast an die Runde", "the guest addressed the group"),
    ("wiederholte der Moderator die Warnung", "the host repeated the warning"),
    ("rief Leo durch den Raum", "Leo called across the room"),
    ("erinnerte sich die Erzählerin an den Ruf", "the narrator recalled the shout"),
    ("blickte die Reporterin direkt in die Kamera", "the reporter looked directly into the camera"),
    ("warnte Klara die anderen", "Klara warned the others"),
)

TOPIC_ACTIONS = {
    "work": ("stellte die Projektleiterin klar", "the project manager made it clear"),
    "school": ("notierte die Lehrerin ein Beispiel", "the teacher wrote down an example"),
    "news": ("fasste die Reporterin die Meldung zusammen", "the reporter summarized the news item"),
    "museum": ("zitierte der Audioguide einen Zeitzeugen", "the audio guide quoted a witness"),
    "nature": ("erklärte die Sprecherin des Naturfilms", "the nature documentary's narrator explained"),
    "family": ("fügte der Vater ruhig hinzu", "the father added calmly"),
    "medical": ("sagte die Ärztin mit ruhiger Stimme", "the doctor said in a calm voice"),
    "travel": ("erklärte der Reiseführer der Gruppe", "the guide explained to the group"),
}


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def is_rich(text: str) -> bool:
    return RICH_MIN_WORDS <= word_count(text) <= MAX_WORDS


def frame_for(rank: int, slot: int, german: str) -> tuple[str, str]:
    if german.rstrip().endswith("?"):
        actions = list(QUESTION_ACTIONS)
    elif german.rstrip().endswith("!") or german.lstrip().startswith(("Bitte ", "Komm ", "Gehen ", "Nimm ")):
        actions = list(EXCLAMATION_ACTIONS)
    else:
        actions = list(STATEMENT_ACTIONS)
    lowered = german.casefold()
    topics = [
        topic for topic, keywords in TOPIC_KEYWORDS.items()
        if any(keyword in lowered for keyword in keywords)
    ]
    for topic in topics:
        actions.append(TOPIC_ACTIONS[topic])
    digest = hashlib.sha256(f"{rank}:{slot}:{german}".encode("utf-8")).digest()
    start = int.from_bytes(digest[:4], "big")
    for offset in range(len(LEADS) * len(actions)):
        lead_de, lead_en = LEADS[(start + offset) % len(LEADS)]
        action_de, action_en = actions[((start // len(LEADS)) + offset) % len(actions)]
        de = f"{lead_de} {action_de}: „{{text}}“"
        if word_count(de.format(text=german)) <= MAX_WORDS:
            return de, f"{lead_en}, {action_en}, “{{text}}”"
    raise ValueError(f"No sentence frame fits rank {rank}, slot {slot}")


def enrich(card: dict) -> tuple[dict, list[str]]:
    previous_slots = card.get("sentence_design", {}).get("enriched_slots", [])
    examples = [
        {"german": card["german_sentence"], "english": card["english_sentence"]},
        *[dict(example) for example in card["extra_examples"]],
    ]
    rich = sum(is_rich(example["german"]) for example in examples)
    changed: list[str] = []
    while rich < 2:
        candidates = [
            index for index, example in enumerate(examples)
            if not is_rich(example["german"])
            and word_count(example["german"]) < RICH_MIN_WORDS
        ]
        main_preferred = (
            card["frequency_rank"] > AUDIO_LOCKED_THROUGH
            and card["frequency_rank"] % 3 == 0
            and 0 in candidates
        )
        if main_preferred:
            selected = 0
        else:
            extras = [index for index in candidates if index > 0]
            selected = max(extras or candidates, key=lambda i: word_count(examples[i]["german"]))
        original = examples[selected]
        de_frame, en_frame = frame_for(card["frequency_rank"], selected, original["german"])
        enriched = {
            "german": de_frame.format(text=original["german"]),
            "english": en_frame.format(text=original["english"]),
        }
        if word_count(enriched["german"]) > MAX_WORDS:
            raise ValueError(
                f"Rank {card['frequency_rank']} enrichment exceeds {MAX_WORDS} words: "
                f"{enriched['german']}"
            )
        examples[selected] = enriched
        changed.append("main" if selected == 0 else f"extra{selected}")
        rich += 1
    card["german_sentence"] = examples[0]["german"]
    card["english_sentence"] = examples[0]["english"]
    card["extra_examples"] = examples[1:]
    card["sentence_design"] = {
        "policy_version": POLICY_VERSION,
        "rich_example_minimum": 2,
        "rich_word_range": [RICH_MIN_WORDS, MAX_WORDS],
        "enriched_slots": list(dict.fromkeys([*previous_slots, *changed])),
    }
    return card, changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify without writing")
    args = parser.parse_args()
    source_headwords = {
        row["rank"]: row["headword"]
        for row in (
            json.loads(line)
            for line in SOURCE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }
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
            path.write_text(
                "".join(json.dumps(card, ensure_ascii=False) + "\n" for card in output),
                encoding="utf-8",
            )
    action = "Checked" if args.check else "Enriched"
    print(
        f"{action} {card_count} cards; {changed_examples} examples across "
        f"{changed_cards} cards needed deterministic context expansion."
    )


if __name__ == "__main__":
    main()
