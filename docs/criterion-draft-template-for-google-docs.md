# Criterion drafting template for Google Docs

This is a collaboration worksheet for drafting and discussing criteria. It is
not loaded by the reviewer. After the team agrees on a draft, transfer it to a
Markdown file under `criteria/` that follows `criteria/_schema.md`.

Title: (a sentence describing the good state of the criterion)
Id: (kebab-case, permanent)
Group: structure | licensing-citation | data | code-quality | environment | repository-hygiene | archive-release | reproducibility (choose one)

CHECK 1 (copy as many times as you have checks for a criterion)
  Id: (kebab-case, unique within this criterion)
  Mode:  deterministic | ai | none
  Severity: must-fix | should-fix | polish
  Summary: (the report line; phrase it as the good state of this check)
  Passes when:  present | absent 
  Evidence: (best-first — the top entry becomes the recommended fix)
  R:
Evidence 1
Evidence 2
…
  Python:
Evidence 1
Evidence 2
…
   Any:
Evidence 1
Evidence 2 
…

Prose text

Here you can put things like:
Why it matters
How to satisfy it
Examples
Concrete instructions
Questions
References
…
This can be text that will go on the website, but also just additional info, links etc. Does not need to be polished yet.


