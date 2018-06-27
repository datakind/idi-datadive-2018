from parsel import Selector
from helpers import init_chrome_webdriver
import pandas as pd


def scrape_miga(search_term):
    return MigaScraper().scrape(search_term)


class MigaScraper(object):

    DFI_NAME = 'MIGA'
    STARTING_URL = "https://www.miga.org/Pages/Projects/SearchResults.aspx?projname={0}&dispset=9000"

    def __init__(self):
        self.driver = init_chrome_webdriver(headless=True, download_dir=None)

    def scrape(self, search_term):
        # starting url attempts to avoid pagination
        self.driver.get(self.STARTING_URL.format(search_term))
        # need html to get iframe
        source = Selector(text=self.driver.page_source)
        # parse iframe
        iphrame = source.css('iframe').xpath("@src").extract_first()
        # get iframe page
        self.driver.get(iphrame)
        source = Selector(text=self.driver.page_source)
        # call extraction on full page
        df = self._extract_data(source)
        df['DFI'] = self.DFI_NAME
        print('Completed Search for', search_term, '\n')
        if df.shape[0] > 0:
            df = df[['Project Name', 'URL', 'Status', 'DFI']]
            return df
        else:
            return pd.DataFrame(columns=['Project Name', 'URL', 'Status', 'DFI'])

    def _extract_data(self, source):
        data = []
        results = source.css('ul.search-results-list li')
        for item in results:
            item_data = {}
            if item.css('h3 a').xpath('string()').extract_first():
                item_data['Project Name'] = item.css('h3 a').xpath('string()').extract_first().strip()
            # finish url
            if item.css('h3 a').extract_first():
                item_data['URL'] = str('https://www.miga.org/pages/projects/project.aspx?pid=' +
                                       item.css('h3 a').extract_first().split('pid=')[1].split("'")[0])
            for sub_item in item.css('dl'):
                if sub_item.css('dt').xpath('string()').extract_first() == "Project Status: ":
                    item_data['Status'] = sub_item.css('dd').xpath('string()').extract_first()
                else:
                    continue
            if len(item_data.keys()) > 1:
                data.append(item_data)
        return pd.DataFrame(data)
