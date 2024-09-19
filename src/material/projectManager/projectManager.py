from material.model.model import Model
from material.calculator.calcualtor import Calculator
from material.databaseManager.databaseManager import DatabaseManager

import pickle

class Project:

    def __init__(self, name=None):
        self.name = name
        self.model = Model(self)
        self.models = {}
        self.database = DatabaseManager(self)
        self.calculator = Calculator(self)
    
    def __reduce__(self):
        
        return (self.__class__, (self.name,), {"model":self.model, "database": self.database})
    
    def __setstate__(self, state):
        self.__dict__.update(state)
    
    def get_model(self):

        return self.model
    
    def get_database(self):

        return self.database
    
    def get_calculator(self):

        return self.calculator
    
    def get_impact_categories(self):

        return self.impact_categoreis
    
    def create_model(self, name):

        model = Model(name)
        self.models[name] = model
    
    def clear_project(self, model=True, database=True):

        if model:
            self.model = Model(self)

        if database:
            self.database = DatabaseManager(self)

    def save(self, file_path):

        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(file_path):
        with open(file_path, 'rb') as file:
            project = pickle.load(file)

        return project