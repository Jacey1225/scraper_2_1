from src.pickle_data import Pickle_Data
from bs4 import BeautifulSoup
import os
import time
import requests
import pickle

BASE_URL = "https://www.backmarket.com"

class Download_URLS:
    def __init__(self, url: str = BASE_URL):
        """Initializes the class with a url

        Args:
            url (str, optional): url to scrape. Defaults to BASE_URL.
        """
        self.url = url

    # This class downlaods a set of found redirect urls from a page in backmarket
    def create_soup_variable(self, content):
        # Converts content into readable/valid formatting
        return BeautifulSoup(content, "html.parser")

    def create_element_variable(self, soup, header, header_class):
        # Returns an element containing all the desired content
        return soup.find_all(header, class_=header_class)

    def get_response_content(self):
        # returns content of the main url html
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text

    def fetch_main_page_element(self):
        # Returns the element of a given url
        print('fetching main page content')
        content = self.get_response_content()
        soup = self.create_soup_variable(content)
        


        element = self.create_element_variable(soup, "li", "col-span-1 md:col-span-1 flex")
        if element is not None:
            return element
        else:
            print("element not found")
            return None

    def store_href_addresses(self, main_element):
        # This method will search through the main element to find sections that contain an href address.
        # Whenever one is located, it will store it in a list and return that list back
        print('fetching all href addresses')

        href_urls = []
        for item in main_element:
            href_container = item.find("a", href = True)
            if href_container is not None:
                href_address = href_container.get("href")

                if href_address is not None:
                    print(f'address: {href_address}')
                    href_urls.append(str(self.url + href_address))
                else:
                    print("no href address found")
                    continue

        return href_urls

    def add_pages(self, href_urls, max_pages=4):
        #Adds additional url page links to expand search results
        print('adding pages')
        count = 0
        pages = []
        for url in href_urls:
            for count in range(max_pages):
                page = url + f'?p={count}'
                pages.append(str(page))

        return pages  

    # --vv--
    # Downloading url list via pickle

    def function(self):
        # reruns the program 

        main_element = self.fetch_main_page_element()
        href_urls = self.store_href_addresses(main_element)
        return self.add_pages(href_urls)

    def save_url_data(self):
        filename = 'backmarket_url_data'
        max_age = 3 #days
        function = self.function

        #sud == save url data
        sud = Pickle_Data(filename, max_age, function)
        return sud.verify_data_age()

