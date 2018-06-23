import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def scrape_opic(search_term):
    return OpicScraper().scrape(search_term)

class OpicScraper(object):

    def __init__(self):
        pass

    def scrape(self, search_term):

        projectName = None
        projectURL = None
        projectStatus = None
        NameList = []
        urlList = []

        browser = webdriver.Chrome("/usr/local/bin/chromedriver")
        url = "https://www3.opic.gov/OPICProjects"
        browser.get(url)
        time.sleep(1 + np.random.randint(2,4))

        searchTerm = browser.find_element_by_xpath('//*[@id="grid1_table_headers"]/thead/tr[2]/td[5]/span/input')
        searchTerm.send_keys(search_term)
        time.sleep(1 + np.random.randint(2,5))
        table = browser.find_element_by_xpath('//*[@id="grid1_table"]')

        for row in table.find_elements_by_xpath(".//tbody/tr"):
            if [td.get_attribute("href") for td in row.find_elements_by_xpath(".//td[5]/a")] == []:
                projectURL = None
            else:
                projectURL = [td.get_attribute("href") for td in row.find_elements_by_xpath(".//td[5]/a")][0]
            projectName = [td.text for td in row.find_elements_by_xpath(".//td[text()]")][-2]
            projectName = projectName.split('\n')[0]
            NameList.append(projectName)
            urlList.append(projectURL)

        while True:
            if search_term == "":
                break
            try:
                browser.find_element_by_xpath('//*[@id="grid1_table_pager"]/div/div[3]/a')
                browser.find_element_by_xpath('//*[@id="grid1_table_pager"]/div/div[3]').click()
                time.sleep(1 + np.random.randint(2,4))
                table = browser.find_element_by_xpath('//*[@id="grid1_table"]')

                for row in table.find_elements_by_xpath(".//tbody/tr"):
                    if [td.get_attribute("href") for td in row.find_elements_by_xpath(".//td[5]/a")] == []:
                        projectURL = None
                    else:
                        projectURL = [td.get_attribute("href") for td in row.find_elements_by_xpath(".//td[5]/a")][0]
                    projectName = [td.text for td in row.find_elements_by_xpath(".//td[text()]")][-2]
                    projectName = projectName.split('\n')[0]
                    NameList.append(projectName)
                    urlList.append(projectURL)
            except NoSuchElementException:
                break


        res = {'Project Name': NameList,
               'URL': urlList}
        df = pd.DataFrame.from_dict(res)
        df['DFI'] = 'Overseas Private Investment Corporation (OPIC)'
        df['Status'] = 'Active'
        df = df[['Project Name', 'URL', 'Status', 'DFI']]
        return df
