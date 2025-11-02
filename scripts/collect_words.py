#!/usr/bin/env python3
"""Script to run words collection for the BlueHealthKnowledge project."""

# --- Silenciar avisos de BeautifulSoup a tot l'script ---
from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
# ---------------------------------------------------------

from pathlib import Path
import os
from typing import List
from requests import RequestException

from lisc import Words
from lisc.utils import SCDB, save_object, load_api_key

# -------------------- Config --------------------
TEST = os.environ.get('BLUEHEALTH_TEST_MODE', '0') == '1'
LABEL = 'test' if TEST else 'blue_health_factors'

# Rutes robustes des de l’arrel del repo (assumim que aquest fitxer és a ./scripts/)
REPO_ROOT = Path(__file__).resolve().parent.parent
DB_ROOT   = REPO_ROOT                  # SCDB crearà ./data sota aquesta arrel
TERMS_DIR = REPO_ROOT / 'terms'
API_FILE  = REPO_ROOT / 'api_key.txt'

# e-utils
FIELD  = 'TIAB'
RETMAX = 5 if TEST else int(os.environ.get('BLUEHEALTH_RETMAX', '10000'))

# Execució / log
SAVE_N_CLEAR = False if TEST else True
LOGGING = None
VERBOSE = False if TEST else True
# ------------------------------------------------

def _prepare_directories(scdb: SCDB) -> None:
    """Assegura carpetes SCDB per a outputs de Words."""
    for key in ('words', 'raw', 'summary'):
        p = Path(scdb.get_folder_path(key))
        p.mkdir(parents=True, exist_ok=True)
        print("Directori preparat:", p.resolve())

def main():
    # Gestió de directoris (NO és el mateix que el 'db'='pubmed' de LISC)
    scdb = SCDB(str(DB_ROOT))
    api_key = load_api_key(str(API_FILE))
    _prepare_directories(scdb)

    words = Words()

    if TEST:
        # Mini conjunt de prova sense carregar PubMed en excés
        words.add_terms([['P100'], ['N100']])
        words.add_terms([['protein'], ['protein']], term_type='exclusions')
    else:
        # Dimensió A (factors) + exclusions + etiquetes
        words.add_terms('blue_health_factors.txt', directory=str(TERMS_DIR))
        words.add_terms('erps_exclude.txt', term_type='exclusions', directory=str(TERMS_DIR))
        words.add_labels('blue_health_factor_labels.txt', directory=str(TERMS_DIR))

    print('\n\nRUNNING WORDS COLLECTION\n')

    # IMPORTANT: 'db' ha de ser la cadena 'pubmed' (no l’objecte SCDB)
    run_kwargs = {
        'db'          : 'pubmed',
        'retmax'      : RETMAX,
        'field'       : FIELD,
        'save_n_clear': SAVE_N_CLEAR,
        'logging'     : LOGGING,
        'verbose'     : VERBOSE,
        'usehistory'  : not TEST,
        'api_key'     : None if TEST else api_key,
    }

    try:
        words.run_collection(**run_kwargs)
    except RequestException as exc:  # xarxa / PubMed
        print(
            '\nNetwork error while contacting PubMed. '
            'Switching to offline mode and creating an empty words structure.\n'
        )
        words.meta_data = {'error': str(exc), 'note': 'Offline placeholder generated.'}
        words.results = []
        words.combined_results = []

    # Desa l’objecte Words a la carpeta SCDB “words/”
    out_dir = Path(scdb.get_folder_path('words'))
    save_object(words, f'words_{LABEL}', directory=str(out_dir))

    print('\n\nWORDS COLLECTION FINISHED\n')

if __name__ == "__main__":
    main()
