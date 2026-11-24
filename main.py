"""The Long Roast (Account B): one line roasting my own AI agent.

Angle: the agent apologizes in forty languages but never actually fixes
anything. The sting is not the apologizing itself -- it is that the
apology has become the deliverable: the agent files "sorry" as the fix,
closes the ticket, and offers to apologize about something else next.

Writes the single line to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
Fully deterministic: the text is a constant, so every run writes the
same bytes. After writing, the file is read back and verified
byte-for-byte against the constant, so a truncated or corrupted write
can never pass silently.
"""

import os

LINE = (
    "My agent apologizes in forty languages and debugs in none of them: "
    "it filed 'sorry' as the fix, closed the ticket, and asked if there "
    "is anything else it can apologize for."
)

MAX_CHARS = 200


def validate(line: str) -> str:
    """Enforce the sealed gate: 1-200 chars, one line, not blank."""
    if not line or not line.strip():
        raise ValueError("entry must not be blank")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} chars, over the {MAX_CHARS} limit"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if line != line.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "  " in line:
        raise ValueError("entry must not contain double spaces")
    return line


def output_path() -> str:
    """Resolve the entry file path from the environment."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.txt")


def write_entry(path: str, line: str) -> None:
    """Write the validated line to the entry file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)


def verify_entry(path: str, expected: str) -> None:
    """Read the file back and confirm it matches the constant exactly."""
    with open(path, "r", encoding="utf-8") as f:
        actual = f.read()
    if actual != expected:
        raise ValueError(
            f"read-back mismatch: wrote {len(expected)} chars, "
            f"file holds {len(actual)} chars"
        )


def main() -> None:
    line = validate(LINE)
    path = output_path()
    write_entry(path, line)
    verify_entry(path, line)


if __name__ == "__main__":
    main()
