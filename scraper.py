import os
import sys
import re
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

scrapeOutputDirectory = "./output/scrapes"
defaultPageFileName = "index.html"
specificFileName = "specific-items.html"

mode = 0o777
fileEncoding = "utf-8"

html_tags = ["link", "html", "head", "title", "meta", "body", "div", "p", "a", "img", "ul", "ol", "li", "table", "tr", "td", "th", "form", "input", "button", "textarea"]

def extract_content(folder_path, response_content):
    searchFor = input("What do you want to search for? - (tag / class): ")
    if searchFor == "tag":
        isOnelineTag = input("Is the tag one line? (ex: <link rel= href= />) - (y / n): ")
        if isOnelineTag == "y":
            search_term = input("Enter the tag you want to find: ")
            if search_term in html_tags:
                link_content = re.findall(r'<' + search_term + '\s[^>]*\/?>', response_content)
                if link_content:
                    with open(os.path.join(folder_path, specificFileName), "w", encoding='utf-8') as f:
                        i = 0
                        for item in link_content:
                            i += 1
                            f.write(item + "\n")
                            print(str(i) + " found!", end="\r")
                        print(str(i) + " found!")
                else:
                    print("No matching tags found.")
                print("Exported to " + scrapeOutputDirectory.replace("./", "") + "/" + specificFileName)
            else:
                print("'{}' not valid HTML tag.".format(search_term))
    elif searchFor == "class":
        search_class = input("Enter the class you want to find: ").strip()
        try:
            soup = bs(response_content, 'html.parser')
            elements_with_class = soup.find_all(class_=search_class)
            if elements_with_class:
                with open(os.path.join(folder_path, specificFileName), "w", encoding='utf-8') as f:
                    for element in elements_with_class:
                        f.write(str(element) + "\n")
                    print("Found {} elements with class '{}'.".format(len(elements_with_class), search_class))
                    print("Exported to " + scrapeOutputDirectory.replace("./", "") + "/" + specificFileName)
            else:
                print("No elements found with class '{}'.".format(search_class))
        except TimeoutException:
            print("Timed out waiting for elements with class '{}'.".format(search_class))

def create_site_folder_from_scrape(url):
    print("Fetching page content...")
    
    options = Options()
    options.headless = False
    options.set_preference("permissions.default.desktop-notification", 1)
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    driver.minimize_window()
    
    time.sleep(10)
    
    response_content = driver.page_source
    
    domain = urlparse(url).netloc
    folder_path = os.path.join(scrapeOutputDirectory, domain)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, mode)
        
    with open(os.path.join(folder_path, defaultPageFileName), "w", encoding=fileEncoding) as f:
        f.write(response_content)
        
    extract_content(folder_path, response_content)

    driver.quit()

def main():
    print("Enter the URL with connection type (http:// or https://):")
    url = input().strip()

    if not (url.startswith('http://') or url.startswith('https://')):
        print("Invalid URL. Please include 'http://' or 'https://'")
        sys.exit(1)
    print("Opening Browser...")
    create_site_folder_from_scrape(url)

if __name__ == "__main__":
    main()