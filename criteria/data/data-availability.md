---
id: data-availability
title: Data availability is documented and access is facilitated where possible
group: data
sources:
  - turing-way-compendia
  - wilson-2017
  - nature-code-guidelines
checks:
  - id: data-access-instructions
    mode: ai
    severity: should-fix
    summary: The repository states whether and how the data can be obtained
    evidence:
      any:
        - "a data-availability statement identifying data as public, restricted, unavailable, or available on request"
        - "a URL or DOI for public data"
        - "an application process for restricted data"
        - "contact information for data available on request"
  - id: data-open-format
    mode: ai
    severity: should-fix
    summary: Included data uses open formats where a suitable open format exists
    evidence:
      any:
        - "open formats such as CSV, TSV, TXT, JSON, Parquet, or an appropriate domain standard"
        - "no unexplained reliance on proprietary formats such as XLSX, SAV, or DTA"
---

## Why it matters

The absence of data from a repository is not automatically a problem: ethical, legal,
or contractual restrictions may prevent sharing. The important requirement is that a
reader can tell what data were used and whether and how access is possible.

Open formats reduce dependence on particular software and make data easier to inspect
and reuse.

## How to satisfy it

- Add a data-availability statement to the README.
- Link public data with a stable URL or DOI; explain the application process for
  restricted data; give a contact route for data available on request.
- Prefer open or community-standard formats and explain any necessary proprietary
  format.
