# idi-datadive-scoping

IDI scoping repo - see  [Project Brief](https://docs.google.com/document/d/1sGneio4rzMvcZA9WSEO908Mce53GeSwuOvBeaRbV0rA/edit#heading=h.hs0b4pt5bzef) for more detailed information on background, goals, etc. 


## Proposed Methodology
At the DataDive - data scientists will work to develop a simple scraper tool that take as an input “search terms” and provide the links to projects that resulted when those terms were searched. 
This tool will be comprised of numerous subtools that search specific DFI websites. At the DataDive we will prioritize the creation of scrapers based on IDI’s prioritization. Scrapers will be written in Python likely using some combination of Selenium, Beautifulsoup, requests, etc. 

## General Requirements
* Tool(s) take a csv/excel list of search terms as input
* Tool(s) return a csv/excel file with a list of links that were found for a specific search term, each row should include (where available)
* Project Name
* Search Term Used
* DFI Site scrape extracted from (what bank is being scraped)
* Tool(s) are easy to execute and have straightforward instructions for use.
* Tool(s) cover high priority DFI sites
* All scrapers return data in an identical format - meaning the output has the same columns and meanings as all other scrapers. If some data is only available for a subset of DFIs then that column will be present but empty for the DFIs that do not have that information. 
* Tool(s) deduplicate projects by specific DFI site, tool should not deduplicate across DFI sites.

## Getting Started

The demo Flask app & scrapers are found in `/flask_scraper_demo`.

1. Clone the repository (Click "Clone or download"; click the copy button; `git clone {copied text}`)
2. Setup a virtual environment: `mkvirtualenv idi-datadive-scoping`
3. Navigate to `./flask_scraper_demo`
4. `make setup` to install the requirements
5. `make run` to run the app
6. Navigate to http://localhost:5000/ to make sure the app works
7. On the app, choose the `Search_Terms.txt` file & click "Submit"
8. It should show 2 search terms: click "Run Scraper"
9. Make sure the status of the scrapers is printed to your terminal
10. Make sure the table displays on the web page at the end of the run

This *proof of concept* app takes as input a csv file of search terms and searches the [IFC](https://disclosures.ifc.org/#/enterpriseSearchResultsHome/*) site. It only works for this site currently. If you want to run it there is a demo search terms file located at `flask_scraper_demo/Search_Terms.txt`. 

**Landing Page**
![Landing Page](img/p1.png)
__________________________

**Load Search Terms**
![Search Terms Page](img/p2.png)
__________________________
**Results Page**
![Results Page](img/p3.png)



**Notes**
Code for the scraper is in ifc_scraper.py. This demo does have a grouping function in the ifc_scraper.py code, so it removes obvious duplicates and returns a single row for a project but shows which search terms were associated with a given project. 

### 