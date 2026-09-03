---
id: installation-instructions-verified
title: Installation and rerun instructions have been tested independently
group: archive-release
sources:
  - nature-code-guidelines
checks:
  - id: installation-instructions-verified
    mode: none
    severity: polish
    summary: Ask a colleague to test the setup and rerun instructions from a fresh copy
---

## Why it matters

Instructions can look complete to their author while still depending on unstated local
knowledge. A fresh test exposes missing steps and machine-specific assumptions.

## How to satisfy it

Ask a colleague unfamiliar with the project to follow the instructions from a fresh
clone or download. Record anything they had to ask and update the documentation. A CI
environment build is useful supporting evidence, but it does not replace the human
usability test.
