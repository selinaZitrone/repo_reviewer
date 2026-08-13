#!/usr/bin/env python3
"""Run the fast repo-reviewer development checks and build the local skill.

Optionally collect deterministic evidence for one or all shared manual fixtures.
This command never runs code from a fixture repository.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(command: list[str], cwd: Path) -> None:
    print(f"\n> {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def fixture_names(fixtures_dir: Path) -> list[str]:
    return sorted(path.name for path in fixtures_dir.iterdir() if path.is_dir())


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    fixtures_dir = root / "tests" / "manual" / "fixtures"
    names = fixture_names(fixtures_dir)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        default="dev",
        help="Version stamped into the generated skill (default: dev).",
    )
    parser.add_argument(
        "--fixture",
        choices=[*names, "all"],
        help="Also write deterministic evidence JSON for this fixture (or all).",
    )
    args = parser.parse_args()

    try:
        run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], root)
        run(
            [
                sys.executable,
                "tools/compile_skill.py",
                "--version",
                args.version,
            ],
            root,
        )

        selected = names if args.fixture == "all" else ([args.fixture] if args.fixture else [])
        for name in selected:
            fixture = fixtures_dir / name
            output = root / "build" / "manual-evidence" / f"{name}.json"
            run(
                [
                    sys.executable,
                    "build/repo-reviewer/scripts/collect_repository_evidence.py",
                    str(fixture),
                    "--out",
                    str(output),
                ],
                root,
            )
    except subprocess.CalledProcessError as error:
        print(f"\nDevelopment check stopped (exit {error.returncode}).", file=sys.stderr)
        return error.returncode or 1

    print("\nDevelopment check passed.")
    print(f"Skill: {root / 'build' / 'repo-reviewer'}")
    if selected:
        print(f"Evidence: {root / 'build' / 'manual-evidence'}")
        print("Next: open a selected fixture as the agent workspace and request a review.")
    else:
        print("Tip: add --fixture all to generate evidence snapshots for the manual corpus.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
