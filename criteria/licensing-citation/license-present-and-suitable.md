---
id: license-present-and-suitable
title: The repository has a clear, suitable licence
group: licensing-citation
sources:
  - fair4rs
  - fair-software-eu
  - nature-code-guidelines
checks:
  - id: license-present
    mode: deterministic
    severity: must-fix
    summary: A licence file (or full licence text) exists
    evidence:
      any:
        - LICENSE
        - LICENCE
        - LICENSE.md
        - LICENCE.md
        - LICENSE.txt
        - LICENCE.txt
        - "LICENSE-<name> or LICENCE-<name> for a named or dual licence"
        - "full licence text present in README"
  - id: license-machine-readable
    mode: deterministic
    severity: must-fix
    summary: The licence is available as plain text rather than only in a binary document
    evidence:
      any:
        - "LICENSE or LICENCE with no extension or a .md, .txt, or .rst extension"
        - "full licence text present in README"
  - id: code-license-osi
    mode: ai
    severity: should-fix
    summary: The code licence is OSI-approved and is not a data licence misapplied to code
    evidence:
      any:
        - "MIT, GPL, LGPL, Apache-2.0, or another licence on the OSI list"
  - id: data-license
    mode: ai
    severity: should-fix
    summary: Included data carries its own licence (only when data is present)
    evidence:
      any:
        - "a licence file inside the data folder"
        - "a data licence (e.g. CC-BY-4.0, CC0) named with its text"
        - "a README statement that clearly scopes a licence to the data"
---

## Why it matters

Without an explicit licence, code is "all rights reserved" by default: nobody may
legally reuse, modify, or redistribute it — the opposite of what publishing an
analysis is for. A licence is what turns "here is my code" into "here is my code,
and here is what you may do with it." It is a small file that unlocks the entire
point of sharing.

Data and code are different works and often need *different* licences. A single
`LICENSE` file covering an MIT-licensed script says nothing about whether the
CSV next to it may be redistributed.

> This is one criterion with several checks, not several criteria: "a licence is
> present", "it is a recognised licence", and "included data is licensed too" are
> checks of the same criterion — one report section, up to three `✓`/`✗`/`?` lines.

## How to satisfy it

- Add a licence file at the repository root. For research **code**, prefer an
  [OSI-approved](https://opensource.org/licenses) licence (MIT and Apache-2.0 are
  common, permissive choices; GPL if you want copyleft).
- For **data**, add a separate data licence — Creative Commons (e.g. CC-BY-4.0)
  is usual for data. State it distinctly from the code licence.
- Make sure the full licence *text* is present, not just a name in the README.
  Use a plain-text or Markdown file, not only a PDF or office document. GitHub's
  "Add a license" helper generates the correct file.
- If the repository combines code, data, and text, say in the README which
  licence covers which part.

## Examples

Sufficient:

    LICENSE          # full text of MIT / Apache-2.0 / GPL-3.0 ...
    data/LICENSE     # CC-BY-4.0 for the contents of data/

Not sufficient:

    README.md        # "MIT licensed" with no LICENSE file and no text
    (no licence file at all, data included)   # -> data is un-reusable by default
