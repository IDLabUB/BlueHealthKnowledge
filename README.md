# BlueHealthKnowledge
[![Website](https://img.shields.io/badge/site-bluehealthknowledge.github.io-informational.svg)](https://bluehealthknowledge.github.io/)

`BlueHealthKnowledge` project repository: a knowledge base and suite of automated analyses that catalogue every documented factor linking the sea to physical and mental health and overall wellbeing.
The definitive project guidance is maintained directly on the repository's `main` branch so collaborators always reference and contribute to the canonical instructions here, rather than on temporary feature branches.

## Overview

Blue spaces such as seas and oceans are increasingly recognised for the restorative benefits they provide to people and communities.
This project explores the breadth of scientific evidence on how marine environments influence physical health, mental health, and holistic wellbeing outcomes.
We combine automated literature collection with targeted knowledge curation to catalogue protective, promotive, and risk factors linked to time spent in, on, or near the sea.

In particular, we document how marine settings contribute to:

- **Physical health pathways** such as opportunities for active transport, sport, and exposure to marine aerosols.
- **Mental health pathways** including stress reduction, restoration, and pro-social interactions fostered by coastal spaces.
- **Community wellbeing** through equitable access, cultural practices, blue-economy livelihoods, and climate resilience.

The results of this project are hosted online on the [project website](https://osf.io/ats8c/).

## Project Guide

The goal of this project is to map, analyse, and explain the factors that relate marine environments to human health and wellbeing.
To achieve this, we manually curate a dictionary of blue-health factors that span environmental characteristics (for example water quality, biodiversity, accessibility), behavioural pathways (such as physical activity, social connection, and nature engagement), and health outcomes.
We iteratively expand these terms to ensure comprehensive coverage of all documented links between the sea and human wellbeing, including emerging evidence on climate change, ecosystem services, and socio-economic determinants.
This living list of terms is available in the `terms` sub-folder and viewable in the `SearchTerms` notebook.

For data collection, this project uses two main approaches:
- The 'Words' approach gathers text and metadata (e.g., authors, journals, keywords, and publication date) from all articles identified through blue-health search terms.
  This data is used to build profiles of marine-related health factors, highlight the intensity of research activity, and surface knowledge gaps.
- The 'Count' approach collects data on the co-occurrence of sea-related terms and other pre-defined concepts of interest, including psychological, social, environmental, and policy dimensions.
  This data is used to analyze patterns and relationships between different determinants of blue health and to prioritise combinations of factors for deeper qualitative synthesis.

The project analyses trends in the literature to provide insights into how contact with the sea promotes or hinders physical and mental health, supports wellbeing, mitigates inequalities, and informs policy and practice interventions.

You can explore the outputs of this project by visiting the [project website](https://osf.io/ats8c/), which features individual profiles of the examined blue-health factors and group-level analyses.

For details on how the project was conducted and to view the underlying code, you can explore this repository.
As a starting point, the `notebooks` provide an overview of the approach used in this project. To conduct similar literature analyses, refer to the [LISC](https://github.com/lisc-tools/lisc) tool.

## Reference

This project is described in the following paper (in preparation):

    [Authors] (2025). Mapping blue health evidence: exploring marine factors linked to physical and mental wellbeing. DOI: [Placeholder DOI]

Direct link: [Placeholder DOI]

## Requirements

This project is written in Python 3 and requires Python >= 3.7 to run.

The project requires standard scientific Python libraries, listed in `requirements.txt`, which can be installed via [Anaconda Distribution](https://www.anaconda.com/distribution/).

Additional requirements include:
- [lisc](https://github.com/lisc-tools/lisc) >= 0.2.0

## Repository Layout

This project repository is organized in the following way:

- `build_site/` contains scripts to create the project website
- `code/` contains the code used for this project
- `docs/` contains the files that define the project website
- `notebooks/` contains Jupyter notebooks detailing the project workflow
- `scripts/` contains scripts for data collection and analysis
- `terms/` contains all the search terms used for literature collection and categorisation of blue-health factors

To re-run the analyses using the existing dataset, download the dataset (see below) and add it to a `data` folder within the project directory.

You can also run a new data collection using the terms defined in the `terms` sub-folder and the data collection scripts in the `scripts` sub-folder.

The primary data analyses are conducted in the `notebooks` after data collection.

## Data

This project uses literature data that documents the relationships between marine environments and human health.

The literature dataset collected and analyzed in this project is openly available at this [OSF repository](https://osf.io/ats8c/).
