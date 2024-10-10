import pandas as pd
from bs4 import BeautifulSoup
from src.save_data import Save_Data
from src.eBay_elements import eBay_Elements
from src.download_products import Download_Products
from src.eBay_urls import eBay_URLS

dp = Download_Products()
P_DATA = dp.save_product_data() #backmarket product attributes (title, price)

ee = eBay_Elements()
E_DATA = ee.save_eBay_element_data() #eBay element data for price pulling

class eBay_Products:
    def __init__(self, e_data = E_DATA, p_data = P_DATA):
        '''Initializes the class with E_DATA, P_DATA
            
            args:
                E_DATA(list: eBay elements): Used to process attributes of a product ie. title and price
                P_DATA(list: Backmarket Products): will be extended to hold an average price of similar eBay products
                U_DATA(list: Backmarket Product Links): will be extended to hold a redirect link of the buy product
            '''
        self.e_data = e_data
        self.p_data = p_data

#################################
# ATTACH PRODUCT ATTRIBUTES #
#################################

    def attribute_list(self):
        new_p_data = self.p_data[:] #p_data copy instance [(title, price)]
        
        for i, item in enumerate(self.e_data): #for each in element_data and product_data - extend a copy of product_data with an average instance [(title, price, average)]            
            new_p_data[i] = (new_p_data[i], item)
            if new_p_data[i]:
                print(f'new item: {new_p_data[i]}')
        
        return new_p_data

###########################
# SAVE PRODUCT ATTRBIUTES #
###########################
    def attribute_function(self):
        new_p_data = self.attribute_list()
        if new_p_data is not None:
            return new_p_data

    def save_attributes_data(self):
        filename = 'all_product_data'
        function = self.attribute_function

        #ad == attribute data
        ad = Save_Data(filename, function)
        return ad.fetch_data()