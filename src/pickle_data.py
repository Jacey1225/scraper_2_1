import pickle
import time
import os

#global variable; path directory
PICKLE_FOLDER = os.path.join('/Users/jaceysimpson/Vscode/scraper_2_1', "pickles")
directory = os.path.abspath(PICKLE_FOLDER)
if not os.path.exists(directory):
    os.makedirs(directory)

class Pickle_Data:
    def __init__(self, filename, max_age, function):
        '''Initializes the class with filename, max_age, function
        
        args:
            filename: the path in which data will be locally stored
            max_age: the age limit that data may remain stored in a file
            
        '''
        self.filename = filename
        self.max_age = max_age
        self.function = function

    def pickle_data(self, data):
        #saving data via pickle.dump()
        print(f'saving data {self.filename}')
        file_path = os.path.join(directory, self.filename)

        #with open as writing 
        with open(file_path, 'wb') as f:
            pickle.dump((data, time.time()), f)
    
    def age_variable(self, timestamp):
        #creating an age instance to track the last time the code was ran
        seconds = time.time() - timestamp
        age = seconds / (60 * 60 * 24)
        return age
    
    def load_data(self):
        #loads data via pickle.load() - with open as read
        print(f'loading data {self.filename}')
        file_path = os.path.join(directory, self.filename)

        #if the file does not exists return None
        if not os.path.exists(file_path):
            print('path does not exist...loading function')
            return None
        
        with open(file_path, 'rb') as f:
            #create two variables of data and a timestamp to store the last runtime
            data, timestamp = pickle.load(f)

        age = self.age_variable(timestamp)
        print(f'age of {self.filename} - {age}')

        #if the age limit is not yet exceeded, return data...else return None
        if age <= self.max_age:
            print('age accepted')
            return data
        else:
            print('age exceeded')
            return None

    def verify_data_age(self):
        data = self.load_data()

        if data is None:
            print(f'loading function for {self.filename}')
            data = self.function()
            self.pickle_data(data)
        
        return data
    