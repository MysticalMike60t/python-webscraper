import os
import requests
import sys
import re
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse

mode = 0o777
fileEncoding = "utf-8"

scrapeOutputDirectory = "./output/scrapes"
defaultPageFileName = "index.html"
specificFileName = "specific-items.html"

def extract_link_content(folder_path, response_content):
    link_content = re.findall(r'<link[^>]*\/>', response_content.decode(fileEncoding))
    if link_content:
        with open(os.path.join(folder_path, specificFileName), "w", encoding=fileEncoding) as f:
            for item in link_content:
                f.write(item + "\n")

def create_site_folder_from_scrape(url, response_content):
    domain = urlparse(url).netloc
    folder_path = os.path.join(scrapeOutputDirectory, domain)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, mode)
        
    with open(os.path.join(folder_path, defaultPageFileName), "w", encoding=fileEncoding) as f:
        soup = bs(response_content, 'html.parser')
        prettyHTML = soup.prettify()
        f.write(prettyHTML)
        
    # Extract specific content and save it
    extract_link_content(folder_path, response_content)

def main():
    print("Enter the URL with connection type (http:// or https://):")
    url = input().strip()

    if not (url.startswith('http://') or url.startswith('https://')):
        print("Invalid URL. Please include 'http://' or 'https://'")
        sys.exit(1)

    response = requests.get(url)
    
    if response.status_code == 404:
        print("Error: Page not found")
    elif response.status_code != 200:
        print("Error: Failed to fetch the page. Status code:", response.status_code)
    else:
        print("Page content saved successfully.")
        create_site_folder_from_scrape(url, response.content)

if __name__ == "__main__":
    main()
