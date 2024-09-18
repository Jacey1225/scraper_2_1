from src.download_url_elements import Download_Elements
from bs4 import BeautifulSoup
import requests
import pickle
import time
import os

#variable carrying element class
de = Download_Elements()
#variable carrying pickle folder 
PICKLE_FOLDER = os.path.join('/Users/jaceysimpson/Vscode/scraper_2_1', "pickles")

#directory path for the pickle folder
directory = os.path.abspath(PICKLE_FOLDER)
if not os.path.exists(directory):
    os.makedirs(directory)

#filenames of all data
soup_filename = 'soup_data'
element_filename = 'element_data'
max_age = 3 #days

#pulling local data files 
soup_data = de.verify_soup_data_age(soup_filename, max_age)
DATA = de.verify_element_data_age(element_filename, max_age, soup_data)

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

    def rerun_product_specifics(self):
        #reruns program if specifics_data is None
        product_specifics = self.fetch_product_specifics()
        if product_specifics is not None:
            return product_specifics
    
    def pickle_product_specifics(self, filename, specifics_data):
        #saves the data via pickle.dump()
        print('saving specifics data')
        file_path = os.path.join(directory, filename)

        with open(file_path, 'wb') as f:
            pickle.dump((specifics_data, time.time()), f)
    
    def age_variable(self, timestamp):
        seconds = time.time() - timestamp
        age = seconds / (60 * 60 * 24)
        
        return age

    def load_specifics_data(self, filename, max_age):
        #loads data via pickle.load() creating both a data variable and a timestamp
        file_path = os.path.join(directory, filename)

        #if the path does not yet exist, return None
        if not os.path.exists(file_path):
            return None
        
        print('loading specifics data')
        with open(file_path, 'rb') as f:
            specifics_data, timestamp = pickle.load(f)

        age = self.age_variable(timestamp)
        print(f'product specifics age: {age}')

        #if age exceeds limit return None
        if age <= max_age:
            print('age accepted')
            return specifics_data
        else:
            print('age exceeded')
            return None
    
    def verify_specifics_age(self, filename, max_age):
        product_specifics = self.load_specifics_data(filename, max_age)

        if product_specifics is None:
            print('specifics data is None - reloading')
            product_specifics = self.rerun_product_specifics()
            self.pickle_product_specifics(filename, product_specifics)
        
        return product_specifics