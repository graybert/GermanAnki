"""Inspect a generated Anki package without importing it into a user collection."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import tempfile
import zipfile
from pathlib import Path


FIELD_SEPARATOR = "\x1f"
SOUND_RE = re.compile(r"\[sound:([^\]]+)\]")


def validate(path: Path, expected_notes: int) -> None:
    errors = []
    with zipfile.ZipFile(path) as package:
        names = package.namelist()
        if "collection.anki2" not in names:
            errors.append("missing collection.anki2")
        if "media" not in names:
            errors.append("missing media map")
        media_map = json.loads(package.read("media"))
        mapped_entries = set(media_map)
        archive_media_entries = set(names) - {"collection.anki2", "media"}
        if mapped_entries != archive_media_entries:
            errors.append("media map does not match packaged media files")
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "collection.anki2"
            database_path.write_bytes(package.read("collection.anki2"))
            connection = sqlite3.connect(database_path)
            cursor = connection.cursor()
            integrity = cursor.execute("PRAGMA integrity_check").fetchone()[0]
            if integrity != "ok":
                errors.append(f"SQLite integrity check failed: {integrity}")
            note_count = cursor.execute("SELECT count(*) FROM notes").fetchone()[0]
            card_count = cursor.execute("SELECT count(*) FROM cards").fetchone()[0]
            if note_count != expected_notes:
                errors.append(f"expected {expected_notes} notes, found {note_count}")
            if card_count != expected_notes:
                errors.append(f"expected {expected_notes} cards, found {card_count}")
            guids = [row[0] for row in cursor.execute("SELECT guid FROM notes")]
            if len(guids) != len(set(guids)):
                errors.append("duplicate note GUIDs")
            note_rows = list(cursor.execute("SELECT flds FROM notes"))
            field_counts = [len(row[0].split(FIELD_SEPARATOR)) for row in note_rows]
            if set(field_counts) != {16}:
                errors.append(f"unexpected note field counts: {sorted(set(field_counts))}")
            sound_files = {
                filename
                for row in note_rows
                for filename in SOUND_RE.findall(row[0])
            }
            packaged_media = set(media_map.values())
            if sound_files != packaged_media:
                errors.append(
                    "sound field references do not match packaged media names"
                )
            collection = cursor.execute("SELECT models, decks FROM col").fetchone()
            models = json.loads(collection[0])
            decks = json.loads(collection[1])
            if len(models) != 1:
                errors.append(f"expected 1 note model, found {len(models)}")
            if len(decks) < 1:
                errors.append("package contains no deck")
            connection.close()

    if errors:
        raise SystemExit("\n".join(errors))
    print(
        f"Validated {path}: {expected_notes} notes, {expected_notes} cards, "
        f"{len(packaged_media)} media files, valid SQLite and media map."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--expected-notes", type=int, required=True)
    args = parser.parse_args()
    validate(args.path, args.expected_notes)


if __name__ == "__main__":
    main()
