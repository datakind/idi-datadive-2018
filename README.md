# IDI Scraper App

See the [Project Brief](https://docs.google.com/document/d/1sGneio4rzMvcZA9WSEO908Mce53GeSwuOvBeaRbV0rA/edit#heading=h.hs0b4pt5bzef) for more detailed information on background, goals, etc.

# Running the app (using Docker)

This is the intended way for users to run the app. There is some setup, but should be less error-prone than having every user install all of the dependencies separately.

To run the app using Docker:
1. Download Docker
    * [Mac Download](https://download.docker.com/mac/stable/Docker.dmg)
    * [Windows Download](https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe)
    * [Other systems](https://www.docker.com/community-edition#/download) *(may need to create an account to get download links)*
2. Follow the installation instructions ([Docker Install Docs](https://docs.docker.com/install/))
3. Open Docker (double-click the icon after it's installed)
4. Open your Terminal
5. Run the app (container): `docker run -d -p 5000:5000 jimjshields/idi:latest`
    * To get updates, first run `docker pull jimjshields/idi:latest`
    * To stop the service, get the *CONTAINER ID* by running: `docker ps`. Then stop it with `docker kill the_id`
6. Navigate to http://localhost:5000/

If needed, it can be run without Docker, by installing ChromeDriver and running the app with Python.

# Developer Notes

This section is for a developer who needs to dive into the codebase for the first time, likely because one of the scrapers has failed.

## Prerequisites

* Python 3 (https://www.python.org/downloads/)
* Optional, but recommended: Virtualenv (https://virtualenv.pypa.io/en/stable/) / virtualenvwrapper (https://virtualenvwrapper.readthedocs.io/en/latest/)

## Code Guide

The scrapers use a combination of pandas, requests, beautifulsoup and selenium.

Selenium relies on ChromeDriver — a program that allows you to run Chrome in your code — and it is set to run "headless", which means it will not open the actual browser.

**Navigating the code**

In the root folder:

* `Dockerfile`: contains all of the commands to build the Docker image for this project.
    * [More info on Dockerfiles.](https://docs.docker.com/engine/reference/builder/)

The `flask_scraper_demo/` folder contains all of the relevant code to run the app.

The main files of note in the `flask_scraper_demo` folder are:

* `app/routes.py` - The backbone of the app. It contains all of the URLs the app can access, and the code that runs upon accessing the URLs. The most significant thing it does is call `execute_search` (below), which runs the scrapers given the search terms, when the `/run` URL is accessed.
* `app/scrapers/execute_search.py` - This file is responsible for sequentially calling all of the scrapers, concatenating the results into one DataFrame, and returning that DataFrame.
* `app/scrapers/[xyz]_scraper.py` - these are the scraper scripts for the individual DFIs. If something is broken, it's most likely one of these that needs to be updated.
* `app/scrapers/helpers.py` - various common functions for the Selenium scrapers.
* `app/table_builder.py` - class to assist with pandas formatting.

The `scrapers/` folder served as a test bed for development of individual scrapers.
This folder can be safely ignored.

## Making changes to the code

Pre-req: You have a Docker account, and Docker is installed and running (see above)

1. If possible, merge the changes to the `master` branch of this repository (so we have them saved for the future)
2. Build the docker container: `docker build -t {username}/idi:latest .`
3. Try running the container to make sure it works: `docker run -it -p 5000:5000 {username}/idi:latest` *(use `-it` here to be able to see the output of the flask app to debug)*
4. Navigate to http://localhost:5000/ and make sure your changes are incorporated!
5. Once you confirm that it works, push the container to you account: `docker push {username}/idi:latest`
    * This will be uploaded to a docker hub account - similar to GitHub - so you will not need to build on every computer

# Pre-Datadive Notes

## Proposed Methodology
At the DataDive, data scientists will work to develop a simple scraper tool that take as an input “search terms” and provide the links to projects that resulted when those terms were searched.
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
