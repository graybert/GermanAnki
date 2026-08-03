"""Build fully developed frequency cards for ranks 2001-2500."""

import build_batch_005 as builder


builder.START = 2001
builder.END = 2500
builder.OUT = builder.ROOT / "data" / "canonical" / "frequency-2001-2500.jsonl"
builder.DATA_FILES = tuple(
    builder.ROOT / "tools" / f"batch_008_{start:04}_{start + 49:04}.txt"
    for start in range(builder.START, builder.END + 1, 50)
)


if __name__ == "__main__":
    builder.main()
