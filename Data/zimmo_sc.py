
#import nest_asyncio
#nest_asyncio.apply()


###Imports###
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

from collections import Counter
import re
import pandas as pd
import numpy as np

###Change city name###
city_name = "Erembodegem"

###Empty Lists###
headdict = {'Prijs':"",
             'Adres':"",
             'Stad':"",
             'Type':"",
             'Bouwjaar':"",
             'EPC':"",
             'Woonopp.':"",
             'Slaapkamers':"",
             'Badkamers':"",
             'Grondopp.':"",
             'Bebouwing':"",
             'Garages':"",
             'Tuin':"",
             'Dagen':"",
             'Link':"",
             'Handelsopp.':"",
             }
head = ['Prijs','Adres','Type','Bouwjaar','EPC','Woonopp.','Slaapkamers','Badkamers','Grondopp.','Bebouwing','Garages','Tuin','Garage']
urls_houses = []
new_urls_houses = []

###Get the directory of the script##
script_directory = os.path.dirname(os.path.abspath(__file__))

###Specify the subdirectory###
subdirectory = "Data"

###Today###
today = date.today()
today = today.strftime("%d-%m-%Y")
start_time = time.time()

def scroll_list(work_list):
    newlist = []
    tmp_list = []
    for word in work_list:
        word = word.split(",")
        newlist.extend(word)  # <----
    new_list = [s.replace("[", "") for s in newlist]
    new_list = [s.replace("'", "") for s in new_list]
    new_list = [s.replace(" ", "") for s in new_list]
    for data1, data2 in headdict.items():
        for x in range(0,int(len(new_list))):
            
            if data1 ==  new_list[x]:
                res = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", new_list[x+1])
                res = re.sub(r"\B([A-Z])", r" \1", res)
                headdict.update({data1:res})
                if data1 == "Adres":
                    res = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", new_list[x+2])
                    headdict.update({"Stad":res})
                if data1 in ('Prijs', 'Woonopp.','Grondopp.'):
                    res2 = re.sub('\D', '', headdict[data1])
                    headdict.update({data1:res2})
            if data1 == "Link":
                if new_list[x][0:5]=="https":
                    headdict.update({data1:new_list[x]})
            if data1 == "Dagen":
                if new_list[x][0:5]=="Days:":
                    headdict.update({data1:new_list[x][5:-1]})
    tmp_list.append(headdict.copy())
    return headdict.copy()

def c_database(all_data):
    new_temp = []
    for i in range(0,int(len(all_data))):
        work_list = all_data[i]
        tempered_list = scroll_list(work_list)
        new_temp.append(tempered_list)
    df = pd.DataFrame(new_temp[0], index=range(1), columns=list(headdict.keys()))
    for i in range(0,int(len(new_temp))):
        df = df.append(new_temp[i], True)
    return df

def cookie_ok():
    try:
        search_box = driver.find_element("id", "didomi-notice-agree-button")
        search_box.send_keys('ChromeDriver')
        time.sleep(4)
        search_box.click()
        search_box.submit()
    except:
        pass  # Handle the case where the element is not found or other exceptions

def city_input(city):
    search = driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div[1]/div[1]/zimmo-search-form/div[1]/app-cities-search/div/app-places-lookup/app-places-search-box/input")
    search.send_keys(city)
    search.send_keys(Keys.RETURN)
    searchbutton = driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div[1]/div[1]/zimmo-search-form/div[1]/button")
    time.sleep(4)
    searchbutton.click()   


### GETTING TO THE FIRST PAGE AND INPUT CITY NAME ###


###User Agent Load###
ua = UserAgent()
user_agent = ua.random
options = webdriver.ChromeOptions()

###Set the fake user agent###
options.add_argument(f"user-agent={user_agent}")

###Add options to disable notifications and run headless###
options.add_argument("--disable-notifications")
options.add_argument("--headless")

