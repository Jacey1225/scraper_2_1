import pickle
import os


PICKLE_FOLDER = os.path.join('/Users/jaceysimpson/Vscode/scraper_2_1', "pickles")

directory = os.path.abspath(PICKLE_FOLDER)
if not os.path.exists(directory):
    os.makedirs(directory)

class Save_Data:
    def __init__(self, filename, function):
        '''initializes class with filename and function
        args: 
            filename: contains the name holding specific data
            function: contains the function for executing a program to fetch the desired data
        '''
        self.filename = filename
        self.function = function
    
    def pickle_data(self, data):
        file_path = os.path.join(directory, self.filename)

        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
    
    def load_data(self):
        file_path = os.path.join(directory, self.filename)

        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        
        return data
    
    def fetch_data(self):
        data = self.load_data()

        if data is None:
            data = self.function()
            self.pickle_data(data)
        
        return data