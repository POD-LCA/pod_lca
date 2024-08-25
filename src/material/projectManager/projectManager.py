from material.model.model import Model
from material.calculator.calcualtor import Calculator
from material.databaseManager.databaseManager import DatabaseManager

class Project:

    def __init__(self):
        self.model = Model(self)
        self.database = DatabaseManager(self)
        self.calculator = Calculator(self)

    def get_model(self):

        return self.model
    
    def get_database(self):

        return self.database
    
    def get_calculator(self):

        return self.calculator
    
