from time import sleep

from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.keys import Keys

from .helpers import init_chrome_webdriver


def scrape_IFC(search_term):
    return IFCScraper().scrape(search_term)


class IFCScraper(object):

    DFI_NAME = 'IFC'

    def __init__(self):
        ## Build the chrome windows
        self.driver = init_chrome_webdriver(headless=True, download_dir=None)
        self.starting_url = "https://disclosures.ifc.org/#/enterpriseSearchResultsHome/*"
        self.results = []

    def scrape(self, search_term):
        # Wait for it
        sleep(2)

        ## Grab the Url
        self.driver.get(self.starting_url)
        print('Initializing Website')
        sleep(3)  ## Wait for it

        self._search(search_term)

        ## Now Collect the Links

        soup = BeautifulSoup(self.driver.page_source)
        current_page = 0
        total_pages = self._get_total_pages(soup)

        print('Scraping Results')
        while current_page + 1 <= total_pages:
            current_page += 1
            soup = BeautifulSoup(self.driver.page_source)

            print('\nProcessing Page: %s' % current_page, '\n')
            projects_on_page = self._get_projects_on_page(soup)
            self.results.extend(projects_on_page)
            if current_page < total_pages:
                self._click_next_button()

        df = self._build_dataframe()

        self.driver.quit()
        print('Completed Search for', search_term, '\n')
        return df

    def _search(self, search_term):
        ## Execute the Search
        inputElement = self.driver.find_element_by_id("searchBox")
        inputElement.clear()  ## Clear it just in case
        inputElement.send_keys('"{}"'.format(search_term))
        inputElement.send_keys(Keys.ENTER)
        print('searching for term')
        sleep(3)

    def _get_total_pages(self, soup):
        pagenum = soup.find(text=" Page")
        total_pages = int([i for i in pagenum.parent.nextSiblingGenerator()][3].text)
        print('Total Pages', total_pages)
        return total_pages

    def _get_projects_on_page(self, soup):
        projects_on_page = []
        for i in soup.find_all('div', {"class": "projects"}):
            try:
                selected = i.find('a', {'class': 'search-head'})
                url = selected['href']
                label = selected.text
                projects_on_page.append([label, url])
            except TypeError:
                continue
        return projects_on_page

    def _click_next_button(self):
        sleep(2)
        nextButton = self.driver.find_element_by_class_name('next')
        print(nextButton)
        nextButton.click()
        sleep(2)

    def _build_dataframe(self):
        df = pd.DataFrame(self.results, columns=['Project Name', 'URL'])
        # TODO: extract project status
        df['Status'] = None
        df['DFI'] = self.DFI_NAME
        return df
