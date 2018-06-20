"""
Helper script to test an individual scraper.
"""


import pandas as pd

# NOTE: replace with your scraper
# from ifc_scraper import scrape_ifc
from worldbank_scraper import scrape_world_bank


DF_HEAD_LENGTH = 20  # number of records to print per dataframe
SCRAPER = scrape_world_bank  # NOTE: replace with your scraper
# SCRAPER = scrape_ifc
TEST_SEARCH_TERMS = [  # NOTE: replace if these yield no results for your DFI
    'BNP Paribas',
    "NULL SHOULDN'T RETURN ANY ROWS qwertyuiop",
    'Bank of China',
]


def search(search_term):
    """
    test that the scraper works and returns results in the right format
    output columns: 'Project Name', 'URL', 'Status', 'DFI', 'Search Term'
    """
    df = pd.DataFrame([], columns=['Project Name', 'URL', 'Status', 'DFI'])
    print("\033[1m", "#" * 30, "\033[0m")
    print('Searching for Term:', search_term)

    df = SCRAPER(search_term)

    assert list(df.columns) == ['Project Name', 'URL', 'Status', 'DFI'], \
        "Columns must be: ['Project Name', 'URL', 'Status', 'DFI']"
    print('Data looks like:')
    print(df.head(DF_HEAD_LENGTH))
    print()

    df['Search Term'] = search_term
    return df


if __name__ == '__main__':
    df = pd.DataFrame([], columns=['Project Name', 'URL', 'Status', 'DFI', 'Search Term'])

    for search_term in TEST_SEARCH_TERMS:
        df = df.append(search(search_term))

    df.to_csv('test.csv', index=False)
    print('No obvious errors found. Please inspect the file test.csv for any surprises.')
