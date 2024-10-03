import pandas as pd
from bs4 import BeautifulSoup
from src.pickle_data import Pickle_Data
from src.eBay_elements import eBay_Elements
from src.download_products import Download_Products

dp = Download_Products()
P_DATA = dp.save_product_specifics() #backmarket product attributes (title, price)

ee = eBay_Elements()
E_DATA = ee.save_eBay_element_data() #eBay element data for price pulling

class eBay_Products:
    def __init__(self, e_data = E_DATA, p_data = P_DATA):
        '''Initializes the class with E_DATA, P_DATA
            
            args:
                E_DATA(list: eBay elements): Used to process attributes of a product ie. title and price
                P_DATA(list: Backmarket Products): will be extended to hold an average price of similar eBay products
            '''
        self.e_data = e_data
        self.p_data = p_data

#################################
# ATTACH PRODUCT ATTRIBUTES #
#################################

    def attribute_list(self):
        new_p_data = self.p_data[:] #p_data copy instance
        
        for i, item in enumerate(self.e_data): #for each in element_data and product_data - extend with an average instance
            average = item
            
            new_p_data[i] = (new_p_data[i], average)
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
        max_age = 3 #days
        function = self.attribute_function

        #sad = Save attribute data
        sad = Pickle_Data(filename, max_age, function)
        return sad.verify_data_age()