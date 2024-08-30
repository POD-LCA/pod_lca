from material.model.model import Model
from material.calculator.calcualtor import Calculator
from material.databaseManager.databaseManager import DatabaseManager

import pickle

class Project:

    def __init__(self):
        self.name = None
        self.model = Model(self)
        self.database = DatabaseManager(self)
        self.calculator = Calculator(self)
    
    def __reduce__(self):
        
        return (self.__class__, (None), {"project": self.project, "processes":self.processes, 
                                         "products": self.products, "impacts": self.impacts})
    
    def __setstate__(self, state):
        self.__dict__.update(state)
    
    def get_model(self):

        return self.model
    
    def get_database(self):

        return self.database
    
    def get_calculator(self):

        return self.calculator
    
    def save(self, file_path):

        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(file_path):
        with open(file_path, 'rb') as file:
            project = pickle.load(file)

        return project