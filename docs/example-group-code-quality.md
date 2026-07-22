A WORKED GROUP: CODE QUALITY
============================

Three criteria from one group, written out in full. Read them alongside the field
notes — between them they show every variation you are likely to need.

    Criterion 1  paths-are-relative           two "absent" checks, pattern evidence
    Criterion 2  randomness-is-reproducible   a presence check + a judgement check
    Criterion 3  run-order-discoverable       a single-check criterion, no "absent"

What to notice as you read is collected at the end.


--------------------------------------------------------------------------------
CRITERION 1 OF 3
--------------------------------------------------------------------------------

Title:      The code runs from a fresh clone without editing paths
Id:         paths-are-relative
Group:      code-quality
Sources:    marwick-2018, wilson-2017, ropensci-devguide


CHECK 1
  Id:           no-absolute-paths
  Mode:         deterministic
  Severity:     must-fix
  Summary:      No absolute filesystem paths appear in the code
  Passes when:  absent
  Evidence:
      Any:      paths beginning /Users/, /home/, /mnt/, /media/
                paths beginning with a drive letter (C:/, C:\, D:\)
                a path assembled from an absolute root, e.g.
                  file.path("C:/work", ...) or os.path.join("/home/ab", ...)

CHECK 2
  Id:           no-working-directory-changes
  Mode:         deterministic
  Severity:     should-fix
  Summary:      The code does not change the working directory at run time
  Passes when:  absent
  Evidence:
      R:        setwd(
      Python:   os.chdir(
      Any:      a cd to a machine-specific location inside a run script


WHY IT MATTERS

An absolute path is a sentence about one computer. `/Users/selina/thesis/data.csv`
is true on exactly one machine in the world, and the reviewer, the collaborator, and
the person who finds the repository in 2031 are all on a different one. Code that
contains absolute paths does not fail loudly for them — it fails at the first read
step, before any analysis has run, and it fails in a way that looks like the user's
mistake rather than the author's.

Changing the working directory is the same problem wearing a disguise. A script that
begins by moving somewhere hard-coded works for whoever wrote it and nobody else, and
because the call sits at the top of the file it breaks the script for everyone before
they reach anything interesting. It also silently changes state for whatever runs
next in the same session.

Both are trivial to fix and trivially fatal to leave. That is why the first is
must-fix.


HOW TO SATISFY IT

Write every path relative to the project root, and let a helper find that root for
you rather than assuming where the working directory is.

  - R — open the project through its `.Rproj` file and build paths with
    `here::here("data", "raw.csv")`. Never call `setwd()` in a script. If you need a
    directory change for one operation, scope it: `withr::with_dir()`.
  - Python — build paths from the file's own location, e.g.
    `Path(__file__).resolve().parent / "data" / "raw.csv"`, or use a project-root
    helper such as `pyprojroot`. Never call `os.chdir()` in an analysis script.
  - Either — if a path must point outside the project (a shared drive, a large data
    store), read it from a config file or an environment variable, and document it in
    the README. Don't hard-code it.


EXAMPLES

Sufficient:

    here::here("data", "raw", "trials.csv")
    Path(__file__).resolve().parent / "data" / "raw" / "trials.csv"
    read_csv(Sys.getenv("TRIALS_DATA"))          # documented in the README

Not sufficient:

    setwd("C:/Users/selina/thesis")              # one machine
    read_csv("/home/ab/proj/data/trials.csv")    # one machine
    read_csv("../../data/trials.csv")            # depends where you launched R


--------------------------------------------------------------------------------
CRITERION 2 OF 3
--------------------------------------------------------------------------------

Title:      Random results can be reproduced exactly
Id:         randomness-is-reproducible
Group:      code-quality
Sources:    wilson-2017


CHECK 1
  Id:           seed-is-set
  Mode:         deterministic
  Severity:     must-fix
  Summary:      A random seed is set, wherever the analysis uses randomness
  Passes when:  present
  Evidence:
      R:        set.seed(
                withr::with_seed(
      Python:   np.random.default_rng(<integer>)
                np.random.seed(
                random.seed(
                torch.manual_seed(
      Any:      a seed value read from a config file by the analysis

CHECK 2
  Id:           seed-covers-every-stochastic-step
  Mode:         ai
  Severity:     should-fix
  Summary:      Every stochastic step is reproducible, not only the first one


WHY IT MATTERS

A bootstrap, a permutation test, a train/test split, a random initialisation: run the
script twice and the numbers differ. Without a seed, nobody — including the author six
months later — can tell whether a changed result means a changed method, a bug, or
ordinary sampling noise. The analysis becomes unauditable in the precise place where
auditing matters most, because these are the steps whose output people quote.

Setting a seed does not make an analysis reproducible across package versions or
platforms; random number generators do change. It makes it reproducible for the person
holding this code today, which is the claim a paper implicitly makes when it reports a
bootstrapped confidence interval.

If the analysis is entirely deterministic, this criterion does not apply, and both
checks are reported as "not applicable" rather than as failures.


HOW TO SATISFY IT

Set the seed once, near the top of each script that uses randomness, and commit the
value. A seed is data, not decoration — an arbitrary constant that you never change
afterwards.

  - R — `set.seed(20260709)` at the top of the script. For anything parallel, switch
    to a parallel-safe generator with `RNGkind("L'Ecuyer-CMRG")`, because per-worker
    seeds are not reproducible otherwise.
  - Python — prefer an explicit generator over the global one:
    `rng = np.random.default_rng(20260709)`, then pass `rng` into the functions that
    need it. The global `np.random.seed()` works but any library you call can quietly
    reset it.
  - Either — if a pipeline spans several scripts, each script sets its own seed. A
    seed set in `01_clean.R` does nothing for `03_bootstrap.R`.

Where a result is expensive to recompute, record the seed alongside the saved output
so the two can never drift apart.


EXAMPLES

Sufficient:

    set.seed(20260709)                # 02_split.R
    set.seed(20260709)                # 03_bootstrap.R  — its own seed

Not sufficient:

    set.seed(Sys.time())              # a seed nobody can reuse
    # 01_clean.R sets a seed; 03_bootstrap.R resamples with none


--------------------------------------------------------------------------------
CRITERION 3 OF 3
--------------------------------------------------------------------------------

Title:      The order in which scripts must run is obvious
Id:         run-order-discoverable
Group:      code-quality
Sources:    marwick-2018, cookiecutter-ds, nature-s44271


CHECK 1
  Id:           run-order-stated
  Mode:         ai
  Severity:     should-fix
  Summary:      A reader can tell which script to run first and which follow
                (when the analysis spans more than one script)
  Passes when:  present
  Evidence:
      Any:      numbered script prefixes (01_clean.R, 02_model.R, ...)
                a driver script (main.R, run_all.sh, make.R)
                a build file (Makefile, _targets.R, Snakefile, dvc.yaml)
                a "run these in order" section in the README


WHY IT MATTERS

A folder of six scripts with equally plausible names is a puzzle, and the reader
solves it by opening each one to see what it loads and what it writes. They will
usually guess right, and the times they guess wrong produce results that look
plausible and are wrong — a model fitted on data that was never cleaned.

The cost of stating the order is one line in a README or a two-digit prefix on each
filename. The cost of not stating it is paid by every person who reads the repository,
including the author after a year away.

(Whether the README explains *how to run* the analysis at all belongs to the
orientation group. This criterion is narrower: given that you can run a script,
does the repository tell you in what order?)


HOW TO SATISFY IT

Any one of these is enough — pick the lightest thing that fits the project.

  - Number the scripts. `01_clean.R`, `02_fit.R`, `03_figures.R`. Zero infrastructure,
    reads correctly in every file browser, and survives being emailed as a zip.
  - Write a driver script that calls them in order — `main.R`, `run_all.sh` — so the
    order is executable rather than described.
  - Use a build tool. `Makefile`, `_targets.R` (R), `Snakefile` (Python). Strongest
    option: the order is declared, and out-of-date steps are recomputed. Worth it once
    the pipeline is slow enough that you don't want to rerun all of it.
  - At minimum, a short ordered list in the README.

If a single script does everything, this criterion does not apply.


EXAMPLES

Sufficient:

    R/01_clean.R   R/02_fit.R   R/03_figures.R
    make.R                      # source()s the three in order
    README.md                   # "Run 01_clean.R, then 02_fit.R, then 03_figures.R."

Not sufficient:

    analysis.R   clean.R   figures.R   model.R   utils.R    # which one is first?


--------------------------------------------------------------------------------
WHAT TO NOTICE
--------------------------------------------------------------------------------

Three criteria, one group. They will appear in the report under a single "Code"
heading, as five consecutive lines, with no visible boundary between the criteria.

Modes. Three checks are deterministic — a script can settle them with a regex, and
its verdict is final. Two need judgement about content, so they are ai. None of them
is mode: none, because everything here is visible in the repository.

Passes when. Criterion 1 is a remove-a-thing criterion: both its checks pass by
absence, and their evidence lists the violations to hunt for, not the artefacts to
find. Criteria 2 and 3 are add-a-thing criteria. Notice that the summary is phrased as
the good state in all five checks — "No absolute filesystem paths appear" — so that a
green tick reads as a sentence and a red cross names the target.

Evidence takes four different shapes. Violation patterns to search for (criterion 1).
Function calls that indicate the good state (criterion 2, check 1). Structural
artefacts: filename conventions, a driver script, a README section (criterion 3).
And nothing at all (criterion 2, check 2) — "is every stochastic step covered?" is a
judgement over content that cites what it finds at review time, so there is no list to
write in advance. Evidence is optional for ai checks, exactly for this reason.

Suppression. In criterion 2, if `seed-is-set` fails then `seed-covers-every-stochastic-
step` is reported as "not applicable": there is no seed whose coverage could be
assessed. In criterion 1 the two checks are independent — an absolute path and a
`setwd()` are separate faults, and a repository can commit either without the other —
so both can fail at once, and both should.

Conditional criteria. Criterion 2 does not apply to a deterministic analysis, and
criterion 3 does not apply to a single-script repository. Neither gets a special
field: the condition is written into the check summary and explained in the prose.
The reviewer reports "not applicable" and says why.

Severity. Only two checks are must-fix, and both make the code unrunnable by a
stranger. Everything else is should-fix. If most of your checks are must-fix, the
digest at the top of the report stops prioritising anything.
