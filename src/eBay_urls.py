from src.download_products import Download_Products
from src.pickle_data import Pickle_Data
from bs4 import BeautifulSoup
import requests
import time
import os

dp = Download_Products()
DATA = dp.save_product_specifics()


class eBay_URLS:
    def __init__(self, data = DATA):
        '''Initializes the class with DATA
        
        args:
            DATA(list: product content): Used to find all urls from eBay
            
        '''
        self.data = data

    def create_url(self, raw_title):
        #creates a url using a raw title with character replacements and a base url from eBay

        base_url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw='
        
        #replaces all characters to enter a valid url
        replacements = raw_title.replace(' ', '+').replace('(', '%28').replace(')', '%29')
        ebay_url = base_url + replacements

        return ebay_url

    def fetch_all_urls(self):
        #connects this function for creating urls to the list of titles 
        #returns a new list of urls
        print('generating eBay urls')


        eBay_urls = []
        for title, price in self.data:
            url = self.create_url(title)
            if url:
                eBay_urls.append(url)

        return eBay_urls

#########################
# DOWNLOADING EBAY URLS #
#########################

    def eBay_url_function(self):
        eBay_urls = self.fetch_all_urls()
        return eBay_urls

    def save_eBay_url_data(self):
        filename = 'eBay_urls'
        max_age = 3 #days
        function = self.eBay_url_function

        seud = Pickle_Data(filename, max_age, function)
        return seud.verify_data_age()
        