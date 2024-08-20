from POD_LCA_MATERIAL.model.model import Model
from POD_LCA_MATERIAL.calculator.calcualtor import Calculator
from POD_LCA_MATERIAL.databaseManager.databaseManager import DatabaseManager

class Project:

    def __init__(self):
        self.model = Model()
        self.database = DatabaseManager()
        self.calculator = Calculator()
