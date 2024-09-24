from src.download_backmarket_urls import Download_URLS
from src.pickle_data import Pickle_Data
from bs4 import BeautifulSoup
import pickle
import requests 
import time
import os

du = Download_URLS()
DATA = du.save_url_data()


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
    def soup_function(self):
        #runs the program again if the result of soup_data is None
        soup_data = self.fetch_soup_via_content()
        if soup_data:
            return soup_data

    def save_soup_data(self):
        filename = 'backmarket_soup_data'
        max_age = 3 #days
        function = self.soup_function

        #ssd == save soup data
        ssd = Pickle_Data(filename, max_age, function)
        return ssd.verify_data_age()

########################### 
# RETRIEVING ELEMENT DATA #
########################### 

    def fetch_element(self, soup):
        #finds all content containing the same parent calss
        soup = BeautifulSoup(soup, 'html.parser')
        raw_elements = soup.find_all('a', class_='shadow-short rounded-lg relative block no-underline motion-safe:transition motion-safe:duration-200 motion-safe:ease-in bg-float-default-low focus-visible-outline-default-hi cursor-pointer hover:bg-float-default-low-hover hover:shadow-long h-full overflow-hidden text-left')
        
        #converts raw elements to a text list for serializable data
        element_data = [{'text': a.get_text(strip = True)} for a in raw_elements]
        
        return element_data

    def extend_elements_via_soup_data(self, soup_data):
        #uses the soup_data to gather all data from all urls and make element searches via self.fetch_element()
        all_elements = []

        #loops through soup data to find elements
        for soup in soup_data:
            if soup is not None:
                element = self.fetch_element(soup)
                if element:
                    all_elements.extend(element)
        
        return all_elements
    
############################
# DOWNLOADING ELEMENT DATA #
############################

    def element_function(self, soup_data):
        #rerunning program if element data is None
        element_data = None

        #if there is valid data in soup_data...create an instance of element_data
        if soup_data is not None:
            element_data = self.extend_elements_via_soup_data(soup_data)

        #if not None...return data
        if element_data and len(element_data) > 0:
            return element_data
        else:
            print('no elements found')
            return None

    def save_element_data(self):
        #using Pickle_Data...locally save data to a file path(filename)
        filename = 'backmarket_element_data'
        max_age = 3 # days

        soup_data = self.save_soup_data()
        if soup_data is not None:
            function = lambda: self.element_function(soup_data)
        
            #using variables from above create a class instance and call the function
            sed = Pickle_Data(filename, max_age, function)
            return sed.verify_data_age()

    