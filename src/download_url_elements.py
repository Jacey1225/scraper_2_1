from src.download_backmarket_urls import Download_URLS
from src.save_data import Save_Data
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
                soup_list.append(str(soup))
        
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
        function = self.soup_function

        #ssd == soup data
        sd = Save_Data(filename, function)
        soup_data = sd.fetch_data()
        return soup_data

########################### 
# RETRIEVING ELEMENT DATA #
########################### 

    def serialize_elements(self, raw_elements):
        #converts raw elements to a text list for serializable data
        element_data = [] #stores serializeable element data
        for element in raw_elements:
            element_text = element.get_text()
            if element_text:
                element_data.append(element_text)
        
        return element_data
    
    def fetch_element(self, soup):
        #finds all content containing the same parent class
        #soup = BeautifulSoup(soup, 'html.parser')
        soup = BeautifulSoup(soup, 'html.parser')
        raw_elements = soup.find_all('a', class_='shadow-short rounded-lg relative block no-underline motion-safe:transition motion-safe:duration-200 motion-safe:ease-in bg-float-default-low focus-visible-outline-default-hi cursor-pointer hover:bg-float-default-low-hover hover:shadow-long h-full overflow-hidden text-left')
        
        #calls serialize_elements() to properly pickle data
        element_data = self.serialize_elements(raw_elements)
        
        return element_data

    def extend_elements_via_soup_data(self, soup_data):
        #uses the soup_data to gather all data from all urls and make element searches via self.fetch_element()
        all_elements = []

        #loops through soup data to find elements
        for soup in soup_data:
            if soup is not None:
                element = self.fetch_element(soup)
                if element:
                    all_elements.append(element)
        
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

        soup_data = self.save_soup_data()
        function = lambda: self.element_function(soup_data)
        
        #using variables from above create a class instance and call the function
        ed = Save_Data(filename, function)
        element_data = ed.fetch_data()

        return element_data

    