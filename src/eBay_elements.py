from src.eBay_urls import eBay_URLS
from src.pickle_data import Pickle_Data
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
        max_age = 3 #days
        function = self.soup_function

        #sesd == save eBay soup data
        sesd = Pickle_Data(filename, max_age, function)
        return sesd.verify_data_age()

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

#################
# FETCH AVERAGE #
#################
    def clean_price(self, price: str) -> float:
        #price cleaning, verifying several instances in which the price string may contain characters that conflict
        #with type conversion
        new_price = ""
        
        if "$" in price:
            new_price = price.replace("$", "") #replace "$" with None
        if "to" in new_price:
            price_end = new_price.find(".") #create a new idnex to take the first numerical value
            new_price = new_price[:price_end + 3]
        if "," in new_price:
            new_price = new_price.replace(",", "") #if the float is a 4-digit whole number, remove the comma 

        if new_price is None or new_price is '': #if the new_price does not contain a numerical value, return None
            return None
        
        return float(new_price)

    def get_price(self, item):
        price_element = item.find('span', class_='s-item__price') #in product element, find price element
        price = price_element.get_text() #isolate the price
        if price:
            print(price)
            return self.clean_price(price)

    def fetch_average(self, elements):
        price_list = [] #find all prices within an element/page
        for item in elements:
            price = self.get_price(item) 
            price_list.append(price)
        
        prices = pd.Series(price_list) #convert the list of prices to a pandas dataset
        average = prices.mean() #get the average of the dataset
        return average.round(2) #return and round to the nearest 100th

    def gather_averages(self):
        #combines the soup data with the aboe helper methods to create a list of elements as type <String>
        average_data = []
        soup_data = self.save_eBay_soup_data() #soup data 

        for soup in soup_data:
            print('fetching raw elements')
            raw_elements = self.fetch_element(soup) #raw_elements fetched from helper method

            average = self.fetch_average(raw_elements) #get avereage of all elements within a soup
            if average is not None:
                average_data.append(average) #all average data within the soup data

        return average_data
    

##################
# ELEMENT SAVING #
##################
    def element_function(self):
        #run if result in verify_data_age is None
        average_data = self.gather_averages() #function to run element fetching
        if average_data is not None:
            return average_data 

    def save_eBay_element_data(self):
        filename = 'eBay_average_data' 
        max_age = 3 #days
        function = self.element_function

        #seed = save eBay soup data
        seed = Pickle_Data(filename, max_age, function) #verify data age, hold the maximum age of 3 days, if exceeded return None
        return seed.verify_data_age()




    