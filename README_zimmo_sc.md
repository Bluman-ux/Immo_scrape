# Zimmo Scraper

The Zimmo Scraper is a Python script for scraping real estate data from the Zimmo website. It automates the process of collecting property listings and their details, such as price, address, type, and more, in a specified city.


## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Configuration](#configuration)

## Overview

The Zimmo Scraper is a web scraping tool that allows you to gather real estate data from the Zimmo website efficiently. It extracts property details from listings, including price, address, type, and more, and stores them in a structured format for further analysis.

[zimmo_sc.py] The Zimmo Scraper is a Python script that utilizes Selenium for web scraping to collect real estate data such as prices, addresses, and other details from the Zimmo website. The scraped data is then stored in CSV files for further analysis.

[proxy_scraper.py] is a file for yet not implemented proxy switching

[database.py] creates a database from the full list of scraped items and checks for duplicates. If there is a difference in duplicants, notes it and keeps both. Otherwise deletes one of the duplicants.

## Prerequisites

Before using this scraper, ensure you have the following prerequisites installed:

- Python (3.6 or higher)
- Selenium
- BeautifulSoup4
- Pandas
- NumPy
- ChromeDriver
- Fake-Useragent


## Usage

** Open the zimmo_scraper.py script in your preferred Python IDE, such as Visual Studio.

** Modify the script to customize the following parameters:

*** city_name: Set the city name for which you want to scrape real estate data.
*** max_workers: Adjust the number of worker threads for concurrent data extraction.
Configure other settings as needed.
Save your changes.

** Run the script to start scraping. It will collect property data for the specified city from the Zimmo website.

** The script will create CSV files containing the scraped data, including a file for each city and a consolidated file with all data.