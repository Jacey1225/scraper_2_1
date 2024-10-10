from src.download_backmarket_urls import Download_URLS as du
from src.download_url_elements import Download_Elements as de
from src.download_products import Download_Products as dp
from src.eBay_urls import eBay_URLS as eu
from src.eBay_elements import eBay_Elements as ee
from src.eBay_products import eBay_Products as ep
from src.database_conversion import Convert_Data as cd
from src.pickle_data import Pickle_Data as pd
from datetime import datetime
import time

TIME = "03:00:00"

class Run_Timestamp:
    def __init__(self, targettime: str = TIME):
        '''initializes class with a target time 
        args:
            targettime: represents the desired time the code be run for each day
        '''
        self.targettime = targettime
    
    def check_timestamp(self):
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")

            if current_time == self.targettime:
                self.fetch_all_datasets()

                time.sleep(24 * 60 * 60)
            
            else:
                time.sleep(1)
            
    def fetch_all_datasets(self):
        backmarket_urls = du.save_url_data()
        