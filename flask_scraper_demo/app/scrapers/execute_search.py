import pandas as pd

from .ifc_scraper import scrape_ifc
from .worldbank_scraper import scrape_world_bank

SCRAPERS = [
    (scrape_ifc, 'IFC'),
    (scrape_world_bank, 'World Bank'),

    # NOTE: Uncomment as these are implemented.
    # (scrape_miga, 'MIGA'),
    # (scrape_afdb, 'AfDB'),
    # (scrape_eib, 'EIB'),
    # (scrape_ebrd, 'EBRD'),
    # (scrape_adb, 'ADB'),
    # (scrape_aiib, 'AIIB'),
    # (scrape_idb, 'IDB'),
    # (scrape_opic, 'OPIC'),
    # (scrape_fmo, 'FMO'),
    # (scrape_cdc, 'CDC'),
    # (scrape_bio, 'BIO'),
    # (scrape_kfw, 'KfW')
]


def execute_search(search_term):
    """
    iterate through scrapers and merge results.
    output columns: 'Project Name', 'URL', 'Status', 'DFI', 'Search Term'
    """
    df = pd.DataFrame([], columns=['Project Name', 'URL', 'Status', 'DFI'])
    print("#" * 30)
    print('Searching for Term:', search_term)

    # TODO: optional - run these asynchronously
    for scraper, name in SCRAPERS:
        print('Scraping:', name)
        df = df.append(scraper(search_term))

    df['Search Term'] = search_term
    return df
