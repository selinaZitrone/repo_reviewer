#!/usr/bin/env python3
"""Compile the criteria set into a tool-neutral Agent Skill.

Reads every criterion file (criteria/<group>/<id>.md), pulls the YAML frontmatter
(the `checks`), renders them grouped by report section, and injects the result into
tools/skill_template.md. The criteria are the single source of truth; this script is
the projection into the AI-facing skill.

Usage:
    python tools/compile_skill.py [--criteria-dir DIR] [--template FILE]
                                  [--out FILE] [--version STR]
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

import yaml

# Canonical report-section order + human-readable heading (mirrors criteria/_groups.md).
# Unknown groups append, titled by their raw id.
GROUP_ORDER = [
    "structure",
    "licensing-citation",
    "data",
    "code-quality",
    "environment",
    "repository-hygiene",
    "archive-release",
    "reproducibility",
]
GROUP_TITLES = {
    "structure": "Structure & orientation",
    "licensing-citation": "Licensing & citation",
    "data": "Data",
    "code-quality": "Code quality",
    "environment": "Environment & dependencies",
    "repository-hygiene": "Repository hygiene",
    "archive-release": "Archive & release",
    "reproducibility": "Reproducibility-supporting practices",
}
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CHECK_MODES = {"deterministic", "ai", "none"}
SEVERITIES = {"must-fix", "should-fix", "polish"}


def parse_frontmatter(text: str, path: Path) -> dict:
    """Return the YAML frontmatter of a markdown file as a dict."""
    if not text.startswith("---"):
        raise ValueError(f"{path}: no YAML frontmatter (must start with '---').")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError(f"{path}: frontmatter not closed with '---'.")
    return yaml.safe_load(text[3:end]) or {}


def load_criteria(criteria_dir: Path) -> list[dict]:
    """Load every criterion file. Skips files whose name starts with '_'."""
    criteria = []
    criterion_ids: set[str] = set()
    source_registry = criteria_dir / "_sources.md"
    known_sources = (
        set(
            re.findall(
                r"^\| `([^`]+)` \|",
                source_registry.read_text(encoding="utf-8"),
                flags=re.MULTILINE,
            )
        )
        if source_registry.is_file()
        else set()
    )
    for md in sorted(criteria_dir.glob("*/*.md")):
        if md.name.startswith("_"):
            continue
        text = md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text, md)
        for field in ("id", "title", "group", "checks"):
            if field not in fm:
                raise ValueError(f"{md}: frontmatter missing required field '{field}'.")
        if not ID_PATTERN.fullmatch(str(fm["id"])):
            raise ValueError(f"{md}: criterion id must be kebab-case.")
        if fm["id"] in criterion_ids:
            raise ValueError(f"{md}: duplicate criterion id '{fm['id']}'.")
        criterion_ids.add(fm["id"])
        if md.stem != fm["id"]:
            raise ValueError(f"{md}: filename must match criterion id '{fm['id']}'.")
        if fm["group"] not in GROUP_ORDER:
            raise ValueError(f"{md}: unknown group '{fm['group']}'.")
        if md.parent.name != fm["group"]:
            raise ValueError(f"{md}: parent folder must match group '{fm['group']}'.")
        if not isinstance(fm.get("sources"), list) or not fm["sources"]:
            raise ValueError(f"{md}: 'sources' must be a non-empty list.")
        unknown_sources = set(fm["sources"]) - known_sources if known_sources else set()
        if unknown_sources:
            names = ", ".join(sorted(str(item) for item in unknown_sources))
            raise ValueError(f"{md}: unknown source id(s): {names}.")
        if not isinstance(fm["checks"], list) or not fm["checks"]:
            raise ValueError(f"{md}: 'checks' must be a non-empty list.")

        check_ids: set[str] = set()
        for check in fm["checks"]:
            for field in ("id", "mode", "severity", "summary"):
                if field not in check:
                    raise ValueError(f"{md}: a check is missing '{field}'.")
            check_id = str(check["id"])
            if not ID_PATTERN.fullmatch(check_id):
                raise ValueError(f"{md}: check id '{check_id}' must be kebab-case.")
            if check_id in check_ids:
                raise ValueError(f"{md}: duplicate check id '{check_id}'.")
            check_ids.add(check_id)
            if check["mode"] not in CHECK_MODES:
                raise ValueError(f"{md}: check '{check_id}' has invalid mode '{check['mode']}'.")
            if check["severity"] not in SEVERITIES:
                raise ValueError(
                    f"{md}: check '{check_id}' has invalid severity '{check['severity']}'."
                )
            if check.get("pass_when", "present") not in {"present", "absent"}:
                raise ValueError(f"{md}: check '{check_id}' has invalid pass_when value.")
            if check["mode"] == "deterministic" and not check.get("evidence"):
                raise ValueError(f"{md}: deterministic check '{check_id}' needs evidence.")
            if check["mode"] == "none" and check.get("evidence"):
                raise ValueError(f"{md}: mode-none check '{check_id}' must omit evidence.")

        if "## Why it matters" not in text or "## How to satisfy it" not in text:
            raise ValueError(f"{md}: body must contain 'Why it matters' and 'How to satisfy it'.")
        fm["_path"] = md
        criteria.append(fm)
    return criteria


def render_evidence(evidence: dict | None) -> str:
    """Flatten {lang: [items]} into 'lang: a | b; lang2: c'."""
    if not evidence:
        return ""
    parts = []
    for lang, items in evidence.items():
        if isinstance(items, str):
            items = [items]
        parts.append(f"{lang}: " + " | ".join(str(i) for i in items))
    return "; ".join(parts)


def render_check(check: dict, criterion_path: Path) -> str:
    for field in ("id", "mode", "severity", "summary"):
        if field not in check:
            raise ValueError(f"{criterion_path}: a check is missing '{field}'.")
    pass_when = check.get("pass_when", "present")
    if pass_when not in ("present", "absent"):
        raise ValueError(
            f"{criterion_path}: check '{check['id']}' has pass_when '{pass_when}' "
            f"(must be 'present' or 'absent')."
        )
    tag = f"{check['mode']}, {check['severity']}"
    if pass_when == "absent":
        tag += ", pass_when=absent"
    head = f"- [{check['id']}] ({tag}) {check['summary']}"
    ev = render_evidence(check.get("evidence"))
    if ev:
        return head + f"\n    evidence — {ev}"
    # deterministic checks decide purely from named artifacts, so evidence is
    # mandatory. ai checks judge content and cite evidence at review time, so it is
    # optional. none checks are never evaluated from the repo.
    if check["mode"] == "deterministic":
        raise ValueError(
            f"{criterion_path}: deterministic check '{check['id']}' has no evidence "
            f"(a deterministic check needs artifacts/patterns to look for)."
        )
    return head


def render_criteria(criteria: list[dict]) -> str:
    by_group: dict[str, list[dict]] = {}
    for c in criteria:
        by_group.setdefault(c["group"], []).append(c)

    ordered = [g for g in GROUP_ORDER if g in by_group]
    ordered += [g for g in by_group if g not in GROUP_ORDER]

    blocks = []
    for group in ordered:
        lines = [f"### {GROUP_TITLES.get(group, group)}"]
        for c in by_group[group]:
            lines.append(f"\n**{c['title']}** (`{c['id']}`)")
            for check in c["checks"]:
                lines.append(render_check(check, c["_path"]))
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--criteria-dir", type=Path, default=root / "criteria")
    ap.add_argument("--template", type=Path, default=root / "tools" / "skill_template.md")
    ap.add_argument("--out", type=Path, default=root / "build" / "repo-reviewer" / "SKILL.md")
    ap.add_argument("--version", default="0.1.0")
    args = ap.parse_args()

    try:
        criteria = load_criteria(args.criteria_dir)
        if not criteria:
            print(f"No criteria found under {args.criteria_dir}.", file=sys.stderr)
            return 1
        template = args.template.read_text(encoding="utf-8")
    except (ValueError, OSError) as e:
        print(f"compile_skill: {e}", file=sys.stderr)
        return 1

    version_str = f"{args.version} (compiled {date.today().isoformat()})"
    skill = template.replace("{{CRITERIA}}", render_criteria(criteria))
    skill = skill.replace("{{CRITERIA_VERSION}}", version_str)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(skill, encoding="utf-8")

    # Keep the distributed skill self-contained. Agentic hosts run this bundled,
    # standard-library-only collector before making AI judgments.
    bundled_script = args.out.parent / "scripts" / "collect_repository_evidence.py"
    bundled_script.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "tools" / "collect_repository_evidence.py", bundled_script)
    n_checks = sum(len(c["checks"]) for c in criteria)
    distribution_readme = (root / "tools" / "distribution_README.md").read_text(
        encoding="utf-8"
    )
    distribution_readme = distribution_readme.replace("{{CRITERIA_COUNT}}", str(len(criteria)))
    distribution_readme = distribution_readme.replace("{{CHECK_COUNT}}", str(n_checks))
    (args.out.parent / "README.md").write_text(distribution_readme, encoding="utf-8")

    print(
        f"Compiled {len(criteria)} criteria ({n_checks} checks) -> {args.out} "
        f"(+ {bundled_script})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
