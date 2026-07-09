HOW TO WRITE A CRITERION
========================

Everything below is plain text. Copy it into Google Docs and format it there.
Write one document per criterion. Someone will convert your document into the
repository's file format afterwards — you never need to touch YAML.


THE ONE RULE
------------

One criterion = one checklist item, made up of 1 to N checks.

A criterion is a container. Each check under it is an independently reportable
pass/fail with its own mode and severity. "A LICENSE file is present" and "the
licence is suitable for reuse" are two checks of ONE criterion, not two criteria.

How to decide whether something is a new criterion or a new check:

  - Different artefact, or belongs under a different heading in the report
      -> a new CRITERION
  - Same artefact, different question about it (present? suitable? pinned?)
      -> a new CHECK inside the existing criterion

Grouping checks into a criterion has a consequence you should choose deliberately.
Checks in the same criterion can suppress each other: if a criterion's presence check
fails, its judgement checks about the quality of that same thing are reported as "not
applicable" rather than as failures. You cannot assess whether a licence is
OSI-approved when there is no licence. This is what stops one missing file from
producing four angry red crosses — the gap is reported once, as the presence failure.

So put a check in a criterion when it only makes sense given that criterion's
artefact exists. If a check should fail on its own merits regardless of what the
other checks find, it belongs in a criterion of its own.

Note that the report itself does not show criterion boundaries — it shows a group
heading followed by a flat list of check summaries. The grouping is still doing this
work; the reader just sees its effect rather than the structure.


THE FIELDS
----------

CRITERION-LEVEL FIELDS (one of each, at the top)

  Title
      A human sentence describing the good state, e.g. "The computational
      environment is recorded". Not a filename, not a command. It appears on the
      website; it does NOT appear in the report. Don't rely on it to carry meaning
      that a check summary needs to carry.

  Id
      Short, kebab-case, unique across all criteria, and permanent — it shows up
      in URLs, so treat it as an API. e.g. environment-captured

  Group
      Exactly one of the seven groups: orientation, licensing-citation, data,
      code-analysis, environment, repository-hygiene, archiving-release.
      Tie-breaker: place it by what the reader is DOING when they notice it.
      Looking at the file tree -> orientation. Reading the code -> code-analysis.
      Looking at data files -> data.

  Sources
      At least one source id from the sources table (fair4rs, wilson-2017,
      turing-way-compendia, ...). We adopt criteria from established community
      standards rather than inventing them. If you genuinely have no upstream
      source, say so explicitly and justify it in "Why it matters".


CHECK-LEVEL FIELDS (repeat this block for each check)

  Id
      Kebab-case, unique within this criterion, permanent. It is how we refer to
      the check in discussion, and the finding id in any machine-readable output.
      It is not printed in the report. e.g. env-file-present

  Mode
      How the check gets verified. Pick one:

        deterministic — a script can decide it by looking for files, globs, or
                        regexes. The script's answer is final.
        ai            — it needs judgement about the CONTENT of a file.
        none          — it cannot be decided from the repository at all
                        (e.g. "is it deposited on Zenodo?"). These render on the
                        website and in the closing checklist, never as a finding.

  Severity
      Pick one, using these anchors:

        must-fix    — without this, a competent stranger cannot reuse the repo.
        should-fix  — reuse is possible, but materially harder than necessary.
        polish      — everything else.

  Summary
      The one-line label shown next to a green tick or a red cross in the report.
      Phrase it as the GOOD state ("A licence file exists") so the tick reads
      naturally. This is the most important field you write: the reviewer judges
      the repository against the summary, not against the evidence list. So write
      the real invariant — the thing that must be true — never a filename.

  Passes when
      Either "present" (the default — leave it out if so) or "absent".

        present — the check passes when a satisfying piece of evidence is FOUND.
                  This is the majority: add-a-thing checks.
        absent  — the check passes when the evidence is NOT found. These are
                  remove-a-thing checks: committed secrets, absolute paths,
                  committed junk. Here the evidence list is the set of violation
                  patterns to search for, and the good state is the summary.

      Rule of thumb: if a passing check would make you say "good, I didn't find
      any of those", it is "absent".

  Evidence
      Concrete artefacts or patterns the script or the reviewer looks for, grouped
      by language (R, Python, MATLAB, Any). Four things to know:

        1. Required for deterministic checks. Optional for ai checks — a judgement
           like "is the licence OSI-approved?" reads content and cites its evidence
           at review time. Omit entirely for mode: none.

        2. It is illustrative, not exhaustive. The summary is the definition. A
           repository that satisfies the summary with something you never listed
           still passes — the reviewer names whatever it found. Not finding a
           listed artefact escalates to judgement; it never auto-fails.

        3. Order it best-first. The list does double duty: it decides pass/fail,
           AND the first entry that fits becomes the fix we recommend in the
           report. Put the artefact you'd actually recommend at the top.

        4. Keep entries terse. This is machine-facing text, not prose.

      There is no separate "fix" field. The fix is derived from the ordered
      evidence. Longer how-to prose belongs in "How to satisfy it" below.


