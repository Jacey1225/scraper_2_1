from src.download_backmarket_urls import Download_URLS
from bs4 import BeautifulSoup
import pickle
import requests 
import time
import os

du = Download_URLS()
PICKLE_FOLDER = os.path.join('/Users/jaceysimpson/Vscode/scraper_2_1', "pickles")

directory = os.path.abspath(PICKLE_FOLDER) 
if not os.path.exists(directory):
    os.makedirs(directory)

filename = 'url_data'
max_age = 3 #days
DATA = du.verify_data_age(filename, max_age)


class Download_Elements:
    def __init__(self, data = DATA):
        '''Initializes the class with DATA
        
        args:
            DATA(list: backmarket urls): Used to scrape each url
            
        '''
        
        self.data = data

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
        return BeautifulSoup(content, 'html.parser')

    def fetch_soup_via_content(self):
        #Uses soup function to loop through content and return a list of soups
        soup_list = []
        for content in self.get_response_content():
            soup = self.get_soup_variable(content)
            soup_list.append(soup)
        
        return soup_list

#########################
# DOWNLOADING SOUP DATA #
#########################
    def rerun_soup_program(self):
        return self.fetch_soup_via_content()

    def pickle_soup_data(self, filename, soup_data):
        file_path = os.path.join(directory, filename)

        with open(file_path, 'wb') as f:
            pickle.dump((soup_data, time.time()), f)
    
    def age_variable(self, timestamp):
        seconds = time.time() - timestamp
        age = seconds / (60 * 60 * 24)
        return age
    
    def load_soup_data(self, filename, max_age):
        file_path = os.path.join(directory, filename)

        if not os.path.exists(file_path):
            return None

        with open(file_path, 'rb') as f:
            soup_data, timestamp = pickle.load(f)

        age = self.age_variable(timestamp)

        if age <= max_age:
            return soup_data
        else:
            return None
        
    def verify_soup_data_age(self, filename, max_age):
        soup_data = self.load_soup_data(filename, max_age)

        if soup_data is None:
            soup_data = self.rerun_soup_program()
            self.pickle_soup_data(filename, soup_data)

        return soup_data

########################### 
# RETRIEVING ELEMENT DATA #
###########################