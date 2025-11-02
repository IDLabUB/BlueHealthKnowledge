# Counts artifacts

This directory stores derived summaries (`counts/summary/`), reverse-association lookups
(`counts/assocs/`), and any locally generated counts objects created by
`scripts/collect_counts.py`.

The `.p` pickle files that `scripts/counts_analysis.py` loads are produced by running the
collector and are now ignored by Git to avoid binary-only diffs on GitHub. After cloning the
repository, generate the required objects with:

```
python scripts/collect_counts.py
```

When the PubMed API cannot be reached, the collector automatically falls back to an offline
placeholder so the analysis script can still run. Once real data are available, rerun
`scripts/collect_counts.py` followed by `scripts/counts_analysis.py` to refresh the summaries and
associations checked into this folder.
