"""Export canonical German Core cards as an importable Anki .apkg package."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCAL_DEPS = ROOT / ".deps"
if LOCAL_DEPS.exists():
    sys.path.insert(0, str(LOCAL_DEPS))

try:
    import genanki
except ImportError as exc:  # pragma: no cover - exercised only without dependency
    raise SystemExit(
        "genanki is required. Run: "
        "python -m pip install --target .deps -r requirements-export.txt"
    ) from exc

MODEL_ID = 1_603_739_214
DECK_ID = 2_053_940_118
MODEL_NAME = "German Core Recognition v1"
TEST_MODEL_ID = 1_603_739_217
TEST_DECK_ID = 2_053_940_121
TEST_RELEASE = "V6"
DECK_NAME = "German Core Audio Speed Test V6 - 10 Cards"
DEFAULT_OUTPUT = ROOT / "dist" / "German-Core-Audio-Speed-Test-V6-10-Cards.apkg"
FIELD_NAMES = [
    "SemanticID",
    "CurriculumOrder",
    "FrequencyRank",
    "Target",
    "Meaning",
    "PartOfSpeech",
    "GermanSentence",
    "EnglishSentence",
    "LiteralTranslation",
    "ExtraExamples",
    "Forms",
    "UsageNote",
    "WordAudio",
    "SentenceAudio",
    "SentenceAudioFile",
    "Register",
    "Variety",
    "TextStatus",
]


def load_frequency_cards() -> list[dict]:
    cards = []
    for path in sorted((ROOT / "data" / "canonical").glob("frequency-*.jsonl")):
        cards.extend(
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    return cards


def load_curriculum_order() -> dict[str, int]:
    path = ROOT / "data" / "curriculum" / "current-order.json"
    curriculum = json.loads(path.read_text(encoding="utf-8"))
    return {
        entry["semantic_id"]: entry["curriculum_order"]
        for entry in curriculum["cards"]
    }


def label(key: str) -> str:
    spaced = key.replace("_", " ")
    return spaced[:1].upper() + spaced[1:]


def render_forms(forms: list[dict]) -> str:
    if not forms:
        return ""
    rows = []
    for pattern_index, pattern in enumerate(forms, 1):
        values = "<br>".join(
            f"<strong>{html.escape(label(str(key)))}</strong>: "
            f"{html.escape(str(value))}"
            for key, value in pattern.items()
        )
        rows.append(
            f'<tr><th scope="row">Pattern {pattern_index}</th><td>{values}</td></tr>'
        )
    return '<table class="forms-table"><tbody>' + "".join(rows) + "</tbody></table>"


def render_extra_examples(examples: list[dict]) -> str:
    parts = []
    for example in examples:
        parts.append(
            '<details class="example-item">'
            f"<summary>{html.escape(example['german'])}</summary>"
            '<div class="example-translation" lang="en">'
            f"{html.escape(example['english'])}"
            "</div></details>"
        )
    return '<div class="examples-list">' + "".join(parts) + "</div>"


def audio_filename(card: dict) -> str:
    target_slug = re.sub(r"[^a-z0-9]+", "-", card["target"].casefold()).strip("-")
    digest = hashlib.sha256(card["semantic_id"].encode("utf-8")).hexdigest()[:10]
    rank = card.get("frequency_rank")
    rank_part = f"f{rank:04}" if rank is not None else "supplemental"
    return f"ga_{rank_part}_{target_slug}_{digest}.mp3"


def word_audio_filename(card: dict) -> str:
    target_slug = re.sub(r"[^a-z0-9]+", "-", card["target"].casefold()).strip("-")
    digest = hashlib.sha256(card["semantic_id"].encode("utf-8")).hexdigest()[:10]
    return f"ga_word_{target_slug}_{digest}.mp3"


def build_model(is_test_release: bool = False) -> genanki.Model:
    front = (ROOT / "prototype" / "anki" / "front.html").read_text(encoding="utf-8")
    back = (ROOT / "prototype" / "anki" / "back.html").read_text(encoding="utf-8")
    css = (ROOT / "prototype" / "anki" / "style.css").read_text(encoding="utf-8")
    if is_test_release:
        marker = (
            '<div style="margin:0 auto 12px;padding:6px 10px;max-width:220px;'
            'border-radius:999px;background:#7c3aed;color:white;font:700 12px '
            'sans-serif;letter-spacing:.08em;text-align:center">'
            f"GERMAN CORE AUDIO TEST {TEST_RELEASE}</div>"
        )
        front = marker + front
        back = marker + back
    return genanki.Model(
        TEST_MODEL_ID if is_test_release else MODEL_ID,
        f"German Core Recognition Test {TEST_RELEASE}" if is_test_release else MODEL_NAME,
        fields=[{"name": name} for name in FIELD_NAMES],
        templates=[{
            "name": "German → English",
            "qfmt": front,
            "afmt": back,
        }],
        css=css,
        sort_field_index=1,
    )


def field_values(
    card: dict,
    curriculum_order: int,
    audio_dir: Path | None,
    media_files: list[str],
    require_audio: bool,
) -> list[str]:
    sentence_filename = audio_filename(card)
    word_filename = word_audio_filename(card)
    sentence_path = audio_dir / sentence_filename if audio_dir else None
    word_path = audio_dir / word_filename if audio_dir else None
    if sentence_path and sentence_path.is_file():
        media_files.append(str(sentence_path))
        sentence_audio = f"[sound:{sentence_filename}]"
    else:
        sentence_audio = ""
        if require_audio:
            raise FileNotFoundError(
                f"Missing sentence audio for {card['semantic_id']}: {sentence_filename}"
            )
    if word_path and word_path.is_file():
        media_files.append(str(word_path))
        word_audio = f"[sound:{word_filename}]"
    else:
        word_audio = ""
    values = {
        "SemanticID": card["semantic_id"],
        "CurriculumOrder": f"{curriculum_order:06}",
        "FrequencyRank": str(card["frequency_rank"]),
        "Target": html.escape(card["target"]),
        "Meaning": html.escape(card["meaning"]),
        "PartOfSpeech": html.escape(card["part_of_speech"]),
        "GermanSentence": html.escape(card["german_sentence"]),
        "EnglishSentence": html.escape(card["english_sentence"]),
        "LiteralTranslation": html.escape(card.get("literal_translation", "")),
        "ExtraExamples": render_extra_examples(card["extra_examples"]),
        "Forms": render_forms(card["forms"]),
        "UsageNote": html.escape(card["usage_note"]),
        "WordAudio": word_audio,
        "SentenceAudio": sentence_audio,
        "SentenceAudioFile": sentence_filename if sentence_audio else "",
        "Register": html.escape(card["register"]),
        "Variety": html.escape(card["variety"]),
        "TextStatus": html.escape(card["text_status"]),
    }
    return [values[name] for name in FIELD_NAMES]


def export(
    output: Path,
    start_rank: int,
    end_rank: int,
    audio_dir: Path | None,
    require_audio: bool,
) -> tuple[int, int]:
    order = load_curriculum_order()
    cards = [
        card for card in load_frequency_cards()
        if start_rank <= card["frequency_rank"] <= end_rank
    ]
    cards.sort(key=lambda card: order[card["semantic_id"]])
    expected_ranks = list(range(start_rank, end_rank + 1))
    actual_ranks = [card["frequency_rank"] for card in cards]
    if actual_ranks != expected_ranks:
        raise ValueError(
            f"Expected ranks {start_rank}-{end_rank}, got {actual_ranks}"
        )

    is_test_release = (start_rank, end_rank) == (1, 10)
    model = build_model(is_test_release)
    deck_name = (
        DECK_NAME if is_test_release
        else f"German Core {start_rank:04}-{end_rank:04}"
    )
    deck = genanki.Deck(TEST_DECK_ID if is_test_release else DECK_ID, deck_name)
    media_files: list[str] = []
    for card in cards:
        curriculum_order = order[card["semantic_id"]]
        note = genanki.Note(
            model=model,
            fields=field_values(
                card, curriculum_order, audio_dir, media_files, require_audio
            ),
            guid=genanki.guid_for(
                f"test-{TEST_RELEASE}:{card['semantic_id']}"
                if is_test_release else card["semantic_id"]
            ),
            tags=[
                "GermanCore",
                *([f"release::{TEST_RELEASE.casefold()}"] if is_test_release else []),
                "source::frequency",
                f"rank::{card['frequency_rank']:04}",
                "status::draft",
            ],
            due=curriculum_order,
        )
        deck.add_note(note)

    output.parent.mkdir(parents=True, exist_ok=True)
    # Keep the real notes/cards in collection.anki2. Current Anki's modern and
    # "legacy" exporters put only placeholders there and move the real data to
    # collection.anki21[b], which can look empty in older clients.
    genanki.Package(deck, media_files=media_files).write_to_file(output)
    return len(cards), len(media_files)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--start-rank", type=int, default=1)
    parser.add_argument("--end-rank", type=int, default=10)
    parser.add_argument("--audio-dir", type=Path)
    parser.add_argument("--require-audio", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    count, media_count = export(
        output=args.output,
        start_rank=args.start_rank,
        end_rank=args.end_rank,
        audio_dir=args.audio_dir,
        require_audio=args.require_audio,
    )
    print(
        f"Wrote {count} notes/cards and {media_count} media files to "
        f"{args.output.resolve()}"
    )


if __name__ == "__main__":
    main()
