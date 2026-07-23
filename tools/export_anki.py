"""Export canonical German Core cards as an importable Anki .apkg package."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import tempfile
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

try:
    from anki.collection import Collection
    from anki.import_export_pb2 import (
        ExportAnkiPackageOptions,
        ExportLimit,
        ImportAnkiPackageOptions,
        ImportAnkiPackageRequest,
    )
except ImportError as exc:  # pragma: no cover - exercised only without dependency
    raise SystemExit(
        "Anki's current backend is required. Run: "
        "python -m pip install --target .deps -r requirements-export.txt"
    ) from exc


MODEL_ID = 1_603_739_214
DECK_ID = 2_053_940_118
MODEL_NAME = "German Core Recognition v1"
DECK_NAME = "German Core Test 0001-0010"
DEFAULT_OUTPUT = ROOT / "dist" / "German-Core-Test-0001-0010-v2.apkg"
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
    "SentenceAudio",
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


def build_model() -> genanki.Model:
    front = (ROOT / "prototype" / "anki" / "front.html").read_text(encoding="utf-8")
    back = (ROOT / "prototype" / "anki" / "back.html").read_text(encoding="utf-8")
    css = (ROOT / "prototype" / "anki" / "style.css").read_text(encoding="utf-8")
    return genanki.Model(
        MODEL_ID,
        MODEL_NAME,
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
    filename = audio_filename(card)
    audio_path = audio_dir / filename if audio_dir else None
    if audio_path and audio_path.is_file():
        media_files.append(str(audio_path))
        sentence_audio = f"[sound:{filename}]"
    else:
        sentence_audio = ""
        if require_audio:
            raise FileNotFoundError(f"Missing audio for {card['semantic_id']}: {filename}")
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
        "SentenceAudio": sentence_audio,
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

    model = build_model()
    deck_name = (
        DECK_NAME if (start_rank, end_rank) == (1, 10)
        else f"German Core {start_rank:04}-{end_rank:04}"
    )
    deck = genanki.Deck(DECK_ID, deck_name)
    media_files: list[str] = []
    for card in cards:
        curriculum_order = order[card["semantic_id"]]
        note = genanki.Note(
            model=model,
            fields=field_values(
                card, curriculum_order, audio_dir, media_files, require_audio
            ),
            guid=genanki.guid_for(card["semantic_id"]),
            tags=[
                "GermanCore",
                "source::frequency",
                f"rank::{card['frequency_rank']:04}",
                "status::draft",
            ],
            due=curriculum_order,
        )
        deck.add_note(note)

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        seed_path = Path(temp_dir) / "legacy-seed.apkg"
        collection_path = Path(temp_dir) / "collection.anki2"
        genanki.Package(deck, media_files=media_files).write_to_file(seed_path)
        collection = Collection(str(collection_path))
        try:
            result = collection.import_anki_package(
                ImportAnkiPackageRequest(
                    package_path=str(seed_path),
                    options=ImportAnkiPackageOptions(
                        merge_notetypes=True,
                        with_scheduling=False,
                        with_deck_configs=False,
                    ),
                )
            )
            imported_count = len(result.log.new)
            if imported_count != len(cards):
                raise RuntimeError(
                    f"Anki imported {imported_count} of {len(cards)} seed notes"
                )
            deck_id = collection.decks.id_for_name(deck_name)
            if deck_id is None:
                raise RuntimeError(f"Imported deck not found: {deck_name}")
            exported_count = collection.export_anki_package(
                out_path=str(output.resolve()),
                options=ExportAnkiPackageOptions(
                    with_scheduling=False,
                    with_deck_configs=False,
                    with_media=True,
                    legacy=False,
                ),
                limit=ExportLimit(deck_id=deck_id),
            )
            if exported_count != len(cards):
                raise RuntimeError(
                    f"Anki exported {exported_count} of {len(cards)} notes"
                )
        finally:
            collection.close()
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
