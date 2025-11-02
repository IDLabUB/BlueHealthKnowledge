#!/usr/bin/env python3
from pathlib import Path
from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

"""Script to run counts collection for BlueHealthKnowledge factors and associations."""

import os, re
from typing import List
from requests import RequestException
import numpy as np

from lisc import Counts
from lisc.utils import save_object, load_api_key

###################################################################################################
# Paths i configuració

# arrel del repo independentment del "working dir"
REPO_ROOT  = Path(__file__).resolve().parent.parent
TERMS_DIR  = REPO_ROOT / "terms"
API_FILE   = REPO_ROOT / "api_key.txt"

# Carpeta per desar els resultats (sense el legacy data/)
COUNTS_DIR = REPO_ROOT / "counts"
COUNTS_DIR.mkdir(parents=True, exist_ok=True)

# Mode prova (exporta BLUEHEALTH_TEST_MODE=1 per evitar crides a PubMed)
TEST = os.environ.get('BLUEHEALTH_TEST_MODE', '0') == '1'

# Paràmetres de col·lecció
LOGGING = None
VERBOSE = True

# Debug ràpid
print("Factors file:", (TERMS_DIR / 'blue_health_factors.txt').resolve())

###################################################################################################

def _load_term_groups(path: Path) -> List[List[str]]:
    """
    Carrega grups de termes des d'un .txt.
    - Cada línia és un grup de sinònims.
    - Separadors permesos: coma, punt i coma, tub '|' o tab.
    - Línies buides o amb '#' es descarten.
    """
    if not path.exists():
        raise FileNotFoundError(f"No s'ha trobat el fitxer de termes: {path}")
    groups: List[List[str]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in re.split(r"[;,|\t]", line) if p.strip()]
            if parts:
                groups.append(parts)
    if not groups:
        raise ValueError(f"No s'han trobat termes a {path}")
    return groups

###################################################################################################

def run_counts_collection(label: str, api_key: str):
    """
    Run counts collection per a un 'label' de la dimensió B.

    Dimensió A (primària):
      - blue_health_factors.txt
      - erps_exclude.txt      (exclusions)
      - blue_health_factor_labels.txt (labels)

    Dimensió B (secundària):
      - terms/{label}.txt
    """
    counts = Counts()

    if TEST:
        # Exemple mínim de prova
        counts.add_terms([['Antisocial attitudes'], ['Unemployment'], ['Impulsivity']], dim='A')
        counts.add_terms([['coastal residence'], ['contemplation of water']], dim='B')
    else:
        counts.add_terms('blue_health_factors.txt', dim='A', directory=str(TERMS_DIR))
        counts.add_terms('erps_exclude.txt', term_type='exclusions', dim='A', directory=str(TERMS_DIR))
        counts.add_labels('blue_health_factor_labels.txt', dim='A', directory=str(TERMS_DIR))

        if label != 'erp':
            secondary_terms = _load_term_groups(TERMS_DIR / f"{label}.txt")
            counts.add_terms(secondary_terms, dim='B')

    print(f"\n\nRUNNING COUNTS COLLECTION for: {label}\n")
    try:
        counts.run_collection(db='pubmed', api_key=api_key, logging=LOGGING, verbose=VERBOSE)
    except RequestException as e:
        raise SystemExit(f"[error] Request to PubMed failed: {e}")

    # Desa l'objecte counts a ./counts
    save_object(counts, f"counts_{label}", directory=str(COUNTS_DIR))
    print(f"\nCOUNTS COLLECTION FINISHED for: {label}\n")

###################################################################################################

def main():
    # Carrega API key (fitxer a l'arrel del repo)
    api_key = load_api_key(str(API_FILE))

    # Executa per a les dues dimensions B principals
    for label in ['blue_health_activities', 'blue_health_exposure_metrics']:
        run_counts_collection(label, api_key)

if __name__ == "__main__":
    main()
