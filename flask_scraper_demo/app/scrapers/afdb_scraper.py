import pdb
from time import sleep

from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.keys import Keys

from .helpers import init_chrome_webdriver

def scrape_afdb(search_term):
    return AfricanDevelopmentBankScraper().scrape(search_term)

class AfricanDevelopmentBankScraper(object):

    DFI_NAME = 'African Development Bank'
    STARTING_URL = 'https://www.afdb.org/en/projects-and-operations/project-portfolio//'
    BASE_URL = 'https://www.afdb.org'

    def __init__(self):

        # Build the chrome window
        self.driver = init_chrome_webdriver(headless=True, download_dir=None)

    def scrape(self, search_term):

        self.search_term = search_term

        results = []

        # Wait for it
        sleep(2)

        # Grab the Url
        self.driver.get(self.STARTING_URL)
        print('Initializing Website')
        sleep(3)  ## Wait for it

        self._search(search_term)

        # Now Collect the Links
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        current_page = 0
        total_pages = self._get_total_pages(soup)

        print('Scraping Results')
        while current_page + 1 <= total_pages:
            current_page += 1
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            print('\nProcessing Page: %s' % current_page, '\n')
            projects_on_page = self._get_projects_on_page(soup)
            results.extend(projects_on_page)

            if current_page < total_pages:
                try:
                    self._click_next_button()
                except:
                    'Next page did not load.'

        df = self._build_dataframe(results)

        self.driver.quit()
        print('Completed Search for', search_term, '\n')

        return df

    def _build_dataframe(self, results):
        df = pd.DataFrame(results, columns=['Project Name', 'URL', 'Status'])
        df['DFI'] = self.DFI_NAME
        return df

    def _search(self, search_term):
        # Execute the Search
        inputElement = self.driver.find_element_by_id('tx_llcatalog_pi_filter_keywords')
        inputElement.clear()  # Clear it just in case
        inputElement.send_keys('"{}"'.format(search_term))
        inputElement.send_keys(Keys.ENTER)
        print('searching for term')
        sleep(3)

    def _get_total_pages(self, soup):
        try:
            children = soup.find('div', {'class': 'pagination'}).find('ul')
            page_nums = []
            for child in children:
                try:
                    page_num = int(child.getText())
                    page_nums.append(page_num)
                except:
                    'Not an integer.'

            total_pages = max(page_nums)
            return total_pages
        except:
            return 1

    def _get_projects_on_page(self, soup):
        projects_on_page = []

        table = soup.findChildren('table')
        if table:
            rows = table[0].findChildren(['tr'])[1:]
        else:
            return projects_on_page

        for row in rows:
            cols = row.findChildren('td')

            for col, val in enumerate(cols):
                if col == 0:
                    pass
                elif col == 1:
                    href_tag = val.findChildren('a',recursive=False)[0]
                    project_name = href_tag.getText()
                    href_url = self.BASE_URL + href_tag.get('href')
                elif col == 2:
                    val.find('span').decompose()
                    status = val.getText()

            projects_on_page.append([project_name,href_url,status])

        return projects_on_page

    def _click_next_button(self):
        sleep(2)
        next_button = self.driver.find_element_by_class_name('next')
        print(next_button)
        next_button.click()
        sleep(2)
