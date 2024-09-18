from src.download_url_elements import Download_Elements
from src.pickle_data import Pickle_Data
from bs4 import BeautifulSoup
import requests
import pickle
import time
import os

#variable carrying element class
de = Download_Elements()

#pulling local data files 
DATA = de.save_element_data()

class Download_Products:
    def __init__(self, data = DATA):
        '''Initializes the class with DATA
        
        args:
            DATA(list: backmarket product content): Used to find all product specifics
            
        '''
        self.data = data
    
################################
# RETRIEVING PRODUCT SPECIFICS #
################################

    def find_title(self, product):
        #fetches the title of product content
        text = product.get('text', '')
        index = text.find('-')
        title = text[:index].strip()
        return title
    
    def find_price(self, product):
        #fetches the price of product content
        text = product.get('text', '')
        start_index = text.rfind('$')
        end_index = text.rfind('.')
        price = text[start_index:end_index]
        return price

    def fetch_product_specifics(self):
        #uses the data and both helper methods above to create a new list of data holding a stripped version of the product details
        strip_products = []
        for product in self.data:
            #find title and price via helper methods
            title = self.find_title(product)
            price = self.find_price(product)
            if title and price:
                product_item = (title, price)
                strip_products.append(product_item)
            else:
                product_item = None

        return strip_products

#################################
# DOWNLOADING PRODUCT SPECIFICS #
#################################

    def product_function(self):
        #reruns program if specifics_data is None
        product_specifics = self.fetch_product_specifics()
        if product_specifics is not None:
            return product_specifics
    
    def save_product_specifics(self):
        #using Pickle_Data...locally save data to a file path(filename)
        filename = 'product_specifics_data'
        max_age = 3 #days
        function = self.product_function

        #using variables from above create a class instance and call the function
        spd = Pickle_Data(filename, max_age, function)
        return spd.verify_data_age()