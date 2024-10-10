from src.eBay_urls import eBay_URLS
from src.save_data import Save_Data
from src.eBay_info import eBay_Info
from bs4 import BeautifulSoup
import requests
import pandas as pd

eu = eBay_URLS()
DATA = eu.save_eBay_url_data()

class eBay_Elements:
    def __init__(self, data = DATA):
        '''Initializes the class with DATA
        
        args:
            DATA(list: eBay urls): Used to scrape each url in eBay
            
        '''
        self.data = data

    def get_request(self, url: str):
        #forms a content variable via requests.get >> url
        response = requests.get(url) #request session
        if response.status_code == 200:
            return response.text #return content
        else:
            print(f'error running request for {url}')

    def get_soup(self, url: str):
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
        function = self.soup_function

        #esd == eBay soup data
        esd = Save_Data(filename, function)
        return esd.fetch_data()

#####################
# FETCHING ELEMENTS #
#####################

    def serialize_elements(self, raw_element):
        #converts all elements to a serializeable type of data
        element_text_data = [] #stores texted elements

        for element in raw_element:
            element_text = element.get_text() #converts element type to string
            if element_text:
                element_text_data.append(element_text) 

        return element_text_data

    def fetch_element(self, soup):
        #retrieves all elements found based on the search profile 
        soup = BeautifulSoup(soup, 'html.parser') #converts soup text into a BeautifulSoup instance
        raw_elements = soup.find_all('li', class_='s-item s-item__pl-on-bottom') #search profile

        if raw_elements:
            return raw_elements

    def gather_averages(self):
        #combines the soup data with the aboe helper methods to create a list of elements as type <String>
        info_data = []
        soup_data = self.save_eBay_soup_data() #soup data 

        for soup in soup_data:
            print('fetching raw elements')
            raw_elements = self.fetch_element(soup) #raw_elements fetched from helper method
            ei = eBay_Info(raw_elements, soup) #seperate class code for fetching prices and popularity rates


            average = ei.fetch_average() #get average of all elements within a soup
            pop = ei.fetch_popularity()
            if average and pop is not None:
                final_price = ei.get_selling_fees(average)
                info = (final_price, pop)
                info_data.append(info) #all average data within the soup data

        return info_data



##################
# ELEMENT SAVING #
##################
    def element_function(self):
        #run if result in verify_data_age is None
        average_data = self.gather_averages() #function to run element fetching
        if average_data is not None:
            return average_data 

    def save_eBay_element_data(self):
        filename = 'eBay_info_data' 
        function = self.element_function

        #eed == eBay element data
        eed = Save_Data(filename, function) #verify data age, hold the maximum age of 3 days, if exceeded return None
        return eed.fetch_data()




    