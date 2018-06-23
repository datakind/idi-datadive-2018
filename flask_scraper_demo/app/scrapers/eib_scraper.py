import pandas as pd
from parsel import Selector
from helpers import init_chrome_webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


def scrape_eib(search_term):
    return Eib().scrape(search_term)


class Eib():

    DFI_NAME = 'EIB'
    STARTING_URL = "http://www.eib.org/projects/loan/list/index.htm?from=2008&region=&sector=&to=2018&country"

    def __init__(self):
        self.driver = init_chrome_webdriver(headless=True, download_dir=None)

    def scrape(self, search_term):
        self.search_term = search_term

        self.driver.get(self.STARTING_URL)
        # Search the term
        inputElement = self.driver.find_element_by_css_selector("div.dataTables_filter input")
        inputElement.send_keys(self.search_term)
        inputElement.send_keys(Keys.ENTER)

        # Now show all
        myselect = Select(self.driver.find_element_by_css_selector("div.dataTables_length select"))
        myselect.select_by_value("-1")

        source = Selector(text=self.driver.page_source)

        return self._extract_data(source)

    def _build_dataframe(self, results):
        df = pd.DataFrame(results, columns=['Project Name', 'URL'])
        df['Status'] = None
        df['DFI'] = self.DFI_NAME
        return df

    def _extract_data(self, source):
        results = []
        for result in source.css('table.datatable tbody tr'):
            field = []
            link = None

            total_tds = result.css('td')
            if len(total_tds) == 1:
                # No results were found
                break

            for idx, col in enumerate(total_tds):
                field_value = col.xpath('string()').extract_first()
                field.append(field_value)
                if idx == 0:
                    # Get the link from the first col
                    link = col.css('a').xpath('@href').extract_first()
                    if link is not None:
                        link = "http://www.eib.org" + link
                break  # Only need the first one

            # Convert the list to a usable dict
            results.append([field[0], link])

        return self._build_dataframe(results)
