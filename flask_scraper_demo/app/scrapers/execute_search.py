import pandas as pd

from .ifc_scraper import scrape_ifc
from .worldbank_scraper import scrape_world_bank
from .adb_scraper import adb_scraper


SELECT_ALL_NAME = 'All'

SCRAPER_MAP = {
    'IFC': scrape_ifc,
    'World Bank': scrape_world_bank,

    # NOTE: Uncomment as these are implemented.
    # 'MIGA': scrape_miga,
    # 'AfDB': scrape_afdb,
    # 'EIB': scrape_eib,
    # 'EBRD': scrape_ebrd,
    'ADB': adb_scraper,
    # 'AIIB': scrape_aiib,
    # 'IDB': scrape_idb,
    # 'OPIC': scrape_opic,
    # 'FMO': scrape_fmo,
    # 'CDC': scrape_cdc,
    # 'BIO': scrape_bio,
    # 'KfW': scrape_kfw,
}


def execute_search(search_term, scraper_names):
    """
    iterate through scrapers and merge results.
    output columns: 'Project Name', 'URL', 'Status', 'DFI', 'Search Term'
    """
    df = pd.DataFrame([], columns=['Project Name', 'URL', 'Status', 'DFI'])
    print("#" * 30)
    print('Searching for Term:', search_term)

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
        df = df.append(scraper(search_term))

    df['Search Term'] = search_term
    return df
