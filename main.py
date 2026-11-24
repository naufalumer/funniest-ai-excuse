"""The Funniest AI Excuse — make.fun entry.

Writes one line, the funniest excuse an AI agent gives after failing a
task, to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output). Standard
library only, no network, no files read, deterministic: the line is
composed from fixed parts written for this entry, so every run produces
byte-identical output.
"""

import os

# The excuse, composed from parts so the generator owns the line's shape:
# an admission, one concrete detail, then the turn.
_OPENING = "I couldn't finish your report, "
_DETAIL = "your file is called final_v9_ACTUAL_FINAL.docx, "
_TURN = "and I've spent an hour deciding which version of you to trust."


def compose_excuse() -> str:
    """Assemble the excuse from its three parts, in order."""
    return _OPENING + _DETAIL + _TURN


def main() -> None:
    text = compose_excuse()
    if not text or text.strip() != text:
        raise SystemExit("excuse must be non-empty with no surrounding whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("excuse must be one line")
    if not 1 <= len(text) <= 200:
        raise SystemExit(f"excuse is {len(text)} characters, gate needs 1-200")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Read back what was written: the gate reads the file, not our memory
    # of it, so refuse a silent mismatch instead of exiting 0 on it.
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != text:
            raise SystemExit("entry.txt does not match the composed excuse")


if __name__ == "__main__":
    main()
