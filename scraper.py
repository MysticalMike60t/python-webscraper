import os
import requests
import sys
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse

mode = 0o777

scrapeOutputDirectory = "./output/scrapes"
defaultPageFileName = "index.html"

print("Enter the URL with connection type (http:// or https://):")
url = input().strip()

if not (url.startswith('http://') or url.startswith('https://')):
    print("Invalid URL. Please include 'http://' or 'https://'")
    sys.exit(1)

response = requests.get(url)

def create_site_folder_from_scrape(url):
    domain = urlparse(url).netloc
    folder_path = os.path.join(scrapeOutputDirectory, domain)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, mode)
        
    with open(os.path.join(folder_path, defaultPageFileName), "w", encoding="utf-8") as f:
        soup = bs(response.content, 'html.parser')
        prettyHTML = soup.prettify()
        f.write(prettyHTML)
    
def main():
    if response.status_code == 404:
        print("Error: Page not found")
    elif response.status_code != 200:
        print("Error: Failed to fetch the page. Status code:", response.status_code)
    else:
        print("Page content saved successfully.")
        create_site_folder_from_scrape(url)

main()
