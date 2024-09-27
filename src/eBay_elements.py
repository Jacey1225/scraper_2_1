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
        #forms a content variable via requests.get >> url
        response = requests.get(url) #request session
        if response.status_code == 200:
            return response.text #return content
        else:
            print(f'error running request for {url}')

    def get_soup(self, url):
        #BeatifulSoup >> convert content as html.parser
        raw_content = self.get_request(url) #response content
        soup = BeautifulSoup(raw_content, 'html.parser') #html parser 
        if soup:
            return str(soup)
        else:
            print(f'cannot complete conversion for {url}')

    def fetch_all_soups(self):
        #get soup content via url data in eBay_urls.py 
        soup_data = [] #empty soup data list

        for url in self.data:
            print(f'getting soup for {url}')
            soup = self.get_soup(url) #specified url soup
            if soup:
                print('pass')
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

    