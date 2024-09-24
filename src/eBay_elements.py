from src.eBay_urls import eBay_URLS
from src.pickle_data import Pickle_Data
from bs4 import BeautifulSoup
import requests
import time
import os

eu = eBay_URLS()
DATA = eu.save_eBay_url_data()

class eBay_Elements:
    def __init__(self, data = DATA):
        '''Initializes the class with DATA
        
        args:
            DATA(list: eBay urls): Used to scrape each url in eBay
            
        '''
        self.data = data

    def get_request(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text

    def get_soup(self, raw_content):
        soup = BeautifulSoup(raw_content, 'html.parser')
        if soup:
            return soup

    def fetch_all_soups(self):
        soup_data = []

        for url in self.data:
            content = self.get_request(url)
            soup = self.get_soup(content)
            if soup:
                soup_data.append(soup)

        return soup_data

#####################
# DOWNLOADING SOUPS #
#####################
    def soup_function(self):
        soup_data = self.fetch_all_soups()
        if soup_data is not None:
            return soup_data

    def save_eBay_soup_data(self):
        filename = 'eBay_soup_data'
        max_age = 3 #days
        function = self.soup_function

        sesd = Pickle_Data(filename, max_age, function)
        return sesd.verify_data_age()

    