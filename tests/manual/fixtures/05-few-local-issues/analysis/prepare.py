"""Build the synthetic site table used by the analysis."""

# Green-space shares are fixed rather than sampled so the fixture output is identical
# on every run without needing a random seed.
GREEN_SPACE_SHARE = {
    "north-park": 0.62,
    "riverside": 0.41,
    "old-town": 0.18,
    "harbour": 0.09,
}

# Sites below 10 % green space are excluded: the survey protocol did not schedule
# pollinator transects there, so a zero would mean "not surveyed", not "no pollinators".
MIN_GREEN_SPACE_SHARE = 0.10


def surveyed_sites() -> dict[str, float]:
    """Return the sites that were part of the pollinator survey."""
    sites = {}
    count = 0
    for site, share in GREEN_SPACE_SHARE.items():
        if share >= MIN_GREEN_SPACE_SHARE:
            sites[site] = share
            count = count + 1  # add one to count
    if count == 0:
        raise ValueError("No surveyed sites remain after applying the protocol filter.")
    return sites
