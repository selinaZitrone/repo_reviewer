#!/usr/bin/env python3
"""Collect deterministic repository evidence for the repo-reviewer agent skill.

This script only reads files. It never executes code from the target repository,
installs dependencies, or reads tabular data values. It emits JSON facts for an
agentic AI reviewer with filesystem and shell access.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


SCHEMA_VERSION = "0.1.0"
SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".idea",
    ".vscode",
}
SKIP_FILE_NAMES = {"review.md"}
README_NAMES = {"readme", "readme.md", "readme.rst", "readme.txt"}
LICENSE_NAMES = {"license", "license.md", "license.txt", "licence", "licence.md", "licence.txt"}
ENVIRONMENT_NAMES = {
    "renv.lock",
    "requirements.txt",
    "pyproject.toml",
    "environment.yml",
    "environment.yaml",
    "poetry.lock",
    "pdm.lock",
    "uv.lock",
    "setup.py",
    "dockerfile",
    "apptainer.def",
    "singularity",
}
SUSPECT_SECRET_NAMES = {
    ".env",
    ".renviron",
    ".httr-oauth",
    "credentials",
    "credentials.json",
}
SECRET_SUFFIXES = {".pem", ".ppk", ".key"}
TEXT_SUFFIXES = {
    "",
    ".c",
    ".cpp",
    ".env",
    ".h",
    ".ini",
    ".ipynb",
    ".java",
    ".jl",
    ".js",
    ".json",
    ".m",
    ".md",
    ".py",
    ".r",
    ".rmd",
    ".rst",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
SECRET_ASSIGNMENT = re.compile(
    r"(?i)(api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password)"
    r"\s*[:=]\s*[\"']?([^\s\"'#,;]{8,})"
)
PLACEHOLDERS = re.compile(
    r"(?i)^(your[-_]|example|sample|dummy|placeholder|changeme|replace|xxx|\$\{|<)"
)


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def inventory(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        try:
            rel_parts = path.relative_to(root).parts
        except ValueError:
            continue
        if any(part.lower() in SKIP_DIRS for part in rel_parts[:-1]):
            continue
        if path.is_file() and not path.is_symlink() and path.name.lower() not in SKIP_FILE_NAMES:
            files.append(path)
    return sorted(files, key=lambda p: relative(p, root).lower())


def fact(criterion_id: str, check_id: str, state: str, evidence: list[dict], note: str) -> dict:
    return {
        "criterion_id": criterion_id,
        "check_id": check_id,
        "state": state,
        "evidence": evidence,
        "note": note,
    }


def path_evidence(paths: list[Path], root: Path) -> list[dict]:
    return [{"path": relative(path, root)} for path in paths]


def read_text(path: Path, limit: int = 1_000_000) -> str | None:
    try:
        if path.stat().st_size > limit:
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def scan_secret_candidates(files: list[Path], root: Path) -> list[dict]:
    candidates: list[dict] = []
    for path in files:
        name = path.name.lower()
        rel = relative(path, root)
        if (
            name in SUSPECT_SECRET_NAMES
            or name.startswith("id_rsa")
            or path.suffix.lower() in SECRET_SUFFIXES
            or ("service" in name and "account" in name and path.suffix.lower() == ".json")
        ):
            candidates.append({"path": rel, "kind": "suspicious filename"})

        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = read_text(path, limit=500_000)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            match = SECRET_ASSIGNMENT.search(line)
            if match and not PLACEHOLDERS.match(match.group(2)):
                candidates.append(
                    {
                        "path": rel,
                        "line": line_number,
                        "kind": f"possible {match.group(1).lower()} assignment (value redacted)",
                    }
                )
    return candidates


def collect_facts(root: Path) -> dict:
    files = inventory(root)
    root_files = [path for path in files if path.parent == root]

    readmes = [path for path in root_files if path.name.lower() in README_NAMES]
    licences = [path for path in root_files if path.name.lower() in LICENSE_NAMES]
    environments = [
        path
        for path in files
        if path.name.lower() in ENVIRONMENT_NAMES
        or (path.name.lower().startswith("requirements") and path.suffix.lower() == ".txt")
    ]

    for path in files:
        if path.name.lower() == "description":
            text = read_text(path, limit=200_000) or ""
            if re.search(r"(?mi)^(imports|depends)\s*:", text):
                environments.append(path)

    secrets = scan_secret_candidates(files, root)

    facts = [
        fact(
            "readme-informative",
            "readme-present",
            "pass" if readmes else "fail",
            path_evidence(readmes, root) if readmes else [{"missing": "README at repository root"}],
            "Root README found." if readmes else "No root README with a standard name was found.",
        ),
        fact(
            "license-present-and-suitable",
            "license-present",
            "pass" if licences else "needs-ai",
            path_evidence(licences, root) if licences else [{"missing": "standard root licence file"}],
            (
                "Root licence file found."
                if licences
                else "No standard root licence file was found; AI must check whether the full text is embedded elsewhere."
            ),
        ),
        fact(
            "environment-captured",
            "env-file-present",
            "pass" if environments else "needs-ai",
            path_evidence(sorted(set(environments)), root)
            if environments
            else [{"missing": "known dependency/environment artifact"}],
            (
                "Known dependency/environment artifact found."
                if environments
                else "No known artifact was found; AI must check for an unlisted equivalent."
            ),
        ),
        fact(
            "no-committed-secrets",
            "no-committed-secrets",
            "candidate-fail" if secrets else "pass",
            secrets if secrets else [{"scan": f"{len(files)} files; secret values were never emitted"}],
            (
                "Potential secret indicators require confirmation; values are redacted."
                if secrets
                else "No configured filename or assignment patterns were found."
            ),
        ),
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        # Keep output independent of the user's absolute local path.
        "target": root.name,
        "date": date.today().isoformat(),
        "safety": {
            "repository_code_executed": False,
            "tabular_cell_values_read": False,
            "secret_values_emitted": False,
        },
        "inventory": {
            "file_count": len(files),
            "paths": [relative(path, root) for path in files],
        },
        "facts": facts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, help="Write output to this path instead of stdout.")
    args = parser.parse_args()

    root = args.target.resolve()
    if not root.is_dir():
        print(f"collect_repository_evidence: target is not a directory: {root}", file=sys.stderr)
        return 2

    result = collect_facts(root)
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
        print(f"Collected repository evidence -> {args.out}")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
