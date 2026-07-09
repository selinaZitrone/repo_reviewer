---
id: environment-captured
title: The computational environment is recorded
group: environment
sources:
  - fair4rs
  - turing-way-compendia
  - marwick-2018
  - nature-code-guidelines
checks:
  - id: env-file-present
    mode: deterministic
    severity: must-fix
    summary: A dependency/environment record exists
    evidence:
      r:
        - renv.lock
        - "DESCRIPTION with Imports/Depends"
        - "committed sessionInfo() / sessioninfo::session_info() output"
      python:
        - requirements.txt
        - "pyproject.toml with dependencies"
        - environment.yml
        - "poetry.lock / pdm.lock / uv.lock"
        - "setup.py with install_requires"
      matlab:
        - "list of required toolboxes + MATLAB version (README or ver output)"
      any:
        - Dockerfile
        - "apptainer.def / Singularity"
  - id: env-versions-pinned
    mode: ai
    severity: should-fix
    summary: Dependencies are pinned to exact versions, not just named
    evidence:
      r:
        - renv.lock
        - "DESCRIPTION with versioned Imports/Depends"
      python:
        - "requirements.txt using == (not >= or unpinned)"
        - "poetry.lock / pdm.lock / uv.lock"
        - "pyproject.toml with pinned versions"
  - id: env-language-version
    mode: ai
    severity: should-fix
    summary: The language version itself is recorded
    evidence:
      r:
        - "R version recorded in renv.lock"
      python:
        - ".python-version"
        - "requires-python in pyproject.toml"
        - "Python version stated in README"
---

## Why it matters

Code that ran on your laptop in 2025 will not run on someone else's laptop in
2029 unless the versions of the language and the packages it depended on are
written down. This is the single most common reason a published analysis cannot
be re-executed, and unlike a missing dataset or a missing licence it is
invisible: the repository looks complete right up until someone tries to use it.

Recording the environment is not the same as guaranteeing the analysis will run.
It is the minimum that makes a later attempt possible.

## How to satisfy it

Record the *exact versions* of every package the analysis loads, not just their
names. An unpinned `requirements.txt` (`pandas`, `numpy`) records intent; a
pinned one (`pandas==2.1.4`) records what actually ran.

- **R** — `renv::init()` then `renv::snapshot()`, and commit `renv.lock`.
  A `DESCRIPTION` with versioned `Imports` is an acceptable lighter alternative.
- **Python** — `pip freeze > requirements.txt`, or commit your `environment.yml`,
  your `pyproject.toml` dependencies, or a lockfile (`poetry.lock`, `uv.lock`, …).
- **MATLAB** — list the required toolboxes and the MATLAB version in the README.
- **Either** — a `Dockerfile` supersedes the above and is stronger, but is not
  required.

Also record the *language version itself* (`renv.lock` does this; for Python note
it in the README or a `.python-version` file).

## Examples

Sufficient:

    renv.lock                    # R version + all package versions
    requirements.txt             # pandas==2.1.4, numpy==1.26.2, ...

Not sufficient:

    requirements.txt             # pandas, numpy          <- no versions
    README.md                    # "install the usual tidyverse packages"
