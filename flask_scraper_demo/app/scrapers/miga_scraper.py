import pandas as pd


def scrape_miga(search_term):
    return MigaScraper().scrape(search_term)


class MigaScraper(object):

    DFI_NAME = 'MIGA'

    def __init__(self):
        pass

    def scrape(self, search_term):

        # Store project data here
        results = []

        # Implement scraping logic here

        df = self._build_dataframe(results)
        print('Completed Search for', search_term, '\n')
        return df

    def _build_dataframe(self, results):
        df = pd.DataFrame(results, columns=['Project Name', 'URL'])
        # TODO: extract project status
        df['Status'] = None
        df['DFI'] = self.DFI_NAME
        return df
