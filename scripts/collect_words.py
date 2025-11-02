"""Script to run words collection for the BlueHealthKnowledge project."""

from pathlib import Path
import os
from typing import List

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
RETMAX = int(os.environ.get('BLUEHEALTH_RETMAX', '10000'))

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


def _load_term_groups(path: Path) -> List[List[str]]:
    """Load term groups from a comma-separated term file, skipping comments and blanks."""

    groups: List[List[str]] = []

    with path.open('r', encoding='utf-8') as term_file:
        for line in term_file:
            stripped = line.strip()

            if not stripped or stripped.lstrip().startswith('#'):
                continue

            groups.append([term.strip() for term in stripped.split(',') if term.strip()])

    return groups


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
        factor_terms = _load_term_groups(TERMS_DIR / 'blue_health_factors.txt')
        words.add_terms('blue_health_factors.txt', directory=str(TERMS_DIR))

        exclusions_path = TERMS_DIR / 'erps_exclude.txt'
        if exclusions_path.exists():
            exclusions = _load_term_groups(exclusions_path)
            if len(exclusions) == len(factor_terms):
                words.add_terms('erps_exclude.txt', term_type='exclusions', directory=str(TERMS_DIR))
            else:
                print(
                    'Skipping exclusions because the number of entries does not match the '
                    f'blue health factors ({len(exclusions)} vs {len(factor_terms)}).'
                )
        label_count = len(_load_term_groups(TERMS_DIR / 'blue_health_factor_labels.txt'))
        if label_count == len(factor_terms):
            words.add_labels('blue_health_factor_labels.txt', directory=str(TERMS_DIR))
        else:
            print(
                'Skipping labels because the number of entries does not match the '
                f'blue health factors ({label_count} vs {len(factor_terms)}).'
            )

    print('\n\nRUNNING WORDS COLLECTION\n\n')

    run_kwargs = dict(
        db='pubmed',
        retmax=RETMAX,
        field=FIELD,
        usehistory=True,
        api_key=api_key,
        save_and_clear=SAVE_N_CLEAR,
        directory=db,
        logging=LOGGING,
        verbose=VERBOSE,
    )

    if TEST:
        run_kwargs.update({'usehistory': False, 'api_key': None})

    try:
        words.run_collection(**run_kwargs)
    except (RequestException, AttributeError) as exc:  # pragma: no cover - network dependent
        print(
            '\nError while contacting or parsing data from PubMed. '
            'Switching to offline mode and creating an empty words structure.\n'
        )
        partial_results = bool(getattr(words, 'results', None))
        words.meta_data = {
            'error': str(exc),
            'note': (
                'Partial results retained after collection failure.'
                if partial_results
                else 'Offline placeholder generated due to collection failure.'
            ),
        }
        if not partial_results:
            words.results = []
            words.combined_results = []

    # Desa l'objecte Words per poder reutilitzar-lo més endavant
    save_object(words, 'words_' + LABEL, db)

    print('\n\nWORDS COLLECTION FINISHED\n\n')


if __name__ == "__main__":
    main()
