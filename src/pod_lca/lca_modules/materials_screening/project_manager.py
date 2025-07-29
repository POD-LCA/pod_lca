
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

import pickle

from . import Model
from ..impacts import ImpactsDatabase
from ..impacts import TranportationModeImpactsDatabase
from ...utilities import log
from ...utilities import config
from ...utilities import DataImporter


class Project:
    """ Project class which maintains the process models and a link to the impact database.

    Attributes
    ----------
    name : str
        Name of the project.
    models : dict
        All models created/compared in the current project.
    database : Database Obj.
        Maintains input impact data.
    location : Location Obj.
        Location of the project.
    """

    def __init__(self):
        self.name = None
        self.impact_database = None
        self.transport_mode_impact_database = None
        self.models = {}
        self.location = None

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
    
    def set_impact_database(self, database:(ImpactsDatabase)):
        """ Set the impacts database of the project.
    
        Parameters
        ----------
        database : ImpactsDatabase Obj or str
            Impact database object or if a string, filepath to the corresponding csv file containing impact data.
        """
        if isinstance(database, ImpactsDatabase):
            self.impact_database = database
        elif isinstance(database, str):
            impact_database = ImpactsDatabase.new("impact database")
            impact_database.set_data(database)
            self.set_impact_database(impact_database)
        else:
            raise TypeError("Database input not recognized")
        
    def set_transportation_mode_impact_database(self, database:(TranportationModeImpactsDatabase)):
        """ Set the impacts database for transportation impacts by mode.
    
        Parameters
        ----------
        database : ImpactsDatabase Obj or str
            Impact database object or if a string, filepath to the corresponding csv file containing impact data.
        """
        if isinstance(database, TranportationModeImpactsDatabase):
            self.transport_mode_impact_database = database
        elif isinstance(database, str):
            transport_impact_database = TranportationModeImpactsDatabase.new("impact database")
            transport_impact_database.set_data(database)
            self.set_transportation_mode_impact_database(transport_impact_database)
        else:
            raise TypeError("Database input not recognized")
    
    def set_location(self, location):
        """ Set the location of the project.
        
            Parameters
            ----------
            location : Location Obj.
                Location of the project.
        """
        self.location = location

        return self

    def get_name(self):
        """ Retrieve the name of the project.
        
        Returns
        -------
        str
            Name of the project.
        """
        return self.name

    def get_impact_database(self):
        """ Get the impacts database of the project.
        
        Returns
        -------
        DatabaseManager Obj.
            Impact database of the project.
        """
        return self.impact_database

    def get_transportation_mode_impact_database(self):
        """ Get the impacts database of the project.
        
        Returns
        -------
        DatabaseManager Obj.
            Impact database of the tranportation modes.
        """
        return self.transport_mode_impact_database
    
    def get_location(self):
        """ Retrieve the location of the project.
        
            Returns
            -------
            Location Obj.
                Location of the project.
        """
        return self.location
    
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
            self.models[model_name] = model
        else:
            model = Model.from_CSV(file_path, self, model_name)

        return model
    
    def get_model(self, model_name:(str)):
        """ Retrieve a model.
        
        Parameters
        ----------
        model_name : str
            Name of the model to be retrieved.

        Returns
        -------
        Model Obj.
            Current working model.

        Raises
        ------
        KeyError
            A model by such name does not exist in the current project.
        """
        if model_name in self.models:
            return self.models[model_name]
        else:
            raise KeyError(f"'{model_name}' does not exist in the current project.")
    
    def get_model_names(self):
        """ Get all names of all the models in the project.

        Returns
        -------
        list of str
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
            self.impact_database = None

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
        FileNotFoundError
            File not found.
        PermissionError
            Permission denied to access file.
        """
        try:
            with open(file_path, 'rb') as file:
                project = pickle.load(file)
            return project
        except FileNotFoundError:
            log("File not found.", "Error")
        except PermissionError:
            log("Permission denied.", "Error")
        except Exception as e:
            log("An error occurred:" + e, "Error")


    # ================================
    # Calcualotror Methods
    # ================================
    def get_impacts_by_LCstages_models(self, impact_category, model_lst=None):
        """ Returns impact data by life cycle stage for given multiple model and impact category.
            
        Parameters
        ----------
        impact_category : str
            Name of the Impact category.
        model_lst : List of str
            List of the names of models.

        Returns
        -------
        dict
            Impacts dictionary where {model_name (str): { stage (str): quantity of impact (float)}}.
        """
        if model_lst is None:
            model_lst = self.get_model_names()

        data ={}
        for model_name in model_lst:
            model = self.get_model(model_name)
            data[model.get_name()] = model.get_impacts_by_LCstages(impact_category)
        
        return data

    def get_impacts_by_category_models(self, model_lst=None):
        """ Returns impact data by impact category for given multiple models.
            
        Parameters
        ----------
        model_lst : List of str
            List of the names of models.

        Returns
        -------
        dict
            Impacts dictionary where {model_name (str): {impact_category (str) : quantity of impact (float)}}.
        """
        if model_lst is None:
            model_lst = self.get_model_names()
        
        data ={}
        for model_name in model_lst:
            model = self.get_model(model_name)
            data[model_name] = {}
            for impact_category in config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES'].keys():
                data[model_name][impact_category] = sum(model.get_impacts_by_LCstages(impact_category).values())
        
        return data

    def get_normalized_impacts_by_category_models(self, model_lst=None):
        """ Returns impact data by impact category for given multiple models.
            
        Parameters
        ----------
        model_lst : List of str
            List of the names of models.

        Returns
        -------
        dict
            Impacts dictionary where {model_name (str): {impact_category (str) : quantity of impact (float)}}.
        """
        if model_lst is None:
            model_lst = self.get_model_names()

        IMPACT_NORMALIZATION_FACTOR = DataImporter.json_to_dict(config["file_paths"]["IMPACT_NORMALIZATION_FACTOR"])
        data ={}
        for model_name in model_lst:
            model = self.get_model(model_name)
            data[model_name] = {}
            for impact_category in config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES'].keys():
                data[model_name][impact_category] = sum(model.get_impacts_by_LCstages(impact_category).values()) * IMPACT_NORMALIZATION_FACTOR[impact_category]
        
        return data

    def get_impacts_by_LCstages_models_items(self, impact_category, model_lst=None):
        """ Returns impact data by life cycle stage for given multiple model and impact category, with impacts 
            identifieable by individaul item.
            
        Parameters
        ----------
        impact_category : str
            Name of the Impact category.
        model_lst : List of str
            List of the names of models.

        Returns
        -------
        dict
            Impacts dictionary where {model_name (str): {stage (str): {item_name (str): quantity of impact (float)}}.
        """
        if model_lst is None:
            model_lst = self.get_model_names()

        data ={}
        for model_name in model_lst:
            model = self.get_model(model_name)
            model_data = {}
            impacts_dict = model.get_impacts()
            for stage in impacts_dict.keys():
                stage_data = {}
                impact_lst = impacts_dict[stage]
                for impact in impact_lst:
                    stage_data[impact.get_parent().get_name()] = impact.get_record(impact_category)
                model_data[stage] = stage_data
            data[model_name] = model_data

        return data

    def get_impacts_by_LCstages_models_hotspots(self, impact_category, model_lst=None):

        pass # TODO implement
    
    def get_impacts_by_impactcategorys_models_LCstage(self, impact_categories,  model_lst=None):
        """ Returns data for a barchart.
            
        Parameters
        ----------
        impact_categories : List of str
            List of impact categories.
        model_lst : List of str
            List of the names of models.

        Returns
        -------
        dict
            Impacts dictionary where {model_name (str): {impact_category (str): {stage (str): quantity of impact (float)}}.
        """
        if model_lst is None:
            model_lst = self.get_model_names()

        data = {model_name: {} for model_name in model_lst}
        for impact_category in impact_categories:
            for model_name in model_lst:
                model = self.get_model(model_name)
                data[model_name][impact_category] = model.get_impacts_by_LCstages(impact_category)
        
        return data
    

if __name__ == '__main__':
    pass
