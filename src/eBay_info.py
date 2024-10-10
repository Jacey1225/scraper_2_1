import pandas as pd
from bs4 import BeautifulSoup

class eBay_Info:
    def __init__(self, elements, soup):
        '''initializes class with elements
        
        args:
            elements: a list of product info within a url of eBay >> will be used to extract specific info such as price average and product popularity(how many sold in the past few months)
            '''
        self.elements = elements
        self.soup = BeautifulSoup(soup, "html.parser")
    
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

    def fetch_average(self):
        price_list = [] #find all prices within an element/page
        for item in self.elements:
            price = self.get_price(item) 
            price_list.append(price)
        
        prices = pd.Series(price_list) #convert the list of prices to a pandas dataset
        average = prices.mean() #get the average of the dataset
        return average.round(2) #return and round to the nearest 100th

########################
# EXTRACT SELLING FEES #
########################

    def get_selling_fees(self, average):
        selling_fee = 0.15 #ebay selling fee for electronic devices
        price_difference = average * selling_fee #get the amount as a subtractable integer 
        final_price = average - price_difference #subtract difference from the selling amount

        return final_price

####################
# FETCH POPULARITY #
####################

    def fetch_popularity(self):
        #fetch info on how popular a given item is on eBay eg >> 4,600+ results for iPhone X
        pop_element = self.soup.find('h1', class_='srp-controls__count-heading') #html search command 
        pop = pop_element.get_text() #String variable
        if pop is not None:
            return pop