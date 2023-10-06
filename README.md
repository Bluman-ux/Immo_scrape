## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Dependencies](#dependencies)

## Introduction

[zimmo_sc.py] The Zimmo Scraper is a Python script that utilizes Selenium for web scraping to collect real estate data such as prices, addresses, and other details from the Zimmo website. The scraped data is then stored in CSV files for further analysis.

[proxy_scraper.py] is a file for yet not implemented proxy switching

[database.py] creates a database from the full list of scraped items and checks for duplicates. If there is a difference in duplicants, notes it and keeps both. Otherwise deletes one of the duplicants.


## Features

- **City Selection:** Specify the city for which you want to scrape real estate data.
- **Pagination Handling:** The script handles pagination to retrieve data from multiple pages.
- **Data Cleaning:** The scraped data is processed and cleaned for better readability.
- **Parallel Processing:** Concurrent execution for imporved performance using 'concurent.futures'
- **Elapsed Time Logging:** The elapsed time is logged at various points to monitor script performance.

## Prerequisites

- Python 3.x
- ChromeDriver (download and install from [here](https://sites.google.com/chromium.org/driver/))
  
## Dependencies
- Selenium
- Beautiful Soup
- Pandas
- NumPy
- Fake UserAgent
- SQLite3
- Concurrent.futures
