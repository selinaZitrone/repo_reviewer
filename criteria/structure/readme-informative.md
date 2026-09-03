---
id: readme-informative
title: The README orients a newcomer
group: structure
sources:
  - nature-code-guidelines
  - ropensci-devguide
  - fair-software-eu
checks:
  - id: readme-present
    mode: deterministic
    severity: must-fix
    summary: A README exists at the repository root
    evidence:
      any:
        - README.md
        - README.rst
        - README.txt
        - README
  - id: readme-has-content
    mode: deterministic
    severity: must-fix
    summary: The README contains substantive content rather than a placeholder
    evidence:
      any:
        - "README contains more than a title line"
        - "README is not an unedited hosting-platform stub"
  - id: readme-states-what-and-why
    mode: ai
    severity: must-fix
    summary: The README says what the project is and why it exists
    evidence:
      any:
        - "a title and a 1–3 sentence description of the project / research question"
        - "what the analysis addresses or produces"
  - id: readme-states-how-to-run
    mode: ai
    severity: must-fix
    summary: The README explains how to run or reproduce the analysis
    evidence:
      any:
        - "the entry point / run order (e.g. run R/make.R, or numbered scripts in order)"
        - "where inputs come from and where outputs go"
  - id: readme-structure-overview
    mode: ai
    severity: must-fix
    summary: The README explains how the repository is organised
    evidence:
      any:
        - "a directory tree or prose description of the top-level folders"
        - "an established layout whose parts are explained"
  - id: readme-matches-repo
    mode: ai
    severity: should-fix
    summary: The README's description of files and folders matches the actual repository
    evidence:
      any:
        - "folders and scripts named in the README actually exist in the repo"
        - "no references to renamed, moved, or deleted files"
  - id: readme-nice-to-haves
    mode: ai
    severity: polish
    summary: The README includes useful orientation aids for the kind of project being reviewed
    evidence:
      any:
        - "a table of contents for a long README"
        - "an example command and expected outputs"
        - "versioned releases or relevant status badges"
---

## Why it matters

The README is the front door. A stranger decides in the first minute whether they can
understand and reuse your work, and the README is where they decide it. It has to say
three things — what this is, why it exists, and how to run it — and it has to be *true*.
A README that describes folders or scripts that no longer exist is worse than a short
one: it sends the reader looking for files that aren't there and quietly signals that
the rest of the documentation may be stale too.

## How to satisfy it

- Open with a **title and 1–3 sentences**: what the project is and the question it
  answers. Replace any hosting-platform placeholder text.
- Tell a newcomer **how to reproduce it**: the entry point (e.g. "run `R/make.R`"), the
  order things run in, where the input data come from, and where outputs are written.
- **Keep it in sync.** When you rename or move files, update the README. Describe the
  structure at a level that does not rot — folders and their roles — rather than a
  line-by-line file list that goes stale the moment you refactor.
- For a long README or complex project, add an example command, expected output, or
  table of contents when it helps a newcomer find the important path quickly.

## Examples

Sufficient:

    # Project title
    One-paragraph description + research question.
    ## Reproduce
    Run `R/make.R`; inputs in `data-raw/`, outputs in `data/`.

Not sufficient:

    README describes `R/02_cookie_cutting/` and `Figure1.R`   # neither exists anymore
    README with a title but no "how to run" and no entry point
