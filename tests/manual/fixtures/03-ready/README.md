# Urban pollinator analysis

This example analysis estimates how pollinator observations vary with urban
green-space coverage. It is a synthetic, publication-ready fixture used to test
repo-reviewer; it does not contain real observations.

## Reproduce the analysis

Use Python 3.12, install the exact dependencies in `requirements.txt`, and run
`python analysis/run_analysis.py` from the repository root. The script generates
its synthetic input internally and writes `outputs/pollinator-summary.txt`.

## Repository structure

- `analysis/run_analysis.py` is the analysis entry point.
- `outputs/` contains generated results and may initially be empty.

No research data are distributed with this fixture. The MIT licence in `LICENSE`
covers the code and documentation.
