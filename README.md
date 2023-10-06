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
- [̶P̶a̶r̶a̶l̶l̶e̶l̶ ̶P̶r̶o̶c̶e̶s̶s̶i̶n̶g̶:̶ ̶C̶o̶n̶c̶u̶r̶r̶e̶n̶t̶ ̶e̶x̶e̶c̶u̶t̶i̶o̶n̶ ̶f̶o̶r̶ ̶i̶m̶p̶r̶o̶v̶e̶d̶ ̶p̶e̶r̶f̶o̶r̶m̶a̶n̶c̶e̶ ̶u̶s̶i̶n̶g̶ ̶`̶c̶o̶n̶c̶u̶r̶r̶e̶n̶t̶.̶f̶u̶t̶u̶r̶e̶s̶`̶]̶ ̶
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
