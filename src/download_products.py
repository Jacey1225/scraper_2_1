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

    def split_title(self, product):
        #pre-assumed titles of products based on given element data
        prefixes = {'iPhone', 'MacBook', 'iPad', 'Nintendo', 'PlayStation', 'Switch', 'Xbox'}

        for prefix in prefixes:
            if product.find(prefix) != -1:
                start_title = product.find(prefix) #beginning index of the title
                end_title = product.find('-', start_title) #ending index of the title
                if end_title == -1:
                    end_title = len(product) #backup index if end_title cannot be found
                
                title = product[start_title:end_title - 1]
                
                if title is not None:
                    return title
                else:
                    print(f'title not found{product}')
                    return 'unkown'
                    
    def split_price(self, product):
        start_price = product.rfind('$') #beginning index of price
        end_price = product.rfind('.') #ending index of price
        if end_price == -1:
            end_price = len(product) #backup index if end_price cannot be found

        price = product[start_price:end_price]
        
        if price is not None:
            return price
        else:
            return '$0.0'
            print(f'price not found {product}') #printing values not found 

    def fetch_product_specifics(self):
        #uses the data and both helper methods above to create a new list of data holding a stripped version of the product details
        strip_products = []
        print(f'finding titles and prices in element_data: {len(self.data)}')
        for item in self.data:
            for product in item:
                #find title and price via helper methods
                title = self.split_title(product) #stripped title string
                price = self.split_price(product) #stripped price string

                attributes = (title, price) #tuple value 
                strip_products.append(attributes)
        
        print(f'Length of element data: {len(self.data)}')
        print(f'Length of stripped data: {len(strip_products)}')
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