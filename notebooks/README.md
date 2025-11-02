# BlueHealthKnowledge — Project Notebooks

This folder contains the notebooks used to **automate evidence mapping for Blue Health**.  
The project synthesizes literature on the associations between:

- **Blue-health factors** (psychological, social, cognitive, and physiological outcomes), and
- **Blue-environment exposures**, captured as **activities** (e.g., swimming, kayaking, sailing) and **exposure metrics** (e.g., distance to coast, viewshed, time near water).

Automated collection is performed with the `lisc` pipeline (PubMed e-utilities), and results are saved under `data/words/` and `counts/` (with figures in `counts/figures/...`). Terms and exclusions are defined in `./terms`.

## Notebooks overview

### 00-Background
Introduces aims, data sources (PubMed), and the high-level workflow (terms → words → counts → analyses). Provides a quick exploratory overview of the Blue Health literature.

### 01-SearchTerms
Defines and validates the **vocabularies**:
- `blue_health_factors.txt` (outcomes),
- `blue_health_activities.txt` and `blue_health_exposure_metrics.txt` (exposures),
- paired **exclusions** files to avoid off-topic hits (e.g., acronym collisions).

### 02-WordsAnalyses
Runs `collect_words` for factors (and optionally exposures), drops low-frequency components, and summarizes term usage. Produces word summaries and basic plots to inspect term quality.

### 03-WordsNetwork
Builds a term network from words data (e.g., co-occurrence / cosine). Computes basic centrality metrics and visualizes communities to understand the structure of the Blue Health vocabulary.

### 04-CountsActivities
Analyzes **associations between blue-health factors and activities** using `counts_blue_health_activities.p`.  
Steps:
- Drop low-frequency items and normalize scores,
- Export full score matrix to CSV,
- Write JSONs with top associations (A→B and B→A),
- Plot clustermap and dendrograms.  
Outputs are saved under:
