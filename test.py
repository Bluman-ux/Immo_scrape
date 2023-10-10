import os
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import date
from pprint import pprint
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import numpy as np
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import re
import datetime
import concurrent.futures

class Scraper:
    def __init__(self, city_name):
        self.city_name = city_name
        self.urls_houses = []
        self.new_urls_houses = []

    def setup_driver(self):
        ua = UserAgent()
        user_agent = ua.random
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--disable-notifications")
        options.add_argument("--headless")
        service = Service(executable_path='C:\\Program Files (x86)\\chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def cookie_ok(self, driver):
        try:
            search_box = driver.find_element("id", "didomi-notice-agree-button")
            search_box.send_keys('ChromeDriver')
            time.sleep(4)
            search_box.click()
            search_box.submit()
        except:
            pass

    def city_input(self, driver):
        search = driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div[1]/div[1]/zimmo-search-form/div[1]/app-cities-search/div/app-places-lookup/app-places-search-box/input")
        search.send_keys(self.city_name)
        search.send_keys(Keys.RETURN)
        searchbutton = driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div[1]/div[1]/zimmo-search-form/div[1]/button")
        time.sleep(4)
        searchbutton.click()

    def extract_data_from_link(self, link):
        try:
            driver = self.setup_driver()
            driver.get(link)
            self.cookie_ok(driver)

            response = driver.page_source
            html_soup = BeautifulSoup(response, 'lxml')
            driver.close()
            details = html_soup.find('ul', class_='main-features')
            days_on = html_soup.find('div', class_='stat-text text')

            popper = link.find("?")
            to_print_link = link[:int(popper) - 1]

            try:
                split_details = list(details.stripped_strings)
                evens = [x for x in range(len(split_details)) if x & 1 == 0]
            except:
                pass

            split_details.append(to_print_link)
            try:
                days_online = str(int(days_on.text))
                split_details.append("Days: " + days_online)
            except:
                pass
            time.sleep(2)
            return split_details

        except Exception as e:
            print(f"Error processing link {link}: {e}")
            return None

    def scrape_links(self):
        driver = self.setup_driver()
        driver.get("https://www.zimmo.be/nl/")
        self.cookie_ok(driver)
        self.city_input(driver)
        time.sleep(4)
        newpage = driver.current_url
        driver.quit()

        ua = UserAgent()
        user_agent = ua.random
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--disable-notifications")
        options.add_argument("--headless")
        service = Service(executable_path='C:\\Program Files (x86)\\chromedriver.exe')

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(newpage)
        self.cookie_ok(driver)

        try:
            max_pages = driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div[4]/div[2]/div[3]/div[3]/ul/li[13]/a/span").text
            now_t = driver.find_element(By.CLASS_NAME, "pagination")
            now_page = now_t.find_element(By.CLASS_NAME, "active").text
        except:
            now_t = driver.find_element(By.CLASS_NAME, "pagination")
            now_page = now_t.find_element(By.CLASS_NAME, "active").text
            max_pageszz = driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div[4]/div[2]/div[3]/div[3]/ul").text
            number = int(max_pageszz[-1]) + 1
            max_pages = driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div[4]/div[2]/div[3]/div[3]/ul/li[" + str(number) + "]/a/span").text

        elems = driver.find_elements(By.CLASS_NAME, 'property-item_link')
        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None:
                self.urls_houses.append({"Url: ": href, "Date: ": today})
                self.new_urls_houses.append(href)

        next_t = driver.find_element(By.CLASS_NAME, "last")
        next_t2 = next_t.find_element(By.XPATH, ".//a")
        next_t2.click()
        time.sleep(4)
        newpage = driver.current_url
        driver.quit()

        text = newpage
        head = text.partition('=')
        basic = head[0] + "=" + head[2].partition('=')[0] + "="

        n = 0
        for x in range(2, int(max_pages) + 1):
            n = + x
            new_page = basic + str(x)
            options = webdriver.ChromeOptions()
            ua = UserAgent()
            user_agent = ua.random
            options.add_argument(f"user-agent={user_agent}")
            options.add_argument("--disable-notifications")
            options.add_argument("--headless")
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(new_page)
            self.cookie_ok(driver)
            now_t = driver.find_element(By.CLASS_NAME, "pagination")
            now_page = now_t.find_element(By.CLASS_NAME, "active").text
            pprint(now_page)

            if int(now_page) <= int(max_pages):
                pprint("Page - " + str(now_page) + "/" + str(max_pages))
                elems = driver.find_elements(By.CLASS_NAME, 'property-item_link')
                for elem in elems:
                    href = elem.get_attribute('href')
                    if href is not None:
                        self.urls_houses.append({"Url: ": href, "Date: ": today})
                        self.new_urls_houses.append(href)
                driver.quit()
            else:
                elems = driver.find_elements(By.CLASS_NAME, 'property-item_link')
                pprint("Page - " + str(now_page) + "/" + str(max_pages))
                for elem in elems:
                    href = elem.get_attribute('href')
                    if href is not None:
                        self.urls_houses.append({"Url: ": href, "Date: ": today})
                        self.new_urls_houses.append(href)
                driver.quit()
                break

    def save_links_to_csv(self):
        df = pd.DataFrame(self.urls_houses)
        csv_path = os.path.join(script_directory, subdirectory, f'ZimmoLinks_{str(self.city_name)}_{str(today)}.csv')
        df.to_csv(csv_path, index=False, header=True)

    def process_links(self):
        extracted_data_list = []
        try:
            with open(self.csv_path, newline='') as f:
                reader = csv.reader(f, delimiter=",")
                all_links_new = list(reader)

        except Exception as e:
            pprint(f"Error: {e}")
            pprint("Can not open saved CSV-link file")

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.extract_data_from_link, link_info["Url: "]) for link_info in self.urls_houses]

            for future in concurrent.futures.as_completed(futures):
                try:
                    extracted_data = future.result()
                    if extracted_data is not None:
                        extracted_data_list.append(extracted_data)
                except Exception as e:
                    print(f"Error when processing a link: {e}")

        extracted_data_df = pd.DataFrame(extracted_data_list)
        extracted_data_csv_path = os.path.join(script_directory, subdirectory, f"Extracted_Data_{self.city_name}_{today}.csv")
        extracted_data_df.to_csv(extracted_data_csv_path, index=False, header=True)

        try:
            with open(extracted_data_csv_path, newline='') as f:
                reader = csv.reader(f, delimiter=",")
                all_data = list(reader)

        except Exception as e:
            pprint(f"Error: {e}")
            pprint("Can not open saved CSV-link file")

        df = self.create_database(all_data)

        file_path_city_only = os.path.join(script_directory, subdirectory, f"Final_File_{self.city_name}.csv")

        try:
            if os.path.exists(file_path_city_only):
                df_initial_city = pd.read_csv(file_path_city_only)
                final_df_city = pd.concat([df, df_initial_city], ignore_index=True)
                final_df_city.to_csv(file_path_city_only, index=False, header=True)
            else:
                try:
                    initial = os.path.join(script_directory, subdirectory, f"Initial_File.csv")
                except:
                    print("Can not open initial file for  " + str(self.city_name) + ", bruv.")
                df_initial_city = pd.read_csv(initial)
                try:
                    final_df_city = pd.concat([df, df_initial_city], ignore_index=True)
                except:
                    print("Cannot concat initial file and the new DataFrame")
                final_df_city.to_csv(file_path_city_only, index=False, header=True)
        except:
            print("Can not open saved CSV-link file " + str(self.city_name) + " cuz there is no, bruv.")

        file_path_full = os.path.join(script_directory, subdirectory, f"Final_File.csv")
        try:
            if os.path.exists(file_path_full):
                df_initial = pd.read_csv(file_path_full)
                final_df = pd.concat([df, df_initial], ignore_index=True)
                output_path = os.path.join(script_directory, subdirectory, f"Final_File.csv")
            else:
                try:
                    initial = os.path.join(script_directory, subdirectory, f"Initial_File.csv")
                except:
                    print("Can not open initial file for  " + str(self.city_name) + ", bruv.")
                df_initial = pd.read_csv(initial)
                try:
                    final_df = pd.concat([df, df_initial], ignore_index=True)
                except:
                    print("Cannot concat initial file and the new DataFrame")
        except:
            print("Can not open saved CSV-link file full file cuz there is no, bruv.")

        output_path = os.path.join(script_directory, subdirectory, f"Final_File.csv")
        final_df.to_csv(output_path, index=False)


if __name__ == "__main__":
    city_name = "Antwerpen"
    today = date.today()
    today = today.strftime("%d-%m-%Y")
    
    scraper = Scraper(city_name)
    scraper.scrape_links()
    scraper.save_links_to_csv()
    scraper.process_links()
