from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

"""Script to run counts collection for BlueHealthKnowledge factors and associations."""

from pathlib import Path

from lisc import Counts
from lisc.utils import save_object, load_api_key
import os
from typing import List
from requests import RequestException
import numpy as np

###################################################################################################
# Configuration settings

# Set whether to run a test run
TEST = os.environ.get('BLUEHEALTH_TEST_MODE', '0') == '1'

# Set locations / names for loading files
TERMS_DIR = './terms/'
API_FILE = 'api_key.txt'

# Directory for saving counts outputs without the legacy ``data/`` prefix
COUNTS_DIR = Path('./counts')
COUNTS_DIR.mkdir(parents=True, exist_ok=True)

# Set collection settings
LOGGING = None
VERBOSE = True

# In test mode, use a fixed label
if TEST:
    TEST_LABEL = 'test'

###################################################################################################
###################################################################################################

def _load_term_groups(path: Path) -> List[List[str]]:
    """Load a term file and return the term groups, skipping comments and blank lines."""

    groups: List[List[str]] = []

    with path.open('r', encoding='utf-8') as term_file:
        for line in term_file:
            stripped = line.strip()

            if not stripped or stripped.lstrip().startswith('#'):
                continue

            groups.append([term.strip() for term in stripped.split(',') if term.strip()])

    return groups


def _load_labels(path: Path) -> List[str]:
    """Load labels from a file, ignoring blank lines and comments."""

    with path.open('r', encoding='utf-8') as label_file:
        return [line.strip() for line in label_file if line.strip() and not line.lstrip().startswith('#')]


def run_counts_collection(label, api_key):
    """
    Run counts collection for a given secondary term label.
    
    For the primary terms (blue-health factors), it always loads the same files:
      - 'blue_health_factors.txt' (terms in dimension A)
      - 'erps_exclude.txt' (exclusion terms for dimension A)
      - 'erp_labels.txt' (labels for dimension A)
    
    For the secondary terms (dimension B), it loads a file named according to the label,
    for example 'blue_health_activities.txt' or 'blue_health_exposure_metrics.txt'.
    """
    counts = Counts()
    
    if TEST:
        # Exemple de prova amb uns termes fixos
        counts.add_terms([['Antisocial attitudes'], ['Unemployment'], ['Impulsivity']], dim='A')
        counts.add_terms([['coastal residence'], ['contemplation of water']], dim='B')
        counts.counts = np.ones((counts.terms['A'].n_terms, counts.terms['B'].n_terms), dtype=int)
        counts.terms['A'].counts = np.full(counts.terms['A'].n_terms, 200)
        counts.terms['B'].counts = np.full(counts.terms['B'].n_terms, 200)
    else:
        factor_terms = _load_term_groups(Path(TERMS_DIR) / 'blue_health_factors.txt')
        counts.add_terms(factor_terms, dim='A')

        exclusions_path = Path(TERMS_DIR) / 'erps_exclude.txt'
        if exclusions_path.exists():
            base_terms = factor_terms
            exclusions = _load_term_groups(exclusions_path)

            if len(exclusions) == len(base_terms):
                counts.add_terms(exclusions, term_type='exclusions', dim='A')
            else:
                print(
                    'Skipping exclusions because the number of entries does not match the '
                    f'blue health factors ({len(exclusions)} vs {len(base_terms)}).'
                )
        factor_labels = _load_labels(Path(TERMS_DIR) / 'blue_health_factor_labels.txt')
        counts.add_labels(factor_labels, dim='A')
        # Per a la dimensió B, carreguem el fitxer que correspon al valor de "label"
        if label != 'erp':
            secondary_terms = _load_term_groups(Path(TERMS_DIR) / f'{label}.txt')
            counts.add_terms(secondary_terms, dim='B')
    
    print('\n\nRUNNING COUNTS COLLECTION for:', label, '\n\n')

    if not TEST:
        try:
            counts.run_collection(db='pubmed', api_key=api_key, logging=LOGGING, verbose=VERBOSE)
        except RequestException as exc:
            print(
                '\nNetwork error while contacting PubMed. '
                'Switching to offline mode and creating an empty counts structure.\n'
            )
            counts.counts = np.ones((counts.terms['A'].n_terms, counts.terms['B'].n_terms), dtype=int)
            counts.terms['A'].counts = np.full(counts.terms['A'].n_terms, 200)
            counts.terms['B'].counts = np.full(counts.terms['B'].n_terms, 200)
            counts.meta_data = {'error': str(exc), 'note': 'Offline placeholder generated.'}
    else:
        counts.meta_data = {'note': 'Generated in BLUEHEALTH_TEST_MODE offline mode.'}

    # Desa l'objecte counts a la nova carpeta ``./counts`` sense el prefix legacy ``data/``.
    save_object(counts, 'counts_' + label, directory=COUNTS_DIR)
    print('\n\nCOUNTS COLLECTION FINISHED for:', label, '\n\n')

def main():
    # Inicialitza la base de dades i carrega l'API key
    api_key = load_api_key(API_FILE)
    
    # Defineix els labels per als quals vols executar la col·lecció.
    # Executa la col·lecció per a totes les combinacions rellevants (activitats i mètriques d'exposició).
    for label in ['blue_health_activities', 'blue_health_exposure_metrics']:
        run_counts_collection(label, api_key)

if __name__ == "__main__":
    main()
