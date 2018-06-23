import pandas as pd

from .ifc_scraper import scrape_ifc
from .worldbank_scraper import scrape_world_bank
from .adb_scraper import adb_scraper
from .afdb_scraper import scrape_afdb
from .eib_scraper import scrape_eib
from .bio_scraper import scrape_bio
from .fmo_scraper import scrape_fmo
from .miga_scraper import scrape_miga


SELECT_ALL_NAME = 'All'

SCRAPER_MAP = {
    'IFC': scrape_ifc,
    'World Bank': scrape_world_bank,

    # NOTE: Uncomment as these are implemented.
    'MIGA': scrape_miga,
     'EIB': scrape_eib,
    # 'EBRD': scrape_ebrd,
    'Asian Development Bank': adb_scraper,
    'African Development Bank': scrape_afdb,
    # 'AIIB': scrape_aiib,
    # 'IDB': scrape_idb,
    # 'OPIC': scrape_opic,
     'FMO': scrape_fmo,
    # 'CDC': scrape_cdc,
    'BIO': scrape_bio,
    # 'KfW': scrape_kfw,
}


def execute_search(search_term, scraper_names):
    """
    iterate through scrapers and merge results.
    output columns: 'Project Name', 'URL', 'Status', 'DFI', 'Search Term'
    """
    df = pd.DataFrame([], columns=['Project Name', 'URL', 'Status', 'DFI'])
    if not (search_term and scraper_names):
        return df

    search_term_quoted = add_quotations_if_not_already(search_term)

    print("#" * 30)
    print('Searching for Term:', search_term_quoted)

    if SELECT_ALL_NAME in scraper_names:
        scraper_names = SCRAPER_MAP.keys()

    # TODO: optional - run these asynchronously
    for name in scraper_names:
        scraper = SCRAPER_MAP.get(name)
        if not scraper:
            print(' - ERROR: scraper name {} not found'.format(name))
            print('   ... skipping scraper')
            continue

        print('Scraping:', name)
        df = df.append(scraper(search_term_quoted))

    df['Search Term'] = search_term
    return df


def add_quotations_if_not_already(search_term):
    if not search_term:
        return '""'

    return '{}{}{}'.format(
        '"' if search_term[0] != '"' else '',
        search_term,
        '"' if search_term[-1] != '"' else '',
    )
