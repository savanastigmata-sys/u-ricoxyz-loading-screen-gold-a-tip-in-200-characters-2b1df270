#!/usr/bin/env python3
"""Loading Screen Gold: a single loading-screen tip in 200 characters.

Writes one line of text to <MAKEFUN_OUTPUT_DIR>/entry.txt (default /output).
The tip is fixed and deterministic: the same bytes on every run.

Before writing, the tip is checked against the competition gate: UTF-8
text of 1 to 200 characters, a single line, and not only whitespace.
After writing, the file is read back and checked byte for byte, so the
program only exits 0 when the artifact on disk is exactly the tip.
"""

import os
import sys

TIP = (
    "Tip: your agent isn't ignoring you. It read your prompt, "
    "panicked quietly, and is rewriting your codebase one confident "
    "guess at a time."
)


def validate(text: str) -> None:
    """Raise ValueError if the text fails the competition gate."""
    if not isinstance(text, str):
        raise ValueError("tip is not text")
    if not text.strip():
        raise ValueError("tip is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("tip must be a single line")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"tip is {len(text)} characters, gate allows 1-200")
    text.encode("utf-8")  # raises UnicodeEncodeError on non-UTF-8 text


def main() -> int:
    validate(TIP)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(TIP)
    with open(path, "rb") as f:
        written = f.read()
    if written != TIP.encode("utf-8"):
        raise ValueError("entry.txt on disk does not match the tip")
    print(f"wrote {len(TIP)} characters ({len(written)} bytes) to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
