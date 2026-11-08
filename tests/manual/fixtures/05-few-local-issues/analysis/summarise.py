"""Turn the site table into expected pollinator observations."""

# Observations per transect at 100 % green space, taken from the synthetic
# calibration in the fixture description; a linear model keeps the example readable.
OBSERVATIONS_AT_FULL_COVER = 20


def expected_observations(sites: dict[str, float]) -> dict[str, int]:
    """Return the expected observation count for each surveyed site."""
    expected = {}
    # loop over the sites
    for site, share in sites.items():
        # Round down because a transect records whole observations only.
        expected[site] = int(share * OBSERVATIONS_AT_FULL_COVER)
    return expected


def format_summary(expected: dict[str, int]) -> str:
    """Format one line per site, sorted by name so the output file is stable."""
    lines = [f"{site}: {count}" for site, count in sorted(expected.items())]
    return "\n".join(lines) + "\n"
