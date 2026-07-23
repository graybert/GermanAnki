"""Import a package into an isolated current-Anki collection and validate it."""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCAL_DEPS = ROOT / ".deps"
if LOCAL_DEPS.exists():
    sys.path.insert(0, str(LOCAL_DEPS))

try:
    from anki.collection import Collection
    from anki.import_export_pb2 import (
        ImportAnkiPackageOptions,
        ImportAnkiPackageRequest,
    )
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Anki's current backend is required. Run: "
        "python -m pip install --target .deps -r requirements-export.txt"
    ) from exc


SOUND_RE = re.compile(r"\[sound:([^\]]+)\]")


def validate(
    path: Path,
    expected_notes: int,
    expected_deck: str | None = None,
    required_rendered_text: str | None = None,
) -> None:
    errors = []
    with zipfile.ZipFile(path) as package:
        names = set(package.namelist())
        if "collection.anki2" not in names:
            errors.append("missing legacy-compatible collection.anki2 database")
        if "media" not in names:
            errors.append("missing media map")
        if "collection.anki2" in names:
            with tempfile.TemporaryDirectory() as database_temp:
                database_path = Path(database_temp) / "collection.anki2"
                database_path.write_bytes(package.read("collection.anki2"))
                database = sqlite3.connect(database_path)
                try:
                    legacy_notes = database.execute(
                        "SELECT count(*) FROM notes"
                    ).fetchone()[0]
                    legacy_cards = database.execute(
                        "SELECT count(*) FROM cards"
                    ).fetchone()[0]
                finally:
                    database.close()
                if legacy_notes != expected_notes:
                    errors.append(
                        f"compatibility database contains {legacy_notes} notes, "
                        f"expected {expected_notes}"
                    )
                if legacy_cards != expected_notes:
                    errors.append(
                        f"compatibility database contains {legacy_cards} cards, "
                        f"expected {expected_notes}"
                    )

    with tempfile.TemporaryDirectory() as temp_dir:
        collection = Collection(str(Path(temp_dir) / "collection.anki2"))
        try:
            result = collection.import_anki_package(
                ImportAnkiPackageRequest(
                    package_path=str(path.resolve()),
                    options=ImportAnkiPackageOptions(
                        merge_notetypes=True,
                        with_scheduling=False,
                        with_deck_configs=False,
                    ),
                )
            )
            if len(result.log.new) != expected_notes:
                errors.append(
                    f"current Anki imported {len(result.log.new)} of "
                    f"{expected_notes} expected notes"
                )
            for category in (
                "conflicting",
                "missing_notetype",
                "missing_deck",
                "empty_first_field",
            ):
                count = len(getattr(result.log, category))
                if count:
                    errors.append(f"Anki import reported {count} {category} notes")
            note_ids = collection.find_notes("")
            card_ids = collection.find_cards("")
            if len(note_ids) != expected_notes:
                errors.append(f"expected {expected_notes} notes, found {len(note_ids)}")
            if len(card_ids) != expected_notes:
                errors.append(f"expected {expected_notes} cards, found {len(card_ids)}")
            field_counts = {
                len(collection.get_note(note_id).fields) for note_id in note_ids
            }
            if field_counts != {18}:
                errors.append(f"unexpected note field counts: {sorted(field_counts)}")
            for card_id in card_ids:
                card = collection.get_card(card_id)
                question = card.question()
                answer = card.answer()
                if not question.strip():
                    errors.append(f"card {card_id} has an empty rendered question")
                if not answer.strip():
                    errors.append(f"card {card_id} has an empty rendered answer")
                if required_rendered_text and (
                    required_rendered_text not in question
                    or required_rendered_text not in answer
                ):
                    errors.append(
                        f"card {card_id} does not render required text "
                        f"{required_rendered_text!r} on both sides"
                    )
            sound_files = {
                filename
                for note_id in note_ids
                for field in collection.get_note(note_id).fields
                for filename in SOUND_RE.findall(field)
            }
            media_dir = Path(collection.media.dir())
            packaged_media = {
                name for name in os.listdir(media_dir)
                if (media_dir / name).is_file()
            }
            if sound_files != packaged_media:
                errors.append(
                    "sound field references do not match imported media files"
                )
            matching_models = [
                item for item in collection.models.all_names_and_ids()
                if item.name.startswith("German Core Recognition")
            ]
            if len(matching_models) != 1:
                errors.append("expected one German Core Recognition note model")
            if expected_deck:
                matching_decks = [
                    item for item in collection.decks.all_names_and_ids()
                    if item.name == expected_deck
                ]
                if len(matching_decks) != 1:
                    errors.append(f"expected deck named {expected_deck!r}")
        finally:
            collection.close()

    if errors:
        raise SystemExit("\n".join(errors))
    print(
        f"Validated {path}: {expected_notes} notes, {expected_notes} cards, "
        f"{len(packaged_media)} media files, current-Anki import and rendering pass."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--expected-notes", type=int, required=True)
    parser.add_argument("--expected-deck")
    parser.add_argument("--required-rendered-text")
    args = parser.parse_args()
    validate(
        args.path,
        args.expected_notes,
        args.expected_deck,
        args.required_rendered_text,
    )


if __name__ == "__main__":
    main()
