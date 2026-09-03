---
id: file-naming-and-structure
title: Files and folders are named meaningfully and organised clearly
group: structure
sources:
  - marwick-2018
  - cookiecutter-ds
  - nature-s44271
checks:
  - id: repo-name-meaningful
    mode: ai
    severity: must-fix
    summary: The repository name reflects what the project is about
    evidence:
      any:
        - "a project- or paper-specific name rather than a placeholder such as new-repo, test, or project1"
  - id: meaningful-file-and-folder-names
    mode: ai
    severity: must-fix
    summary: File and folder names describe their contents
    evidence:
      any:
        - "descriptive names rather than generic names such as script1.R or Untitled.ipynb"
        - "a consistent, machine-readable naming convention"
  - id: conventional-folder-structure
    mode: ai
    severity: should-fix
    summary: Files are organised into a clear, conventional folder structure
    evidence:
      any:
        - "separate top-level areas for code, data, and results where those artifacts are present"
        - "a structure resembling an established project template"
---

## Why it matters

Descriptive names and a predictable layout let a newcomer understand the project from
the file tree before opening every file. A conventional layout is a means to that end,
not a requirement to force every repository into the same template.

## How to satisfy it

- Give the repository a project-specific name.
- Name files and folders for their role or content, and use one delimiter and casing
  convention consistently.
- Separate major artifact types when the project contains them, for example `data/`,
  `scripts/`, and `outputs/`.
- Prefer an established discipline-specific structure when one exists.

## Examples

`scripts/01-clean-data.R` and `outputs/figures/` are clearer than `code/script1.R`
and `stuff/`.
