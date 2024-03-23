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

html_tags = ["link", "html", "head", "title", "meta", "body", "div", "p", "a", "img", "ul", "ol", "li", "table", "tr", "td", "th", "form", "input", "button", "textarea"]

def extract_content(folder_path, response_content):
    isTag = input("Are you looking for a tag? - (y / n): ")
    if isTag == "y":
        isOnelineTag = input("Is the tag one line? (ex: <link rel="" href="" />) - (y / n): ")
        if isOnelineTag == "y":
            search_term = input("Enter the tag you want to find: ")
        
            if search_term in html_tags:
                link_content = re.findall(r'<' + search_term + r'[^>]*\/>', response_content.decode('utf-8'))
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
    else:
        return

def create_site_folder_from_scrape(url, response_content):
    domain = urlparse(url).netloc
    folder_path = os.path.join(scrapeOutputDirectory, domain)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, mode)
        
    with open(os.path.join(folder_path, defaultPageFileName), "w", encoding=fileEncoding) as f:
        soup = bs(response_content, 'html.parser')
        prettyHTML = soup.prettify()
        f.write(prettyHTML)
        
    extract_content(folder_path, response_content)

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
