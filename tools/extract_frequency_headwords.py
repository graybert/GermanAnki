"""Extract rank, headword, and coarse POS from the local reference PDF.

Dictionary definitions and examples are intentionally discarded. The output is
curriculum metadata only and is not a public reproduction of the source text.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "Source Materials" / "German Frequency Dictionary.pdf"
OUTPUT = ROOT / "data" / "source" / "frequency-all-5009.jsonl"
FINAL_RANK = 5009
POS_MARKERS = ("art", "aux", "conj", "inf", "interj", "num", "part", "prep", "pron", "verb", "adj", "adv")


def parse_label(text: str) -> tuple[str, str]:
    text = " ".join(text.split())
    candidates: list[tuple[int, str]] = []
    for pos in POS_MARKERS:
        match = re.search(rf"\s{pos}(?:\s|$)", text)
        if match:
            candidates.append((match.start(), pos))
    for article in ("der", "die", "das"):
        match = re.search(rf"\s{article}(?:,\s*(?:der|die|das))*\s", text)
        if match:
            candidates.append((match.start(), "noun"))
    if not candidates:
        return text.split()[0], "unknown"
    index, pos = min(candidates)
    return text[:index].strip(), pos


def main() -> None:
    reader = PdfReader(PDF)
    records: list[dict[str, object]] = []
    expected = 1
    # PDF indices 19..254 contain the complete continuous ranked section.
    for page_index in range(19, 255):
        text = reader.pages[page_index].extract_text() or ""
        lines = text.splitlines()
        for line in lines:
            match = re.match(r"^\s*(\d{1,4})\s+(.+?)\s*$", line)
            if not match or int(match.group(1)) != expected:
                continue
            headword, pos = parse_label(match.group(2))
            records.append({
                "rank": expected,
                "headword": headword,
                "source_pos": pos,
                "source_page": page_index + 1,
            })
            expected += 1
            if expected == FINAL_RANK + 1:
                break
        if expected == FINAL_RANK + 1:
            break

    if expected != FINAL_RANK + 1:
        print(
            f"Extraction stopped before rank {FINAL_RANK} "
            f"(next expected: {expected}).",
            file=sys.stderr,
        )
        raise SystemExit(1)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    print(f"Wrote {len(records)} headwords to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
