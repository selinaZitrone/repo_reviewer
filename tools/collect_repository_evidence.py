#!/usr/bin/env python3
"""Collect deterministic repository evidence for the repo-reviewer agent skill.

This script only reads files. It never executes code from the target repository,
installs dependencies, or reads tabular data values. It emits JSON facts for an
agentic AI reviewer with filesystem and shell access.
"""
from __future__ import annotations

import argparse
import json
import os
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
PLAIN_LICENSE_SUFFIXES = {"", ".md", ".txt", ".rst"}
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
CITATION_NAMES = {"citation", "citation.txt", "citation.cff", "codemeta.json"}
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
CODE_SUFFIXES = {".c", ".cpp", ".h", ".java", ".jl", ".js", ".m", ".py", ".r", ".rmd", ".sh"}
JUNK_DIR_NAMES = {
    ".idea",
    "__pycache__",
    ".ipynb_checkpoints",
    ".pytest_cache",
    ".rproj.user",
    ".venv",
    "build",
    "dist",
    "node_modules",
    "venv",
}
JUNK_FILE_NAMES = {".ds_store", "thumbs.db", ".rhistory", ".rdata", ".ruserdata"}
JUNK_SUFFIXES = {".pyc", ".pyo", ".bak", ".orig"}
SECRET_ASSIGNMENT = re.compile(
    r"(?i)(api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password)"
    r"\s*[:=]\s*[\"']?([^\s\"'#,;]{8,})"
)
PLACEHOLDERS = re.compile(
    r"(?i)^(your[-_]|example|sample|dummy|placeholder|changeme|replace|xxx|\$\{|<)"
)
README_CITATION_HEADING = re.compile(r"(?im)^#{1,6}\s+(?:how to cite|citation)\b")
ABSOLUTE_PATH = re.compile(
    r"(?i)(?:/(?:users|home|mnt|volumes)/[^\s\"'`]+|[a-z]:[\\/][^\s\"'`]+|~[\\/][^\s\"'`]+)"
)
WORKING_DIRECTORY_CALL = re.compile(r"\b(?:setwd|os\.chdir)\s*\(")


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


def root_license_files(root_files: list[Path]) -> list[Path]:
    """Return root files whose names conventionally identify a licence."""
    matches = []
    for path in root_files:
        stem = path.name.lower()
        if re.match(r"^licen[cs]e(?:$|[-_.])", stem):
            matches.append(path)
    return matches


def readme_has_substantive_content(path: Path) -> bool:
    text = read_text(path, limit=200_000)
    if text is None:
        return False
    meaningful = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("<!--")
    ]
    if len(meaningful) < 2:
        return False
    body = " ".join(line.lstrip("# ") for line in meaningful[1:]).strip()
    return len(body) >= 20


def scan_junk_candidates(root: Path) -> list[dict]:
    candidates: list[dict] = []
    for current, directory_names, file_names in os.walk(root):
        current_path = Path(current)
        directory_names[:] = [name for name in directory_names if name.lower() not in {".git", ".hg", ".svn"}]
        for name in directory_names:
            lower = name.lower()
            if lower in JUNK_DIR_NAMES or lower.endswith(".egg-info"):
                candidates.append(
                    {"path": relative(current_path / name, root), "kind": "generated or dependency directory"}
                )
        for name in file_names:
            lower = name.lower()
            suffix = Path(name).suffix.lower()
            if lower in JUNK_FILE_NAMES or suffix in JUNK_SUFFIXES or name.endswith("~"):
                candidates.append(
                    {"path": relative(current_path / name, root), "kind": "generated or backup file"}
                )
    return candidates


