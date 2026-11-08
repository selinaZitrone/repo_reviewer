"""Entry point: build the site table, summarise it, and write the result."""

from pathlib import Path

from prepare import surveyed_sites
from summarise import expected_observations, format_summary


def main() -> None:
    summary = format_summary(expected_observations(surveyed_sites()))
    # Relative to the repository root, which the README says to run from.
    output = Path("outputs/pollinator-summary.txt")
    output.parent.mkdir(exist_ok=True)
    output.write_text(summary, encoding="utf-8")


if __name__ == "__main__":
    main()
