"""Build fully developed frequency cards for ranks 1001-1500."""

import build_batch_005 as builder


builder.START = 1001
builder.END = 1500
builder.OUT = builder.ROOT / "data" / "canonical" / "frequency-1001-1500.jsonl"
builder.DATA_FILES = tuple(
    builder.ROOT / "tools" / f"batch_006_{start:04}_{start + 49:04}.txt"
    for start in range(builder.START, builder.END + 1, 50)
)


if __name__ == "__main__":
    builder.main()