###Specify the path to the ChromeDriver executable###
service = Service(executable_path='C:\\Program Files (x86)\\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.zimmo.be/nl/")

###Handling cookie consent ###
cookie_ok()

###Input city and getting the first page with links###
city_input(city_name)
time.sleep(4)
driver.current_url
newpage = driver.current_url
driver.quit()

elapsed_time = time.time() - start_time
print(f"Elapsed Time: {elapsed_time} seconds")


### WORKING THE FIRST PAGE GETTING PAGINATION LINK/SAVING LINKS FROM THE FIRST PAGE ###


###User Agent Load###
ua = UserAgent()
user_agent = ua.random

###Set the fake user agent###
options.add_argument(f"user-agent={user_agent}")
###Specify the path to the ChromeDriver executable###
service = Service(executable_path='C:\\Program Files (x86)\\chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
###Getting the page
driver.get(newpage)
###Handling cookie consent###
cookie_ok()

###Getting pagination/max pages/now page###
try:
    max_pages = driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div[4]/div[2]/div[3]/div[3]/ul/li[13]/a/span").text
    now_t = driver.find_element(By.CLASS_NAME,"pagination")
    now_page = now_t.find_element(By.CLASS_NAME,"active").text
except:
    ###If Number less then 10###
    now_t = driver.find_element(By.CLASS_NAME,"pagination")
    now_page = now_t.find_element(By.CLASS_NAME,"active").text
    max_pageszz = driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div[4]/div[2]/div[3]/div[3]/ul").text
    number = int(max_pageszz[-1])+1
    max_pages = driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div[4]/div[2]/div[3]/div[3]/ul/li["+str(number)+"]/a/span").text
    

###Finding links on the page###
elems = driver.find_elements(By.CLASS_NAME,'property-item_link')
for elem in elems:
    href = elem.get_attribute('href')
    if href is not None:
        urls_houses.append({"Url: ":href,"Date: ":today})
        new_urls_houses.append(href)
        
#next_t = driver.find_element(By.XPATH,"/html/body/div[3]/div[3]/div[4]/div[2]/div[3]/div[3]/ul/li[14]/a")
next_t = driver.find_element(By.CLASS_NAME,"last")
next_t2 = next_t.find_element(By.XPATH,".//a")
next_t2.click() 
time.sleep(4)
driver.current_url
newpage = driver.current_url
driver.quit()

###Getting the link for pagination###
text = newpage
head = text.partition('=')
basic= head[0]+"="+head[2].partition('=')[0]+"="

elapsed_time = time.time() - start_time
print(f"Elapsed Time: {elapsed_time} seconds")


### WORKING THE FIRST PAGE GETTING PAGINATION LINK/SAVING LINKS FROM THE REST OF THE PAGES ###


n = 0
for x in range(2,int(max_pages)+1):
    ###Adding a number to pagination
    n = + x
    new_page = basic+str(x)

    ##Starting the sriver
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f"user-agent={user_agent}")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(new_page)
    
    # Handling cookie consent (if required)
    cookie_ok()

    ###Getting page now###
    now_t = driver.find_element(By.CLASS_NAME,"pagination")
    now_page = now_t.find_element(By.CLASS_NAME,"active").text
    pprint(now_page)
    
    if int(now_page) <= int(max_pages):
        pprint("Page - "+str(now_page)+"/"+str(max_pages))
        elems = driver.find_elements(By.CLASS_NAME,'property-item_link')
        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None:
                urls_houses.append({"Url: ":href,"Date: ":today})
                new_urls_houses.append(href)
        driver.quit()
        elapsed_time = time.time() - start_time
        print(f"Elapsed Time: {elapsed_time} seconds")
        
    else:
        elems = driver.find_elements(By.CLASS_NAME,'property-item_link')
        pprint("Page - "+str(now_page)+"/"+str(max_pages))
        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None:
                urls_houses.append({"Url: ":href,"Date: ":today})
                new_urls_houses.append(href) 
        driver.quit()
        
        elapsed_time = time.time() - start_time
        print(f"Elapsed Time: {elapsed_time} seconds")
        break

###Creating dataframe###
df = pd.DataFrame(urls_houses)

###Constructing the path to subdir to save csv###
csv_path = os.path.join(script_directory, subdirectory,f'ZimmoLinks_'+str(city_name)+'_'+str(today)+'.csv')
df.to_csv(csv_path, index=False, header=True)


###BORED TYPING - REWORKING THE DATA AND SAVING IT. NOT A LOT CAN GO WRONG HERE TBH###


all_details = []
# Try to open the saved CSV file using csv.reader
try:
    with open(csv_path, newline='') as f:
        reader = csv.reader(f, delimiter=",")
        all_links_new = list(reader)
        
except Exception as e:
    pprint(f"Error: {e}")
    pprint("Can not open saved CSV-link file")

for n in range(1,len(all_links_new)):
    try:
        work_links = new_urls_houses[n]
        options = webdriver.ChromeOptions()
        ua = UserAgent()
        user_agent = ua.random
        options.add_argument(f"user-agent={user_agent}")
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get(new_urls_houses[n])
        cookie_ok()
        response = driver.page_source
        html_soup = BeautifulSoup(response, 'lxml')
        driver.close()
        details = html_soup.find('ul', class_='main-features')
        days_on = html_soup.find('div', class_='stat-text text')
        
        popper = work_links.find("?")
        to_print_link = work_links[:int(popper)-1]
            
        try:
            split_details = list(details.stripped_strings)
            evens = [x for x in range(len(split_details)) if x&1 == 0]
        except:
            pass
        #det = {split_details[f]: split_details[f+1] for f in evens}
        split_details.append(to_print_link)
        try:
            days_online = str(int(days_on.text))
            split_details.append("Days: "+days_online)
        except:
            pass
        all_details.append(split_details)
        pprint(str(n)+"/"+str(len(all_links_new)))
        #pprint(split_details)
        time.sleep(5)
        
        elapsed_time = time.time() - start_time
        print(f"Elapsed Time: {elapsed_time} seconds")
        print_details = np.array(all_details,dtype=object,)
        
        ###Creating dataframe
        df = pd.DataFrame(all_details)
        # Construct the path for saving the CSV file in the subdirectory
        csv_path = os.path.join(script_directory, subdirectory,f"ZimmoLinks_"+str(city_name)+str(today)+"_detail.csv")
        
        df.to_csv(csv_path, index=False, header=True)

    except:
        break
    
try:
    with open(csv_path, newline='') as f:
        reader = csv.reader(f, delimiter=",")
        all_data = list(reader)
        
except Exception as e:
    pprint(f"Error: {e}")
    pprint("Can not open saved CSV-link file")

df = c_database(all_data)

csv_path = os.path.join(script_directory, subdirectory,f"Database_"+str(city_name)+str(today)+"_detailComp.tsv")
df.to_csv(csv_path, index=False, header=True, sep = '\t')