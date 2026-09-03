---
id: portable-code
title: The code is portable across machines and operating systems
group: reproducibility
sources:
  - wilson-2017
  - marwick-2018
checks:
  - id: no-absolute-paths
    mode: deterministic
    pass_when: absent
    severity: must-fix
    summary: The code contains no hard-coded absolute paths that tie it to one machine
    evidence:
      any:
        - "file-access paths beginning /Users/, /home/, /mnt/, or /Volumes/"
        - "Windows drive paths such as C:\\ or D:/"
        - "home-relative paths beginning ~/"
  - id: no-setwd-or-chdir
    mode: deterministic
    pass_when: absent
    severity: should-fix
    summary: The code does not pin the process to a machine-specific working directory
    evidence:
      r:
        - "setwd(...)"
      python:
        - "os.chdir(...)"
  - id: os-independent-code
    mode: ai
    pass_when: absent
    severity: should-fix
    summary: The code avoids operating-system-specific assumptions that prevent execution elsewhere
    evidence:
      any:
        - "path construction with hard-coded separators or string concatenation"
        - "OS checks without corresponding implementations for supported systems"
        - "reliance on Desktop, Documents, or another machine-specific location"
---

## Why it matters

Machine-specific paths and operating-system assumptions commonly make otherwise sound
code fail on a fresh computer.

## How to satisfy it

- Use paths relative to the project root.
- In R, use `here::here()` or `file.path()` and avoid `setwd()`.
- In Python, use `pathlib.Path` or `os.path.join()` and avoid `os.chdir()`.
- Document genuine operating-system requirements or provide equivalent branches for
  every operating system the project claims to support.

## Examples

Do not use `read_csv("/Users/name/project/data/raw.csv")`. Prefer a project-relative
path such as `here::here("data", "raw.csv")` or `Path(__file__).parent / "data" /
"raw.csv"`. URLs and illustrative placeholders are not absolute-path violations.
