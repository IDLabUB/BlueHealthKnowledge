# BlueHealthKnowledge Term Resources

This directory collects the text resources that power the BlueHealthKnowledge literature searches and downstream analyses. Each file supplies a curated set of synonyms that describe how marine environments interact with human health and wellbeing.

For a guided tour of how these vocabularies are used during data collection, open the [01-SearchTerms notebook](../notebooks/01-SearchTerms.ipynb) in this repository.

## Blue-health wellbeing factors

- `blue_health_factors.txt` &mdash; the comprehensive catalogue of marine-linked wellbeing factors and outcome terms.
- `blue_health_factor_labels.txt` &mdash; short human-readable labels for the factors list that keep figures and tables tidy.

## Exposure metrics and activity pathways

- `blue_health_exposure_metrics.txt` &mdash; measures of proximity, contact, quality, and other exposure routes to blue spaces.
- `blue_health_activities.txt` &mdash; activities people undertake in marine settings, from contemplative engagement to high-exertion sports.

## ERP resources

- `erp_labels.txt` &mdash; labels used for each ERP term.
- `erps_exclude.txt` &mdash; customized exclusion terms for each ERP.
- `latencies.txt` &mdash; canonical latencies for each ERP.

Each ERP-related file should contain the same number of lines, with matching indices referring to the same ERP. Blank lines indicate there is no entry for that ERP in the given file.

## Additional analysis lists

- `analysis_exclusions.txt` &mdash; general terms excluded from the analysis of common keywords, words, and similar outputs.
- `disease.txt` &mdash; association terms covering disease outcomes of interest.
- `dropped_erps.txt` &mdash; ERPs dropped for having too few results (but returning at least one hit).
- `sensory_erps.txt` &mdash; ERPs with canonical latencies below 100 ms that were excluded from the analyses.

These resources are referenced throughout the data collection scripts in `scripts/` and the analysis notebooks in `notebooks/`. When adding new terms, keep the comma-separated format (canonical term followed by synonyms) so existing parsers continue to work.
