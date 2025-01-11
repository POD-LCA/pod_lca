
from lca_modules.impacts.impacts_database import ImpactsDatabase
from lca_modules.material.model import Model

import pickle

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class Project:
    """
    Project class which maintains the process models, impact database, and calculator.

    Attributes
    ----------
    name : str
        Name of the project.
    models : dict
        All models created/compared in the current project.
    database : Database Obj.
        Maintains input impact data.
    """

    def __init__(self):
        self.name = None
        self.database = None
        self.models = {}

    def __str__(self):
        str = "="*75 + "\n" + f"Project: {self.get_name()}\n" + "="*75 + "\n"

        for model_name in self.get_model_names():
            str += f"{model_name} \n"

        return str

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, name=None):
        """ Create a new project.
        
        Parameters
        ----------
        name : str
            Name of the project.
        
        Returns
        -------
        Project Obj.
            Project created.
        """

        new_project = cls()

        new_project.set_name(name)

        return new_project
    
    # ================================
    # Setters and Getters
    # ================================
    def set_name(self, name:(str)):
        """ Set the name of the project.
        
        Parameters
        ----------
        name : str
            Name of the project.
        """

        self.name = name

        return self
    
    def set_database(self, database:(ImpactsDatabase)):
        """ Set the impacts database of the project.
        
        Parameters
        ----------
        database : Database Obj.
            Impact database of the project.
        """

        self.database = database

        return self
    
    def get_name(self):
        """ Retrieve the name of the project.
        
        Returns
        -------
        str
            Name of the project.
        """

        return self.name

    def get_database(self):
        """ Get the impacts database of the project.
        
        Retruns
        -------
        DatabaseManager Obj.
            Impact database of the project.
        """

        return self.database
    
    # ================================
    # Model Methods
    # ================================
    def add_model(self, model_name:(str), file_path=None):
        """ Create and add a model to the current project.

        Parameters
        ----------
        model_name : str
            Name of the model to be created.        
        """
        
        if file_path is None:
            model = Model.in_project(self, model_name)
        else:
            model = Model.from_CSV(file_path)
            model.set_parent(self)

        self.models[model_name] = model
        
        return model
    
    def get_model(self, model_name:(str)):
        """ Retrieve a model.
        
        Parameters
        ----------
        model_name : str
            Name of the model to be retrieved.

        Retruns
        -------
        Model Obj.
            Current working model.

        Raises
        ------
            KeyError : A model by such name does not exist in the current project.
        """

        if model_name in self.models:
            return self.models[model_name]
        else:
            raise KeyError(f"'{model_name}' does not exist in the current project.")
    
    def get_model_names(self):
        """ Get all names of all the models in the project.

        Retruns
        -------
        list of str.
            List of model names.

        """

        return list(self.models.keys())
    
    # ================================
    # Project Methods
    # ================================
    def clear_project(self, model=True, database=True):
        """ Remove all existing models and the impact database of the project.

        Parameters
        ----------
        model : bool
            True if all the models are to be cleared.    
        database : bool
            True if the database is to be cleared.    
        """

        if model:
            self.models = {}

        if database:
            self.database = None

    def save(self, file_path:(str)):
        """ Save as a *.pkl file.

        Parameters
        ----------
        file_path : str
            Location (including the name) where the data be saved.
        """
        
        with open(file_path, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(file_path:(str)):
        """ Load a project from a pickled file.

        Parameters
        ----------
        file_path : str
            Location (including the name) where the data be loaded from.

        Raises
        ------
            FileNotFoundError : File not found.
            PermissionError : Permission denied.
        """

        try:
            with open(file_path, 'rb') as file:
                project = pickle.load(file)
            return project
        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("Permission denied.")
        except Exception as e:
            print("An error occurred:", e)


if __name__ == '__main__':
    pass
