from src.eBay_products import eBay_Products
from pymongo import MongoClient

ep = eBay_Products()
P_DATA = ep.save_attributes_data() #list of product data ((title, price), average)

class Convert_Data:
    def __init__(self, data = P_DATA):
        '''Initializes class with data(P_DATA)
        args:
            P_DATA(all product data as title, buying price, and selling price): Used to convert list into a mongo database
              '''

        self.data = data
    
    def connect_mongo(self):
        client = MongoClient('mongodb://localhost:27017')
        db = client['eBay_product_database']
        collection = db['eBay_collection']

        return collection

    def transform_collection(self):
        collection = self.connect_mongo()

        data_dicts = [
            {
                "title": item[0][0],
                "buying price": item[0][1],
                "selling price": item[1]
            }
            for item in self.data
        ]

        return collection.insert_many(data_dicts)