import pandas as pd
import json
import requests
import urllib.request

def scrape_kfw_api(search_term):
    return KFWAPIScraper().scrape(search_term)


class KFWAPIScraper(object):

    DFI_NAME = 'KFW API'

    def __init__(self):
        pass

    def scrape(self, search_term):
        res = []

        # Loading all projects from JSON file
        with urllib.request.urlopen('https://www.kfw-entwicklungsbank.de/ipfz/Projektdatenbank/download/json') as url:
            data = json.loads(url.read().decode())

        for n_proj in range(0, len(data)):
            if data[n_proj].get('description'):
                if search_term.lower().replace(" ", "") in data[n_proj]['title'].lower().replace(" ", ""):
                    res.append(self._match_search_term(data, search_term, n_proj))
            if data[n_proj].get('description'):
                if search_term.lower().replace(" ", "") in data[n_proj]['description'].lower().replace(" ", ""):
                    res.append(self._match_search_term(data, search_term, n_proj))
            if data[n_proj].get('projekttraegers'):
                if search_term.lower().replace(" ", "") in data[n_proj]['projekttraegers'][0].lower().replace(" ", ""):
                    res.append(self._match_search_term(data, search_term, n_proj))

        df = self._build_dataframe(res)

        return df

    def _match_search_term(self, data, search_term, n_proj):
        url = "https://www.kfw-entwicklungsbank.de/ipfz/Projektdatenbank/" \
                  + data[n_proj]['title'].replace(" ", "-")  \
                  + "-" + str(data[n_proj]['projnr']) + ".htm"

        r = [data[n_proj]['title'], url, data[n_proj]['status'], "KfW"]
        return r

    def _build_dataframe(self, results):
        df = pd.DataFrame(results, columns=['Project Name', 'URL', "Status", "DFI"])
        return df
