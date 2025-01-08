
from lca_modules.material.calculator import Calculator
from lca_modules.impacts.impacts_database import ImpactsDatabase
from lca_modules.material.model import Model

import csv
import pickle

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
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
        self.database = ImpactsDatabase()
        self.calculator = Calculator(self)
        self.HotSpotAnalysis = None
        self.DataQualityAnalysis = None

    def __reduce__(self):
        
        return (self.__class__, (self.name,), {"current_model":self.current_model, "database": self.database,
                                               "models":self.models})
    
    def __setstate__(self, state):
        self.__dict__.update(state)

    # =

    def set_current_model(self, model_name:(str)):
        """ Set model as current model.
        
        Parameters
        ----------
        model_name : str
            Name of the model to be set as the current model.
        """

        self.current_model = self.models[model_name]
    
    def get_current_model(self):
        """ Get the current model.
        
        Retruns
        -------
        Model Obj.
            Current working model.
        """

        return self.current_model
    
    def get_model(self, model_name:(str)):
        """ Retrieve model.
        
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
 
    def get_database(self):
        """ Get the impacts database of the project.
        
        Retruns
        -------
        DatabaseManager Obj.
            Impact database of the project.
        """

        return self.database
    
    def get_calculator(self):
        """ Get the calculator of the project.
        
        Retruns
        -------
        Calculator Obj.
            Calculator of the project.
        """

        return self.calculator
    
    def create_model(self, model_name:(str)):
        """ Create a model in the current project.

        Parameters
        ----------
        model_name : str
            Name of the model to be created.        
        """

        model = Model(self, model_name)
        self.models[model_name] = model

        return model
    
    def create_model_from_csv(self, file_path, model_name:(str)):
        """ Create a model from data in a csv file.
            The csv file with headers: "Name", "Impact data", "type", "LC stage", "qty", "unit", "transported item", "density", "weight unit" (in any order).
            Transported item is the name of the product transported.
            Quantity in the transportation process should be the distance.

        Parameters
        ----------
        file_path : str
            Location of the csv file.
        model_name : str
            Name of the model to be created.       
        """        

        model = self.create_model(model_name)

        tmp_transportation_map = {}
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            data = csv.reader(file)
            headers = next(data)
            header_map = {header:index for index, header in enumerate(headers)} 
            for row in data:
                name = row[header_map['Name']]
                life_cycle_stage = row[header_map['LC stage']]
                database_item = row[header_map['Impact data']]
                qty, unit = row[header_map['qty']], row[header_map['unit']]
                
                item_type = row[header_map['type']]
                if item_type == 'Product':
                    item = model.create_product(name, life_cycle_stage)
                elif item_type == 'Process':
                    item = model.create_process(name, life_cycle_stage)
                elif item_type == 'Transportation':
                    item = model.create_transportation_process(name, life_cycle_stage)
                elif item_type == 'Energy':
                    item = model.create_energy(name, life_cycle_stage)
                elif item_type == 'Emission':
                    item = model.create_emission(name, life_cycle_stage)
                elif item_type == 'Waste':
                    item = model.create_waste(name, life_cycle_stage)                    
                else:
                    raise TypeError(f"Item type of {item_type} is undefined.")

                if item_type == 'Transportation':
                    item.set_transported_distance_unit(unit)
                    item.set_transported_distance(qty)

                    transported_item = row[header_map['transported item']]
                    transported_product = model.find_item(transported_item) # TODO: create functionality for multiple transported items
                    if not (transported_product is None):
                        item.set_transported_products(transported_product)
                    else:
                        if not (transported_item == ''):
                            tmp_transportation_map[transported_item] = {}
                            tmp_transportation_map[transported_item]['transporter'] = item
                else:
                    item.set_unit(unit)
                    item.update_qty(qty)
                    density = row[header_map['density']]
                    weight_unit = row[header_map['weight unit']]
                    if not (density == ''):
                        item.set_density(density)        
                    if not (weight_unit == ''):
                        item.set_weight_unit(weight_unit)  

                    if name in tmp_transportation_map:
                        tmp_transportation_map[name]['product'] = item

                if not (database_item == ''):
                    item.set_impact_database_entry(database_item)
        
        if tmp_transportation_map:
            for entry in tmp_transportation_map:
                tmp_transportation_map[entry]['transporter'].set_transported_product(tmp_transportation_map[entry]['product'])
                
        return model
    
    def clear_project(self, model=True, database=True):
        """ Remove all existing models adn the impact database of the project.
            An empty model (Model_0) is created and set as the current model.

        Parameters
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
            self.database = ImpactsDatabase(self)

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
