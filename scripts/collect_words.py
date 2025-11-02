# """Script to run words collection for the BlueHealthKnowledge project."""

from pathlib import Path
import os

from requests import RequestException

from lisc import Words
from lisc.utils import SCDB, save_object, load_api_key

###################################################################################################
###################################################################################################

# Set whether to run a test run (also honoured if BLUEHEALTH_TEST_MODE=1)
TEST = os.environ.get('BLUEHEALTH_TEST_MODE', '0') == '1'

# Set label for collection
LABEL = 'blue_health_factors'

# Set locations / names for loading files
# (Comprova que aquestes rutes siguin correctes segons la teva estructura de carpetes)
DB_ROOT = Path('.')
TERMS_DIR = Path('./terms')
API_FILE = 'api_key.txt'

# Set e-utils settings
FIELD = 'TIAB'
RETMAX = 10000

# Set collection settings
SAVE_N_CLEAR = True
LOGGING = None
VERBOSE = True

# Update settings for test run
if TEST:
    LABEL = 'test'
    RETMAX = 5
    SAVE_N_CLEAR = False
    VERBOSE = False

###################################################################################################
###################################################################################################


def _prepare_directories(db: SCDB) -> None:
    """Ensure SCDB-managed directories exist for storing words outputs."""

    for folder_key in ('words', 'raw', 'summary'):
        folder_path = Path(db.get_folder_path(folder_key))
        folder_path.mkdir(parents=True, exist_ok=True)
        print("Directori preparat:", folder_path.resolve())


def main():
    # Inicialitza la base de dades i carrega l'API key
    db = SCDB(str(DB_ROOT))
    api_key = load_api_key(API_FILE)

    _prepare_directories(db)

    words = Words()

    if TEST:
        words.add_terms([['P100'], ['N100']])
        words.add_terms([['protein'], ['protein']], term_type='exclusions')
    else:
        words.add_terms('blue_health_factors.txt', directory=TERMS_DIR)
        words.add_terms('erps_exclude.txt', term_type='exclusions', directory=TERMS_DIR)
        words.add_labels('blue_health_factor_labels.txt', directory=TERMS_DIR)

    print('\n\nRUNNING WORDS COLLECTION')

    if TEST:
        run_kwargs.update({'usehistory': False, 'api_key': None})

    try:
        words.run_collection(**run_kwargs)
    except RequestException as exc:  # pragma: no cover - network dependent
        print(
            '\nNetwork error while contacting PubMed. '
            'Switching to offline mode and creating an empty words structure.\n'
        )
        words.meta_data = {'error': str(exc), 'note': 'Offline placeholder generated.'}
        words.results = []
        words.combined_results = []

    # Desa l'objecte Words per poder reutilitzar-lo més endavant
    save_object(words, 'words_' + LABEL, db)

    print('\n\nWORDS COLLECTION FINISHED\n\n')


if __name__ == "__main__":
    main()
