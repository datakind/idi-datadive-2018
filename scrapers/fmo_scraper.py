from time import sleep

from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.keys import Keys

from helpers import init_chrome_webdriver


def scrape_fmo(search_term):
    return FMOScraper().scrape(search_term)


class FMOScraper(object):

    DFI_NAME = 'FMO'
    #STARTING_URL = "https://disclosures.ifc.org/#/enterpriseSearchResultsHome/*"
    STARTING_URL = "https://www.fmo.nl/worldmap/"

    def __init__(self):

        # Build the chrome window
        self.driver = init_chrome_webdriver(headless=True, download_dir=None)

    def scrape(self, search_term):
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
                self._click_next_button()

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
        inputElement = self.driver.find_element_by_id("f-search")
        inputElement.clear()  # Clear it just in case
        inputElement.send_keys('"{}"'.format(search_term))
        inputElement.send_keys(Keys.ENTER)
        print('searching for term')
        sleep(3)

    def _get_total_pages(self, soup):
        #page_num = soup.find(text=" Page")
        #total_pages = int([i for i in page_num.parent.nextSiblingGenerator()][3].text)
        #print('Total Pages', total_pages)
        #return total_pages
        return 1

    def _get_projects_on_page(self, soup):
        projects_on_page = []

        for i in soup.find_all("li", {"class": "ProjectList__item"}):
            try:
                selected = i

                if (selected.h3):
                    label = selected.h3.text
                else:
                    continue

                if (selected.a):
                    url = selected.a.get('href')
                else:
                    continue

                '''
                Use default status = '' to indicate problems with getting information from website if
                below way to extract status does not work properly any more due to changes of website
                '''
                status = ""

                '''
                The FMO website shows 4 span entries for 'Approved' projects and an additional
                5th span entry with 'Proposed investment' for prxsoposed investments.

                The different spans are:
                0 (title) : Total FMO financing
                1 : date
                2 : country
                3: sector
                4: proposed (only exists if proposed investment)
                '''
                spans = selected.span.find_all('span', recursive=False)

                if ( len(spans) == 4 ):
                    status = "Approved"

                if ( len(spans) == 5 ):
                    status = spans[4].text

                # append project
                projects_on_page.append([label, url, status])
            except TypeError:
                continue
        return projects_on_page

    def _click_next_button(self):
        sleep(2)
        next_button = self.driver.find_element_by_class_name('next')
        print(next_button)
        next_button.click()
        sleep(2)
