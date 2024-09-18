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
            if soup:
                soup_list.extend(soup)
        
        return soup_list

#########################
# DOWNLOADING SOUP DATA #
#########################
    def rerun_soup_program(self):
        #runs the program again if the result of soup_data is None
        return self.fetch_soup_via_content()

    def pickle_soup_data(self, filename, soup_data):
        #saves the soup data via puckle.dump() 
        print('saving soup data')

        file_path = os.path.join(directory, filename)

        #opens file path as 'wb' 
        with open(file_path, 'wb') as f:
            pickle.dump((soup_data, time.time()), f)
    
    def age_variable(self, timestamp):
        #creates an age variable for self.load_element_data() using timestamp in data loading
        seconds = time.time() - timestamp
        age = seconds / (60 * 60 * 24)
        return age
    
    def load_soup_data(self, filename, max_age):
        #loads data - with open(file path on 'rb') and creates data, timestamp variables
        file_path = os.path.join(directory, filename)

        #if the file does not exist method will return None
        if not os.path.exists(file_path):
            print('file path does not exist')
            return None

        print('loading soup file')
        #opens file_path via pickle.load()
        with open(file_path, 'rb') as f:
            soup_data, timestamp = pickle.load(f)

        age = self.age_variable(timestamp)
        print(f'age of soup data - {age}')
        #if the max age limit is not yet exceeded, method will return the data 
        #else it will return None
        if age <= max_age:
            print('age accepted')
            return soup_data
        else:
            print('age exceeded')
            return None
        
    def verify_soup_data_age(self, filename, max_age):
        #loads soup data
        soup_data = self.load_soup_data(filename, max_age)

        #if soup_data is None program will rerun and be saved 
        if soup_data is None:
            print('soup data is None - reloading')
            soup_data = self.rerun_soup_program()
            self.pickle_soup_data(filename, soup_data)

        return soup_data

########################### 
# RETRIEVING ELEMENT DATA #
########################### 

    def fetch_element(self, soup):
        #finds all content containing the same parent calss
        raw_elements = soup.find_all('a', class_='shadow-short rounded-lg relative block no-underline motion-safe:transition motion-safe:duration-200 motion-safe:ease-in bg-float-default-low focus-visible-outline-default-hi cursor-pointer hover:bg-float-default-low-hover hover:shadow-long h-full overflow-hidden text-left')
        #converts raw elements to a text list for serializable data
        element_data = [{'text': a.get_text(strip = True)} for a in raw_elements]
        
        return element_data

    def extend_elements_via_soup_data(self, soup_data):
        #uses the soup_data to gather all data from all urls and make element searches via self.fetch_element()
        all_elements = []

        #loops through soup data to find elements
        for soup in soup_data:
            element = self.fetch_element(soup)
            if element:
                all_elements.extend(element)
        
        return all_elements
    
############################
# DOWNLOADING ELEMENT DATA #
############################

    def rerun_element_program(self, soup_data):
        #rerunning program if element data is None
        if soup_data is not None:
            element_data = self.extend_elements_via_soup_data(soup_data)

        if element_data and len(element_data) > 0:
            return element_data
        else:
            print('no elements found')
            return None

    def pickle_element_data(self, filename, element_data):
        #saves element_data via pickle.dump() 
        print('saving element path')

        file_path = os.path.join(directory, filename)

        with open(file_path, 'wb') as f:
            if element_data is not None:
                pickle.dump((element_data, time.time()), f)
            

    def load_element_data(self, filename, max_age):
        #loads element data via pickle.load() create data nd timestamp variables
        file_path = os.path.join(directory, filename)

        #if the file does not exist method returns None
        if not os.path.exists(file_path):
            print('file path does not exist')
            return None

        print('loading data')
        with open(file_path, 'rb') as f:
            element_data, timestamp = pickle.load(f)
        
        #method used from previous downloading functions
        age = self.age_variable(timestamp)
        print(f'age of element data - {age}')

        #if age limit is not yet reached, method will return element data
        #else it returns None
        if age <= max_age:
            print('age accepted')
            return element_data
        else:      
            print('age exceeded')  
            return None
    
    def verify_element_data_age(self, filename, max_age, soup_data):
        #loads element data
        element_data = self.load_element_data(filename, max_age)

        #if element data is None and the maximum retry limit is not reached then it will rerun the program and save it to a local file
        if element_data is None:
            print('data is None - reloading')
            element_data = self.rerun_element_program(soup_data)
            if element_data:
                self.pickle_element_data(filename, element_data)
        
        return element_data