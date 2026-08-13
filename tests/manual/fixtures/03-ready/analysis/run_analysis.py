"""Generate a deterministic synthetic summary for the test fixture."""

from pathlib import Path


def main() -> None:
    output = Path("outputs/pollinator-summary.txt")
    output.parent.mkdir(exist_ok=True)
    output.write_text("synthetic observation count: 12\n", encoding="utf-8")


if __name__ == "__main__":
    main()
