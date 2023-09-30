import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import csv
import os
from fake_useragent import UserAgent

### Get Proxies from a URL
def get_proxies(url):
    ua = UserAgent()
    response = requests.get(url, headers={'User-Agent': ua.random})
    soup = BeautifulSoup(response.text, 'html.parser')
    return [f"{tds[0].text.strip()}:{tds[1].text.strip()}" for tds in (row.find_all('td') for row in soup.select('tbody tr')) if len(tds) >= 2]

### Function to Check the Health of a Proxy
def check_proxy(proxy_url):
    try:
        response = requests.get("http://www.example.com", proxies={"http": proxy_url, "https": proxy_url}, timeout=5)
        if response.status_code == 200:
            print(f"Proxy {proxy_url} is alive!")
            return proxy_url
        else:
            print(f"Proxy {proxy_url} returned status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error connecting to proxy {proxy_url}: {e}")
        print(f"Proxy {proxy_url} is dead.")
        return None

### List of URLs to Scrape for Proxies
urls = ['https://www.sslproxies.org/', 'https://hidemy.life/ru/proxy-list-servers']
all_proxies = [proxy for url in urls for proxy in get_proxies(url)]
all_proxies_with_http = [f"http://{proxy}" for proxy in all_proxies]

### Determine Number of Worker Threads
default_max_workers = os.cpu_count() or 1
max_workers = min(len(all_proxies_with_http), default_max_workers)

### Check Proxies in Parallel
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    alive_proxies = list(filter(None, executor.map(check_proxy, all_proxies_with_http)))



### Save Proxies to CSV
data_dir = 'Data'
os.makedirs(data_dir, exist_ok=True)
csv_file = os.path.join(data_dir, 'alive_proxies.csv')

header = ['Alive Proxies']
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows([[proxy] for proxy in alive_proxies])

print(f"Alive proxies saved to {csv_file}")