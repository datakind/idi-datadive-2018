import logging
import pandas as pd

from .ifc_scraper import scrape_ifc
from .worldbank_scraper import scrape_world_bank
from .adb_scraper import adb_scraper
from .afdb_scraper import scrape_afdb
from .eib_scraper import scrape_eib
from .bio_scraper import scrape_bio
from .fmo_scraper import scrape_fmo
from .miga_scraper import scrape_miga
from .ebrd_scraper import scrape_ebrd
from .opic_scraper import scrape_opic
from .kfw_api_scraper import scrape_kfw_api
from .kfw_search_scraper import scrape_kfw_search

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


SELECT_ALL_NAME = 'All'

SCRAPER_MAP = {
    'IFC': scrape_ifc,
    'World Bank': scrape_world_bank,

    # NOTE: Uncomment as these are implemented.
    # 'MIGA': scrape_miga,
    'EIB': scrape_eib,
    'EBRD': scrape_ebrd,
    'Asian Development Bank': adb_scraper,
    'African Development Bank': scrape_afdb,
    # 'AIIB': scrape_aiib,  # deprecated
    # 'IDB': scrape_idb,
    'OPIC': scrape_opic,
    'FMO': scrape_fmo,
    # 'CDC': scrape_cdc,  # deprecated
    'BIO': scrape_bio,
    'KFW API': scrape_kfw_api,
    'KFW Search': scrape_kfw_search,
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
        try:
            df = df.append(scraper(search_term))
        except Exception as e:
            logger.exception("The scraper {name} failed on the search {term}"
                             .format(name=name, term=search_term))
            failed_data = [['', '', '', name, search_term, str(e)]]
            results = pd.DataFrame(failed_data, columns=['Project Name', 'URL', 'Status', 'DFI', 'Search Term', 'Error'])
            df = df.append(results)

    df['Search Term'] = search_term
    return df
