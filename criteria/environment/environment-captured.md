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
  - id: additional-toolboxes-specified
    mode: ai
    severity: must-fix
    summary: Required toolboxes and system-level dependencies outside the package manager are named
    evidence:
      r:
        - "non-CRAN packages or system libraries such as GDAL or JAGS documented in the README"
      python:
        - "non-pip dependencies such as system libraries, CUDA, or cuDNN documented in the README"
      matlab:
        - "required MATLAB toolboxes listed by name"
      any:
        - "required compilers, drivers, or external binaries are documented"
  - id: installation-instructions-exist
    mode: ai
    severity: must-fix
    summary: The README explains how to install dependencies and set up the environment
    evidence:
      any:
        - "an Installation, Setup, or Getting started section with commands"
        - "a documented install target such as make install"
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
      matlab:
        - "MATLAB version stated in README"
      any:
        - "language version stated in a configuration file or README"
  - id: container-image-provided
    mode: ai
    severity: polish
    summary: A ready-to-pull container image is provided when container distribution is appropriate
    evidence:
      any:
        - "docker pull and docker run commands for a published image"
        - "CI that builds and publishes an image"
        - "devcontainer.json that references a pre-built image"
        - "an Apptainer or Singularity definition"
  - id: compute-resources-specified
    mode: ai
    severity: should-fix
    summary: Compute resources and job submission are documented when the analysis requires HPC
    evidence:
      any:
        - "CPU, memory, GPU, and wall-time requirements in the README"
        - "a SLURM, PBS, or LSF submission script"
        - "module, queue, and submission instructions"
---

## Why it matters

Code that ran on your laptop in 2025 will not run on someone else's laptop in
2029 unless the versions of the language and the packages it depended on are
written down. This is the single most common reason a published analysis cannot
be re-executed, and unlike a missing dataset or a missing licence it is
invisible: the repository looks complete right up until someone tries to use it.

Recording the environment is not the same as guaranteeing the analysis will run.
It is the minimum that makes a later attempt possible.

Dependencies outside the language package manager are easy to miss. This includes
MATLAB toolboxes, system libraries, drivers, compilers, and cluster requirements.

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

Add copy-pasteable setup commands to the README. Name toolboxes, system libraries,
drivers, and external binaries separately. If the workflow requires HPC, document
cores, memory, accelerators, wall time, and a sample submission command. A published,
versioned container image is useful polish for complex environments but is not required
for every project.

## Examples

Sufficient:

    renv.lock                    # R version + all package versions
    requirements.txt             # pandas==2.1.4, numpy==1.26.2, ...

Not sufficient:

    requirements.txt             # pandas, numpy          <- no versions
    README.md                    # "install the usual tidyverse packages"
