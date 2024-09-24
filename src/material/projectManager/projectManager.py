from material.model.model import Model
from material.calculator.calcualtor import Calculator
from material.databaseManager.databaseManager import DatabaseManager

import pickle

class Project:

    def __init__(self, name=None):
        self.name = name
        self.models = {'Model_0': Model(self, 'Model_0')}
        self.current_model = self.models['Model_0']
        self.database = DatabaseManager(self)
        self.calculator = Calculator(self)
    
    def __reduce__(self):
        
        return (self.__class__, (self.name,), {"model":self.current_model, "database": self.database,
                                               "models":self.models})
    
    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_current_model(self, name):

        self.current_model = self.models[name]
    
    def get_current_model(self):

        return self.current_model
    
    def get_model(self, model_name):

        return self.models[model_name]
    
    def get_database(self):

        return self.database
    
    def get_calculator(self):

        return self.calculator
    
    def get_impact_categories(self):

        return self.impact_categoreis
    
    def create_model(self, name):

        model = Model(self, name)
        self.models[name] = model
    
    def clear_project(self, model=True, database=True):

        if model:
            self.models = {'Model_0': Model(self, 'Model_0')}
            self.current_model = self.models['Model_0']

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