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

        '''
        We encountered troubles with the search using the chrome driver: The resulting html page 
        (and soup object created for it) would only include a subset of the projects that should be
        returned for a given search term. Embedding the search terms in the url and using
        'requests.get()' yields html that, if passed to soup, gives the complete list. =

        The boolean 'debug_search' switches between these two options to get the search results:

        debug_search = False -> use driver based search (this should be the default, but returns only subset of search results)
        debug_search = True -> use url based search
        '''
        debug_search = True

        if ( debug_search ):
            import requests

            first_url = 'https://www.fmo.nl/worldmap?search='
            search_term = 'Standard Bank'
            end_url = '&region=&year=&projects=allProjects'
            page_num = 1
            page = '&page={}'.format(page_num)

            clean_search_term = search_term.lower().strip().replace(' ','+')
            clean_search_term

            new_url = first_url + clean_search_term + end_url + page
            page = requests.get(new_url)

            soup = BeautifulSoup(page.content, 'html.parser')
        else:
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

            if ( debug_search ):
                soup = BeautifulSoup(page.content, 'html.parser')
            else:
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
        df = pd.DataFrame(results, columns=['Project Name', 'URL'])
        # TODO: extract project status
        df['Status'] = None
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

        #for i in  soup.find_all('div', {"class": "projects"}):
        print ("Items found: " , len(soup.find_all("li", {"class": "ProjectList__item"}) ) )

        for i in soup.find_all("li", {"class": "ProjectList__item"}):
            try:
                selected = i
                url = selected.a.get('href') #['href']
                label = selected.h3.text
                print("LABEL:", label)
                projects_on_page.append([label, url])
            except TypeError:
                continue
        return projects_on_page

    def _click_next_button(self):
        sleep(2)
        next_button = self.driver.find_element_by_class_name('next')
        print(next_button)
        next_button.click()
        sleep(2)
