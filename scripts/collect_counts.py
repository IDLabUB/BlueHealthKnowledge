from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

"""Script to run counts collection for BlueHealthKnowledge factors and associations."""

from lisc import Counts
from lisc.utils import SCDB, save_object, load_api_key
import os

###################################################################################################
# Configuration settings

# Set whether to run a test run
TEST = False

# Set locations / names for loading files
DB_NAME = '.'             # Use the project root so that SCDB crea la seva estructura interna correctament
TERMS_DIR = './terms/'
API_FILE = 'api_key.txt'

# Print absolute path for debugging (example: blue_health_factors.txt)
print(os.path.abspath(os.path.join(TERMS_DIR, 'blue_health_factors.txt')))

# Set collection settings
LOGGING = None
VERBOSE = True

# In test mode, use a fixed label
if TEST:
    TEST_LABEL = 'test'

###################################################################################################
###################################################################################################

def run_counts_collection(label, db, api_key):
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
    else:
        counts.add_terms('blue_health_factors.txt', dim='A', directory=TERMS_DIR)
        counts.add_terms('erps_exclude.txt', term_type='exclusions', dim='A', directory=TERMS_DIR)
        counts.add_labels('blue_health_factor_labels.txt', dim='A', directory=TERMS_DIR)
        # Per a la dimensió B, carreguem el fitxer que correspon al valor de "label"
        if label != 'erp':
            counts.add_terms(label + '.txt', dim='B', directory=TERMS_DIR)
    
    print('\n\nRUNNING COUNTS COLLECTION for:', label, '\n\n')
    counts.run_collection(db='pubmed', api_key=api_key, logging=LOGGING, verbose=VERBOSE)
    
    # Desa l'objecte counts utilitzant només el nom (sense ruta completa) perquè SCDB ja gestiona la ruta interna.
    save_object(counts, 'counts_' + label, db)
    print('\n\nCOUNTS COLLECTION FINISHED for:', label, '\n\n')

def main():
    # Inicialitza la base de dades i carrega l'API key
    db = SCDB(DB_NAME)
    api_key = load_api_key(API_FILE)
    
    # Defineix els labels per als quals vols executar la col·lecció.
    # En aquest exemple, es podria executar la col·lecció per activitats o mètriques d'exposició.
    for label in ['blue_health_factors']:
        run_counts_collection(label, db, api_key)

if __name__ == "__main__":
    main()