THE BODY (three sections, in this order)

  Why it matters
      The rationale a scientist reads on the website. Hand-written prose, no
      jargon. This is a credibility artefact — write it well.

  How to satisfy it
      Concrete, tool-specific instructions. Where it makes a difference, give the
      R way and the Python way explicitly.

  Examples  (optional)
      "Sufficient" vs "not sufficient", when it clarifies. Skip it when it would
      be filler.


================================================================================
WORKED EXAMPLE
================================================================================

Title:     The computational environment is recorded
Id:        environment-captured
Group:     environment
Sources:   fair4rs, turing-way-compendia, marwick-2018, nature-code-guidelines


CHECK 1
  Id:          env-file-present
  Mode:        deterministic
  Severity:    must-fix
  Summary:     A dependency/environment record exists
  Passes when: present
  Evidence:
      R:       renv.lock
               DESCRIPTION with Imports/Depends
               committed sessionInfo() / sessioninfo::session_info() output
      Python:  requirements.txt
               pyproject.toml with dependencies
               environment.yml
               poetry.lock / pdm.lock / uv.lock
               setup.py with install_requires
      MATLAB:  list of required toolboxes + MATLAB version (README or ver output)
      Any:     Dockerfile
               apptainer.def / Singularity

CHECK 2
  Id:          env-versions-pinned
  Mode:        ai
  Severity:    should-fix
  Summary:     Dependencies are pinned to exact versions, not just named
  Passes when: present
  Evidence:
      R:       renv.lock
               DESCRIPTION with versioned Imports/Depends
      Python:  requirements.txt using == (not >= or unpinned)
               poetry.lock / pdm.lock / uv.lock
               pyproject.toml with pinned versions

CHECK 3
  Id:          env-language-version
  Mode:        ai
  Severity:    should-fix
  Summary:     The language version itself is recorded
  Passes when: present
  Evidence:
      R:       R version recorded in renv.lock
      Python:  .python-version
               requires-python in pyproject.toml
               Python version stated in README


WHY IT MATTERS

Code that ran on your laptop in 2025 will not run on someone else's laptop in
2029 unless the versions of the language and the packages it depended on are
written down. This is the single most common reason a published analysis cannot
be re-executed, and unlike a missing dataset or a missing licence it is
invisible: the repository looks complete right up until someone tries to use it.

Recording the environment is not the same as guaranteeing the analysis will run.
It is the minimum that makes a later attempt possible.


HOW TO SATISFY IT

Record the exact versions of every package the analysis loads, not just their
names. An unpinned requirements.txt (pandas, numpy) records intent; a pinned one
(pandas==2.1.4) records what actually ran.

  - R — renv::init() then renv::snapshot(), and commit renv.lock. A DESCRIPTION
    with versioned Imports is an acceptable lighter alternative.
  - Python — pip freeze > requirements.txt, or commit your environment.yml, your
    pyproject.toml dependencies, or a lockfile (poetry.lock, uv.lock, ...).
  - MATLAB — list the required toolboxes and the MATLAB version in the README.
  - Either — a Dockerfile supersedes the above and is stronger, but is not
    required.

Also record the language version itself (renv.lock does this; for Python note it
in the README or a .python-version file).


EXAMPLES

Sufficient:

    renv.lock                    # R version + all package versions
    requirements.txt             # pandas==2.1.4, numpy==1.26.2, ...

Not sufficient:

    requirements.txt             # pandas, numpy          <- no versions
    README.md                    # "install the usual tidyverse packages"


================================================================================
TWO VARIANTS THE EXAMPLE ABOVE DOESN'T SHOW
================================================================================

A "passes when: absent" check — the evidence lists what must NOT be there:

  Id:          no-committed-secrets
  Mode:        deterministic
  Severity:    must-fix
  Summary:     No credentials, API keys, or tokens are committed
  Passes when: absent
  Evidence:
      Any:     .env / .Renviron committed to the repository
               files matching id_rsa, *.pem, *.key
               strings matching AKIA[0-9A-Z]{16} (AWS access key)

A "mode: none" check — no evidence at all, because the tool cannot see it:

  Id:          deposited-with-doi
  Mode:        none
  Severity:    should-fix
  Summary:     The repository is deposited in an archive and has a DOI


================================================================================
BLANK TEMPLATE — COPY FROM HERE
================================================================================

Title:
Id:
Group:
Sources:


CHECK 1
  Id:
  Mode:         deterministic | ai | none
  Severity:     must-fix | should-fix | polish
  Summary:
  Passes when:  present | absent
  Evidence:
      R:
      Python:
      Any:

CHECK 2   (delete if unused; add more as needed)
  Id:
  Mode:
  Severity:
  Summary:
  Passes when:
  Evidence:
      R:
      Python:
      Any:


WHY IT MATTERS

  (Prose for the website. Why does a scientist lose something real without this?)


HOW TO SATISFY IT

  (Concrete instructions. The R way and the Python way, where they differ.)


EXAMPLES   (optional — delete if it would be filler)

  Sufficient:

  Not sufficient:
