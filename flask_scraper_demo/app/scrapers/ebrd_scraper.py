import requests
import urllib.parse
import pandas as pd
from parsel import Selector


def scrape_ebrd(search_term):
    return EbrdScraper().scrape(search_term)


class EbrdScraper(object):

    DFI_NAME = 'ebrd'
    URL_TEMPLATE = "https://www.ebrd.com/work-with-us/project-finance/project-summary-documents.html?keywordSearch={term}"  # noqa

    def scrape(self, search_term):
        results = []

        formatted_term = urllib.parse.quote_plus(search_term)
        page_urls = [self.URL_TEMPLATE.format(term=formatted_term)]
        print('Scraping Results')
        page_counter = 1
        while len(page_urls) > 0:
            print('\nProcessing Page: {pg}\n'.format(pg=page_counter))
            url = page_urls.pop()
            source_raw = requests.get(url, verify=False)

            source = Selector(text=source_raw.text)

            results.extend(self._get_projects_on_page(source))
            # Find the next page url
            if page_counter == 1:
                # Only get this list on the first page load
                for page_link in source.css('div.saf-paging a'):
                    page_urls.append("https://www.ebrd.com" + page_link.xpath('@href').extract_first())
            page_counter += 1

        print('Completed Search for', search_term, '\n')

        df = self._build_dataframe(results)
        return df

    @staticmethod
    def _get_projects_on_page(data):
        """Build project data"""

        projects_on_page = []
        projects = data.css('#posts tr')
        for project in projects:
            project_name = project.css('a').xpath('string()').extract_first()
            link = project.css('a').xpath('@href').extract_first()
            if link.startswith('//'):
                link = 'https:' + link
            status = project.css('td').xpath('string()').extract()[-1]
            projects_on_page.append([project_name, link, status])

        return projects_on_page

    def _build_dataframe(self, results):
        df = pd.DataFrame(results, columns=['Project Name', 'URL', 'Status'])
        df['DFI'] = self.DFI_NAME
        return df
