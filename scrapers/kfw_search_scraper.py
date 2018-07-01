import requests
import urllib.parse
import pandas as pd
from parsel import Selector


def scrape_kfw_search(search_term):
    return KFWSearchScraper().scrape(search_term)


class KFWSearchScraper(object):

    DFI_NAME = 'KFW Search'
    URL_TEMPLATE = "https://www.kfw-entwicklungsbank.de/Internationale-Finanzierung/KfW-Entwicklungsbank/Projekte/Projektdatenbank/ipfz/do.haupia?query={term}&page=1&rows=100000&sortBy=relevance&sortOrder=desc&facet.filter.language=de&dymFailover=true"  # noqa

    def scrape(self, search_term):
        results = []

        formatted_term = urllib.parse.quote_plus(search_term)
        url = self.URL_TEMPLATE.format(term=formatted_term)
        print('Scraping Results')

        source = requests.get(url, verify=False).json()
        results.extend(self._get_projects_on_page(source))

        print('Completed Search for', search_term, '\n')

        df = self._build_dataframe(results)
        return df

    @staticmethod
    def _get_projects_on_page(data):
        """Build project data"""

        projects_on_page = []
        projects = data.get('proxyDidYouMean', {}).get('response', {}).get('response', {}).get('docs', [])
        if projects == []:
            # Try a diferent key set
            projects = data.get('response', {}).get('docs', [])

        for project in projects:
            project_name = project.get('title')[0]
            link = project.get('link')
            if link is not None:
                link = 'https://www.kfw-entwicklungsbank.de/ipfz/Projektdatenbank' + link
            projects_on_page.append([project_name, link])

        return projects_on_page

    def _build_dataframe(self, results):
        df = pd.DataFrame(results, columns=['Project Name', 'URL'])
        df['Status'] = None
        df['DFI'] = self.DFI_NAME
        return df
