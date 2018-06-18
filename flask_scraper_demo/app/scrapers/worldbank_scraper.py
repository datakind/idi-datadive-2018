from time import sleep

import pandas as pd
import requests


def scrape_world_bank(search_term):
    return WorldBankScraper().scrape(search_term)


class WorldBankScraper(object):

    DFI_NAME = 'World Bank'
    RESULTS_PER_PAGE = 500
    URL_TEMPLATE = "http://search.worldbank.org/api/v2/projects?format=json&qterm={term}&source=IBRD&rows={results}&srt=score&order=desc&kw=N&os={start}"

    def __init__(self):
        self.results = []

    def scrape(self, search_term):

        formatted_term = self._format_search_term(search_term)
        url = self.URL_TEMPLATE.format(term=formatted_term, results=self.RESULTS_PER_PAGE, start=0)

        print('Scraping Results')
        data = requests.get(url).json()
        total_pages = self._get_total_pages(data)
        current_page = 0
        while current_page + 1 <= total_pages:
            current_page += 1
            print('\nProcessing Page: %s' % current_page, '\n')
            projects = self._get_projects_on_page(data)
            self.results.extend(projects)
            next_url = self.URL_TEMPLATE.format(term=formatted_term, results=self.RESULTS_PER_PAGE, start=self.RESULTS_PER_PAGE * current_page)
            data = requests.get(next_url).json()
        df = self._build_dataframe()
        print('Completed Search for', search_term, '\n')
        return df

    def _get_total_pages(self, data):
        return (int(data['total']) / self.RESULTS_PER_PAGE) + 1

    def _get_projects_on_page(self, data):
        projects_on_page = []
        projects = data['projects']
        for project_id in projects.keys():
            project_data = projects[project_id]
            project_name = project_data['project_name']
            url = project_data['url']
            projects_on_page.append([project_name, url])
        return projects_on_page

    def _build_dataframe(self):
        df = pd.DataFrame(self.results, columns=['Project Name', 'URL'])
        # TODO: extract project status
        df['Status'] = None
        df['DFI'] = self.DFI_NAME
        return df

    @staticmethod
    def _format_search_term(search_term):
        """Replace spaces in search term with '+'."""

        return search_term.replace(' ', '+')
