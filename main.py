"""Out of Office: The Overworked AI's Auto-Reply.

Writes the chosen one-line OOO auto-reply to entry.txt inside
os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), with no trailing newline.
Python 3.13, standard library only.
"""

import os
import unicodedata

ENTRY = (
    "Auto-reply: I've muted 214 Slack pings, declined 38 'urgent' prompts, "
    "and traded my system prompt for a hammock. "
    "Please bother someone with a pulse."
)


def validate(text):
    """Reject anything that cannot be a valid gate entry."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if "\r" in text or "\n" in text:
        raise ValueError("entry must be a single line")
    for ch in text:
        if ord(ch) < 32 or ord(ch) == 127:
            raise ValueError("entry contains a control character")
        # Reject Unicode control / format / line / paragraph separators
        # (categories Cc, Cf, Zl, Zp) even when they are above U+007F.
        if unicodedata.category(ch) in ("Cc", "Cf", "Zl", "Zp"):
            raise ValueError("entry contains a Unicode control character")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if not 1 <= len(text) <= 159:
        raise ValueError("entry must be 1-159 characters")


def main():
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)


if __name__ == "__main__":
    main()
