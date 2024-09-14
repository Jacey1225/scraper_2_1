from src.download_backmarket_urls import Download_URLS
from bs4 import BeautifulSoup
import pickle
import requests 
import time
import os

du = Download_URLS()
filename = 'url_data'
max_age = 3 #days

DATA = du.verify_data_age(filename, max_age)
PICKLE_FOLDER = '/pickles'

class Download_Elements:
    def __init__(self, DATA):
        '''Initializes the class with DATA
        
        args:
            DATA(list: backmarket urls): Used to scrape each url
            
        '''
        
        self.data = DATA

########################
# RETRIEVING SOUP DATA #
########################

    def get_response_content(self):
        #appends text responses from the url data via requests 
        content_list = []
        for url in self.data:
            response = requests.get(url)
            if response.status_code == 200:
                content_list.append(response.text)
        
        return content_list
    def get_soup_variable(self, content):
        #Uses the response content to create valid html input via BeautifulSoup
        return BeautifulSoup(content, 'lxml')

    def fetch_soup_via_content(self):
        #Uses soup function to loop through content and return a list of soups
        soup_list = []
        for content in self.get_response_content():
            soup = self.get_soup_variable(content)
            soup_list.append(soup)
        
        return soup_list

###########################
# RETRIEVING ELEMENT DATA #
###########################


if __name__ == '__main__':
    de = Download_Elements(DATA)
    print(de.fetch_soup_via_content())
        