def scan_code_patterns(files: list[Path], root: Path) -> tuple[list[dict], list[dict]]:
    absolute_paths: list[dict] = []
    working_directory_calls: list[dict] = []
    for path in files:
        if path.suffix.lower() not in CODE_SUFFIXES:
            continue
        text = read_text(path, limit=500_000)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//", "%", "*")):
                continue
            if ABSOLUTE_PATH.search(line):
                absolute_paths.append(
                    {"path": relative(path, root), "line": line_number, "kind": "possible absolute path"}
                )
            if WORKING_DIRECTORY_CALL.search(line):
                working_directory_calls.append(
                    {"path": relative(path, root), "line": line_number, "kind": "working-directory change"}
                )
    return absolute_paths, working_directory_calls


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
    substantive_readmes = [path for path in readmes if readme_has_substantive_content(path)]
    licences = root_license_files(root_files)
    plain_licences = [path for path in licences if path.suffix.lower() in PLAIN_LICENSE_SUFFIXES]
    citations = [path for path in root_files if path.name.lower() in CITATION_NAMES]
    for readme in readmes:
        text = read_text(readme, limit=200_000) or ""
        if README_CITATION_HEADING.search(text):
            citations.append(readme)
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
    junk = scan_junk_candidates(root)
    absolute_paths, working_directory_calls = scan_code_patterns(files, root)

    facts = [
        fact(
            "readme-informative",
            "readme-present",
            "pass" if readmes else "fail",
            path_evidence(readmes, root) if readmes else [{"missing": "README at repository root"}],
            "Root README found." if readmes else "No root README with a standard name was found.",
        ),
        fact(
            "readme-informative",
            "readme-has-content",
            "pass" if substantive_readmes else "fail",
            (
                path_evidence(substantive_readmes, root)
                if substantive_readmes
                else [{"missing": "substantive content in a root README"}]
            ),
            (
                "Root README contains substantive content."
                if substantive_readmes
                else "No substantive root README content was found."
            ),
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
            "license-present-and-suitable",
            "license-machine-readable",
            "pass" if plain_licences else ("candidate-fail" if licences else "needs-ai"),
            (
                path_evidence(plain_licences, root)
                if plain_licences
                else (
                    [
                        {"path": relative(path, root), "kind": "licence is not in a configured plain-text format"}
                        for path in licences
                    ]
                    if licences
                    else [{"missing": "known plain-text licence artifact"}]
                )
            ),
            (
                "Plain-text licence artifact found."
                if plain_licences
                else (
                    "Only possible binary licence artifacts were found; confirm their format."
                    if licences
                    else "No known licence artifact was found; AI must check for embedded or unlisted licence text."
                )
            ),
        ),
        fact(
            "code-citation-present",
            "code-citation-present",
            "pass" if citations else "needs-ai",
            path_evidence(sorted(set(citations)), root) if citations else [{"missing": "known software-citation artifact"}],
            (
                "Software-citation artifact or README section found."
                if citations
                else "No known citation artifact was found; AI must check for an unlisted equivalent."
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
            "no-secrets-present",
            "no-secrets-present",
            "candidate-fail" if secrets else "pass",
            secrets if secrets else [{"scan": f"{len(files)} files; secret values were never emitted"}],
            (
                "Potential secret indicators require confirmation; values are redacted."
                if secrets
                else "No configured filename or assignment patterns were found."
            ),
        ),
        fact(
            "no-junk-files",
            "no-junk-files",
            "candidate-fail" if junk else "pass",
            junk if junk else [{"scan": f"{len(files)} files; no configured junk patterns found"}],
            (
                "Possible generated or throwaway files require confirmation."
                if junk
                else "No configured generated, operating-system, or backup-file patterns were found."
            ),
        ),
        fact(
            "portable-code",
            "no-absolute-paths",
            "candidate-fail" if absolute_paths else "pass",
            absolute_paths if absolute_paths else [{"scan": "code files; no configured absolute-path patterns found"}],
            (
                "Possible absolute paths require confirmation; path contents are not emitted."
                if absolute_paths
                else "No configured absolute-path patterns were found in code files."
            ),
        ),
        fact(
            "portable-code",
            "no-setwd-or-chdir",
            "candidate-fail" if working_directory_calls else "pass",
            (
                working_directory_calls
                if working_directory_calls
                else [{"scan": "code files; no setwd(...) or os.chdir(...) calls found"}]
            ),
            (
                "Working-directory changes require confirmation."
                if working_directory_calls
                else "No configured working-directory change calls were found."
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
