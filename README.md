# IDI Scraper App

See the [Project Brief](https://docs.google.com/document/d/1sGneio4rzMvcZA9WSEO908Mce53GeSwuOvBeaRbV0rA/edit#heading=h.hs0b4pt5bzef) for more detailed information on background, goals, etc.

# App Best Practices
1. We suggest running the app with fewer than 20 search terms at a time, especially if you are running it against `ALL` of the DFI's. It can take a while for the app to scrape the data and when you run a large number of search terms at a time there is the possiblity that the app will time out or a user might accidentely close window its running in etc. 
2. Don't close the browser tab while the app is running, if you do you will have to navigate back to the original url and restart the run.
3. Don't try to run more than one instance of the app on a single machine at  the same time. In other words,  you can only have one tab running the app at a time. 

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
5. Run the app (container): `docker run -d -p 5000:5000 mikdowd/idi:latest`
    * To get updates, first run `docker pull mikdowd/idi:latest`
    * To stop the service, get the *CONTAINER ID* by running: `docker ps`. Then stop it with `docker kill the_id`
6. Navigate to http://localhost:5000/


If needed, it can be run without Docker, by installing ChromeDriver and running the app with Python.

------------------------------------

# Running the app (using Docker on DigitalOcean)

Above we outline how to run the app on a local computer. An alternative way to run the app is on the cloud. This is an easier solution though there is a recurring cost assocaited with it. Using DigitalOcean droplets costs about $5 per month per droplet. The benefit of this approach is that the setup is easier, and you can create as many instances of the app as you want. 

## Initial Setup
1. **Create Digital Ocean Account**: Go to [https://www.digitalocean.com/](https://www.digitalocean.com/) and create a new account. You will need to add a credit card number. You can use this Promo code to get $10 credit (most likely): CodeAnywhere10.
2. **Login**: Login to [https://www.digitalocean.com/](https://www.digitalocean.com/), on the upper right of the screen there should be a button that says `CREATE`, click this and then select `Droplets`
3. **Create a Droplet**: Then under where it says `Choose an image ` select `One-click apps` and then `Docker ##.##.#~.......` (there will be many numbers after the docker part but only one starts with docker. ) Then scroll down to where it says `Choose a size` and select the cheapest isntance (Under the price column you can see the price per month and hour.) Then scroll down to `Choose a datacenter region` and select the region that is closest to the person that will be using this app. Finally, under `Finalize and create` you can create a unique name for this instance like - 'IDI-Scraper-Dustin', then click `CREATE` (the one on the bottom of the page not on the upper right). You will then be redirected to another page where you can see the progress of your droplet being created. Wait for it to complete, and wait to recieve an email from DigitalOcean with the credentials needed to log into the droplet. 

## Launching the App 
1. **Launch the Droplet**: Once created you can click on the droplet which will take you to a summary screen for the droplet. On the upper right there is a button that says `Console` click this - a new window will launch. 
2. **Sign into the Droplet**: On the new window login with the credentials provided in the email. You will be required to change the password the first time you use the droplet so make sure to have a new password ready. Enter the username (probably `root`) and the password.
3. **Start the App**: You will see something like `root@IDI-Scraper-Dustin:~#` type `docker pull mikdowd/idi:latest` (only need to do this if it is first time you are setting up droplet or if the app has changed.), then type `docker run -it -p 5000:5000 mikdowd/idi:latest` and hit enter. 
4. **Navigate to App**: In the same window you executed these commands copy the Public IP Address listed in the lower left. The app web address is `http://<PUBLIC IP ADRESS>:5000` for example: `http://142.93.203.253:5000/` put the IP address where its says public IP and paste this into a web browser. 
5. **Go to the App**: App should now be running on the internet. You can upload search terms and download the results. 

## Shutting Down/Resetting the App
1. Once you are done running the app, or if you need to reset it, you can go back the DigitalOcean website and click your droplet, on the upper right there is an On/Off button. Click it to turn off. 


--------------------------------
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
