import pickle
import time
import os

PICKLE_FOLDER = os.path.join('/Users/jaceysimpson/Vscode/scraper_2_1', "pickles")
directory = os.path.abspath(PICKLE_FOLDER)
if not os.path.exists(directory):
    os.makedirs(directory)

class Pickle_Data:
    def __init__(self, filename, max_age, function):
        '''Initializes the class with DATA
        
        args:
            filename: the path in which data will be locally stored
            max_age: the age limit that data may remain stored in a file
            
        '''
        self.filename = filename
        self.max_age = max_age
        self.function = function

    def pickle_data(self, data):
        file_path = os.path.join(directory, self.filename)

        with open(file_path, 'wb') as f:
            pickle.dump((data, time.time()), f)
    
    def age_variable(self, timestamp):
        seconds = time.time() - timestamp
        age = seconds / (60 * 60 * 24)
        return age
    
    def load_data(self):
        file_path = os.path.join(directory, self.filename)

        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'rb') as f:
            data, timestamp = pickle.load(f)

        age = self.age_variable(timestamp)

        if age <= self.max_age:
            return data
        else:
            return None

    def verify_data_age(self):
        data = self.load_data()

        if data is None:
            data = self.function()
            self.pickle_data(data)
        
        return data
    