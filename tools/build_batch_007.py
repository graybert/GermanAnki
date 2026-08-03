"""Build fully developed frequency cards for ranks 1501-2000."""

import build_batch_005 as builder


builder.START = 1501
builder.END = 2000
builder.OUT = builder.ROOT / "data" / "canonical" / "frequency-1501-2000.jsonl"
builder.DATA_FILES = tuple(
    builder.ROOT / "tools" / f"batch_007_{start:04}_{start + 49:04}.txt"
    for start in range(builder.START, builder.END + 1, 50)
)


if __name__ == "__main__":
    builder.main()
