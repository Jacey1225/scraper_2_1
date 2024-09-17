from bs4 import BeautifulSoup
import os
import time
import requests
import pickle

BASE_URL = "https://www.backmarket.com"
PICKLE_FOLDER = os.path.join('/Users/jaceysimpson/Vscode/scraper_2_1', 'pickles')

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
        return BeautifulSoup(content, "lxml")

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
        content = self.get_response_content()
        soup = self.create_soup_variable(content)
        

        element = self.create_element_variable(soup, "li", ("md:col-span-3 flex", "md:col-span-3 col-span-2 flex"))

        if element is not None:
            return element
        else:
            print("element not found")
            return None

    def store_href_addresses(self, main_element):
        # This method will search through the main element to find sections that contain an href address.
        # Whenever one is located, it will store it in a list and return that list back
        href_urls = []
        for item in main_element:
            href_container = item.find(
                "a",
                class_="shadow-short rounded-lg relative block no-underline motion-safe:transition motion-safe:duration-200 motion-safe:ease-in bg-float-default-low focus-visible-outline-default-hi cursor-pointer hover:bg-float-default-low-hover hover:shadow-long inline-block min-h-[13rem] w-full sm:min-h-[13.5rem] h-320",
            )
            href_address = href_container.get("href")
            if not href_address is None:
                href_urls.append(str(self.url + href_address))
            else:
                print("no href address found")
                continue

        return href_urls

    def add_pages(self, href_urls, max_pages=4):
        #Adds additional url page links to expand search results
        count = 0
        pages = []
        for url in href_urls:
            for count in range(max_pages):
                page = str(url) + f'?p={count}'
                pages.append(page)

        return pages  

    # --vv--
    # Downloading url list via pickle

    def rerun_url_program(self):
        # reruns the program if the value returned from def load_data is None

        main_element = self.fetch_main_page_element()
        href_urls = self.store_href_addresses(main_element)
        return self.add_pages(href_urls)

    def pickle_url_data(self, filename, url_data):
        # Saves data into a file via pickle.dump()
        # Get the absolute path from a relative path
        directory = os.path.abspath(PICKLE_FOLDER)

        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, filename)

        print("saving data")
        with open(file_path, "wb") as f:
            pickle.dump((url_data, time.time()), f)

    def age_variable(self, timestamp):
        # returns the age of last time the program was run
        seconds = time.time() - timestamp
        age = seconds / (60 * 60 * 24)
        return age

    def load_data(self, filename, max_age):
        # variable initialization
        directory = os.path.abspath(PICKLE_FOLDER)
        file_path = os.path.join(directory, filename)
        print(f"file path = {file_path}")

        # Verifies if the path exists
        if not os.path.exists(file_path):
            print("path does not exist")
            return None

        # loads data via pickle.load()
        print("loading data")
        with open(file_path, "rb") as f:
            url_data, timestamp = pickle.load(f)

        # Verifies the age in comparison to the maximum age threshold
        age = self.age_variable(timestamp)
        print(f"Age in days: {age}")

        if age <= max_age:
            return url_data
        else:
            print("age exceeded")
            return None

    def verify_data_age(self, filename, max_age):
        print("verifying data")
        url_data = self.load_data(filename, max_age)

        # verifies the content in the data
        # if data is None, the data will refresh
        if url_data is None:
            print("url data empty")
            url_data = self.rerun_url_program()
            self.pickle_url_data(filename, url_data)

        return url_data

if __name__ == '__main__':
    du = Download_URLS()

    filename = 'url_data'
    max_age = 3 # days

    print(du.verify_data_age(filename, max_age))