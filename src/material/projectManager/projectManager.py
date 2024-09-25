from material.model.model import Model
from material.calculator.calcualtor import Calculator
from material.databaseManager.databaseManager import DatabaseManager
from material.visualizer.plotter import Plotter

import pickle

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class Project:
    """
    Project class which maintains the process models, impact database, and calculator.

    ...

    Attributes
    ----------
    name : str
        Name of the project.
    models : dict
        All models created/compared in the current project.
    current_model : Model Obj.
        Active model which is being worked on.
    database : Database Obj.
        Maintains input impact data.
    calculator : Calculator Obj.
        Carries out varies calculations to generate output data.
    """

    def __init__(self, name=None):
        self.name = name
        self.models = {'Model_0': Model(self, 'Model_0')}
        self.current_model = self.models['Model_0']
        self.database = DatabaseManager(self)
        self.calculator = Calculator(self)
        self.visulizer = Plotter(self)

    def __reduce__(self):
        
        return (self.__class__, (self.name,), {"model":self.current_model, "database": self.database,
                                               "models":self.models})
    
    def __setstate__(self, state):
        self.__dict__.update(state)

    def set_current_model(self, model_name):
        """ Set model as current model.
        
        Parameters:
        ----------
        model_name : str
            Name of the model to be set as the current model.
        """

        self.current_model = self.models[model_name]
    
    def get_current_model(self):

        return self.current_model
    
    def get_model(self, model_name):
        """ Retrieve model.
        
        Parameters:
        ----------
        model_name : str
            Name of the model to be retrieved.
        """

        return self.models[model_name]
    
    def get_database(self):

        return self.database
    
    def get_calculator(self):

        return self.calculator
    
    def get_impact_categories(self):

        return self.impact_categoreis
    
    def create_model(self, model_name):
        """ Create a model in the current project.

        Parameters:
        ----------
        model_name : str
            Name of the model to be created.        
        """

        model = Model(self, model_name)
        self.models[model_name] = model
    
    def clear_project(self, model=True, database=True):
        """ Remove all existing models adn the impact database of the project.
            An empty model (Model_0) is created and set as the current model.

        Parameters:
        ----------
        model : bool
            True if all the models are to be cleared.    
        database : bool
            True if the database is to be cleared.    
        """

        if model:
            self.models = {'Model_0': Model(self, 'Model_0')}
            self.current_model = self.models['Model_0']

        if database:
            self.database = DatabaseManager(self)

    def save(self, file_path):
        """ Save as a *.pkl file.

        Parameters:
        ----------
        file_path : str
            Location (including the name) where the data be saved.
        """

        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(file_path):
        """ Load a project from a pickled file.

        Parameters:
        ----------
        file_path : str
            Location (including the name) where the data be loaded from.
        """

        with open(file_path, 'rb') as file:
            project = pickle.load(file)

        return project

if __name__ == '__main__':
    pass