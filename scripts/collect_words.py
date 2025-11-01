# """Script to run words collection for the BlueHealthKnowledge project."""

import os
import pickle
import pandas as pd
from lisc import Words
from lisc.utils import SCDB, save_object, load_api_key

###################################################################################################
###################################################################################################

# Set whether to run a test run
TEST = False

# Set label for collection
LABEL = 'blue_health_factors'

# Set locations / names for loading files
# (Comprova que aquestes rutes siguin correctes segons la teva estructura de carpetes)
DB_NAME = './data'
TERMS_DIR = './terms/'
API_FILE = 'api_key.txt'

# Set e-utils settings
FIELD = 'TIAB'
RETMAX = 10000

# Set collection settings
SAVE_N_CLEAR = True
LOGGING = None

# Update settings for test run
if TEST:
    LABEL = 'test'
    RETMAX = 5
    SAVE_N_CLEAR = False

###################################################################################################
###################################################################################################

def main():
    # Inicialitza la base de dades i carrega l'API key
    db = SCDB(DB_NAME)
    api_key = load_api_key(API_FILE)

    words = Words()

    if TEST:
        words.add_terms([['P100'], ['N100']])
        words.add_terms([['protein'], ['protein']], term_type='exclusions')
    else:
        words.add_terms('blue_health_factors.txt', directory=TERMS_DIR)
        words.add_terms('erps_exclude.txt', term_type='exclusions', directory=TERMS_DIR)
        words.add_labels('blue_health_factor_labels.txt', directory=TERMS_DIR)

    print('\n\nRUNNING WORDS COLLECTION')

    # Abans de córrer la col·lecció, assegura't que existeix el directori on es desaran els resultats.
    # Atenció: segons l'estructura interna de lisc, si DB_NAME és '../data', la ruta final pot ser:
    # ../data/data/words/raw
    # Per tant, definim aquesta ruta:
    save_dir = os.path.join(DB_NAME, 'data', 'words', 'raw')
    os.makedirs(save_dir, exist_ok=True)
    print("Directori creat (si no existia):", save_dir)

    # Executa la col·lecció de paraules
    words.run_collection(db='pubmed', retmax=RETMAX, field=FIELD,
                         usehistory=True, api_key=api_key, save_and_clear=SAVE_N_CLEAR,
                         directory=db, logging=LOGGING, verbose=True)

    # Desa l'objecte Words per poder reutilitzar-lo més endavant
    save_object(words, 'words_' + LABEL, db)

    print('\n\nWORDS COLLECTION FINISHED\n\n')


if __name__ == "__main__":
    main()
