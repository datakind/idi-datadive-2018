import pandas as pd

from ifc_scraper import scrape_IFC

SCRAPERS = [(scrape_IFC, 'IFC'),
            # NOTE: add more here
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
