#!/usr/bin/env python3
"""Link the generated repo-reviewer skill into a user-level agent skill folder.

The helper never deletes or replaces an existing destination. On Windows it uses
a directory junction; on other platforms it uses a directory symlink.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def destination_for(tool: str, home: Path) -> Path:
    if tool in {"codex", "copilot"}:
        return home / ".agents" / "skills" / "repo-reviewer"
    if tool == "claude":
        return home / ".claude" / "skills" / "repo-reviewer"
    raise ValueError(f"Unsupported tool: {tool}")


def same_location(left: Path, right: Path) -> bool:
    try:
        return left.resolve(strict=True) == right.resolve(strict=True)
    except OSError:
        return False


def create_link(source: Path, destination: Path, dry_run: bool = False) -> str:
    source = source.resolve(strict=True)

    if os.path.lexists(destination):
        if same_location(source, destination):
            return f"Already linked: {destination} -> {source}"
        raise FileExistsError(
            f"Refusing to replace existing path: {destination}\n"
            "Move or rename it yourself, then run this command again."
        )

    if dry_run:
        return f"Would link: {destination} -> {source}"

    destination.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        completed = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(destination), str(source)],
            capture_output=True,
            text=True,
        )
        if completed.returncode:
            message = completed.stderr.strip() or completed.stdout.strip()
            raise OSError(f"Could not create Windows directory junction: {message}")
    else:
        destination.symlink_to(source, target_is_directory=True)

    return f"Linked: {destination} -> {source}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "tools",
        nargs="+",
        choices=("codex", "claude", "copilot"),
        help="Agent tools that should see the development skill.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the links without changing user-level directories.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    source = root / "build" / "repo-reviewer"
    if not (source / "SKILL.md").is_file():
        print("Generated skill not found. Run: python tools/dev_check.py", file=sys.stderr)
        return 1

    destinations: dict[Path, list[str]] = {}
    for tool in args.tools:
        destinations.setdefault(destination_for(tool, Path.home()), []).append(tool)

    try:
        for destination, tools in destinations.items():
            print(f"{', '.join(tools)}: {create_link(source, destination, args.dry_run)}")
    except (FileExistsError, OSError) as error:
        print(f"setup_dev_skill: {error}", file=sys.stderr)
        return 1

    if not args.dry_run:
        print("Rebuilds now flow through the link. Restart an agent if it does not detect the skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
