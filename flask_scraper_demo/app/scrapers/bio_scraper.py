import pandas as pd
import urllib.parse 
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
            
MAIN_URL= "http://www.bio-invest.be/index.php?option=com_portfolio&view=map&filter=&filterType=&filterInstrument=&filterContinent=&sort=p.title&sortDir=DESC&limit=0&limitstart=0&Itemid=30"
ROOT_URL = "http://www.bio-invest.be"

def scrape_bio(search_term):
    return BIOScraper().scrape(search_term)
    
def delist_values(d):
    '''
    Turns list from urllib.parse.qsl() to a single entry e.g. ['ABC'] -> 'ABC'
    '''
    for k,v in d.items():
        d[k] = v[0]
    return d

def parse_xml(term, term_url):
    '''
    BIO Query URLs return an XML with nested HTML 
    function parses XML and HTML to name and link
    '''
    def parse_nested_html(htmltxt):        
        '''
        Parses HTML for one search response
        '''
        soup = BeautifulSoup(htmltxt, 'lxml')
        links = []
        names = []
                             
        ## Get Link
        anchor_resp = soup.find_all('a')
        for _, anchor in enumerate(anchor_resp):
            links.append(anchor.attrs['href'])
        
        ## Get Name
        strong_resp = soup.find_all("strong")
        for _, anchor in enumerate(strong_resp):
            names.append(anchor.text)
        
        return names, links

    results = [] 
    
    resp = requests.get(term_url)
    try:    
        xml_string = resp.content.decode('utf-8',"ignore")
        
    except UnicodeDecodeError:
        ## Page will normally return XML, if returns an HTML (which it does sometimes)
        ## parse HTML immediately rather than using the XML to navigate to nested HTML
        htmltxt = resp.text
        names, links = parse_nested_html(htmltxt) 
        
        for name,link in zip(names, links):
            results.append({"Project Name": name, "URL": ROOT_URL + link, "Search Term": term})
        
        return results
        
    root = ET.fromstring(xml_string)
    
    ## Iterate through all responses if a valid XML is returned
    for i, nested_html in enumerate(root.findall("./marker/markerHtml")):
        htmltxt = nested_html.text
        names , links = parse_nested_html(htmltxt)
        for name,link in  zip(names,links):
            results.append({"Project Name": name, "URL": ROOT_URL + link, "Search Term": term})
        
    return results

class BIOSearchParams(object):
    
    def __init__(self, term):
        self.params = delist_values(urllib.parse.parse_qs(MAIN_URL, keep_blank_values=True))
        self.terms = dict()
        
        self.update_params(term)
        self.terms[term] = self.prepare_url(term)
        
    def update_params(self, t):
        '''
        Sets the filter field (search term) in the Params class
        '''
        self.params['filter'] = t
            
    def prepare_url(self, t):
        '''
        Given a search term function formats a URL
        '''
        query_url = """http://www.bio-invest.be/index.php?option={0}&view={1}&filter={2}&filterType={3}&filterInstrument={4}&filterContinent={5}&sort={6}&sortDir={7}&limit={8}&limitstart={9}&Itemid={10}""".format(self.params['http://www.bio-invest.be/index.php?option'],
                    self.params['view'].strip(),
                    self.params['filter'].strip().replace(" ","+"),
                    self.params['filterType'].strip(),
                    self.params['filterInstrument'].strip(),
                    self.params['filterContinent'].strip(),
                    self.params['sort'].strip(),
                    self.params['sortDir'].strip(),
                    self.params['limit'].strip(),
                    self.params['limitstart'].strip(),
                    self.params['Itemid'].strip())
                    
        return query_url
    
    
class BIOScraper(object):
    
    def __init__(self):
        self.search_term = ""
        self.params = BIOSearchParams("")

    def scrape(self, search_term):
        self.params = BIOSearchParams(search_term)
        self.results = []
        self.DFI_NAME = "BIO"
        
        for term, term_url in self.params.terms.items():
            term = term.replace('+', ' ')
            all_projects = parse_xml(term, term_url)
            self.results.extend(all_projects)
            
        return self._build_dataframe()
            
    def _build_dataframe(self):
        df = pd.DataFrame(self.results, columns=['Project Name', 'URL'])
        df['Status'] = None
        df['DFI'] = self.DFI_NAME
        return df

TEST_STR = "Africa"
ns = BIOScraper()

df = ns.scrape(TEST_STR)


df


        
        
    
    