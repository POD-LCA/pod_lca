
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

import csv
import gc
import os

from . import Electricity
from . import Emission
from . import Fuel
from . import Process
from . import Product
from . import TransportationProcess
from . import Waste
from pod_lca.units import UNITS_MAP
from pod_lca.units import KILO 
from pod_lca.units import WATT_HOUR 


class Model:
    """ Model object is the canvas to which the processes and prodcuts are added. 
        The corresponding calculations are based on models.

    Attributes
    ----------
    project : Project Obj.
        Project on which the calculator operates.
    name : str
        Name of the model.
    processes : list of Process Obj.
        Processes in the model.
    products : list of Product Obj.
        Products in the model.
    impacts : dict
        Impact objects categorized by life cycle stage {life cycle stage (str): list of Impacts Obj.}
    """

    def __init__(self):
        self.project = None
        self.name = None
        self.processes = []
        self.products = []
        self.impacts = {'A1':[], 'A2':[], 'A3':[]}
        self.emissions = {'A1':[], 'A2':[], 'A3':[]}
        self.carbon_storage = {'A1':[], 'A2':[], 'A3':[]}

    def __str__(self):
        str = "="*75 + "\n" + f"Product/Process List of {self.get_name()}\n" + "="*75 + "\n"
        for item in self.get_products() + self.get_processes():
            name_tag = f"{item.get_name()} ({type(item).__name__})"
            if len(name_tag) > 50:
                formated_name_tag = f"{name_tag[:{47}]}..."
            else:
                formated_name_tag = f"{name_tag:<50}" 

            str += f"{formated_name_tag:<50} {item.get_life_cycle_stage():<10} {item.get_qty():<5} {item.get_unit().get_standard_notation():<20}\n"

        return str        

    # ================================
    # Constructors
    # ================================
    @classmethod
    def in_project(cls, project, name=None):    
        """ Create a model object from a parent object.
        
        Parameters
        ----------
        project : Project Obj.
            Project to which the model belong.
        name : str.
            Name of the model.
        
        Returns
        -------
        Model Obj.
            Model object created.
        """
        model = cls()
        
        model.set_project(project)
        if name is not None:
            model.set_name(name)
        else:
            model.set_name(f"Model_{len(project.models)}")

        return model
    
    @classmethod
    def from_CSV(cls, file_path, project, name=None):
        """ Create a model from data in a csv file.
            The csv file with headers: "Name", "Impact data", "type", "LC stage", "qty", "unit", "transported item", "density", "weight unit" (in any order).
            Transported item is the name of the product transported.
            Quantity in the transportation process should be the distance.

        Parameters
        ----------
        file_path : str
            Location of the csv file.
        name : str
            Name of the model to be created.   
        project : Project Obj.
            Project to which the model belong.    
        """        
        model = cls()

        model.set_project(project)

        if name is not None:
            model.set_name(name)
        else:
            model.set_name(os.path.splitext(os.path.basename(file_path))[0])

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
                    item = model.add_product(name, life_cycle_stage, qty, UNITS_MAP[unit], database_item)
                elif item_type == 'Process':
                    item = model.add_process(name, life_cycle_stage, qty, UNITS_MAP[unit], database_item)
                elif item_type == 'Transportation':
                    item = model.add_transportation_process(name, life_cycle_stage, qty, UNITS_MAP[unit], database_item)
                elif item_type == 'Energy':
                    item = model.add_energy(name, life_cycle_stage, qty, UNITS_MAP[unit], database_item)
                elif item_type == 'Electricity':
                    item = model.add_electricity(name, life_cycle_stage, qty, UNITS_MAP[unit])
                elif item_type == 'Emission':
                    item = model.add_emission(name, life_cycle_stage, qty, UNITS_MAP[unit], database_item)
                elif item_type == 'Waste':
                    item = model.add_waste(name, life_cycle_stage, qty, UNITS_MAP[unit], database_item)                    
                else:
                    raise TypeError(f"Item type of {item_type} is undefined.")

                if item_type == 'Transportation':
                    transported_item = row[header_map['transported item']]
                    transported_product = model.find_item(transported_item) # TODO: create functionality for multiple transported items
                    if not (transported_product is None):
                        item.set_transported_products(transported_product)
                    else:
                        if not (transported_item == ''):
                            if transported_item in tmp_transportation_map:
                                tmp_transportation_map[transported_item]['transporter'].append(item)
                            else:
                                tmp_transportation_map[transported_item] = {}
                                tmp_transportation_map[transported_item]['transporter'] = [item]
                else:
                    if not (row[header_map['density']] == ''):
                        item.set_density(row[header_map['density']])        
                    if not (row[header_map['weight unit']] == ''):
                        item.set_weight_unit(UNITS_MAP[row[header_map['weight unit']]])  

                    if name in tmp_transportation_map:
                        tmp_transportation_map[name]['product'] = item
        
        if tmp_transportation_map:
            for entry in tmp_transportation_map:
                tmp_transportation_map[entry]['transporter'].set_transported_product(tmp_transportation_map[entry]['product'])
                
        return model    
    
    # ================================
    # Setters and Getters
    # ================================
    def set_project(self, project):
        """ Set the project object.
        
        Parameters
        ----------
        project : Project Obj.
            Project to which the model belong.
        """
        self.project = project

        return self
    
    def set_name(self, name):
        """ Set the name of the model.
        
        Parameters
        ----------
        name : str.
            Name of the model.
        """
        self.name = name

        return self
    
    def get_project(self):
        """ Retrieve the project object.
        
        Returns
        -------
        Project Obj.
            Project to which the model belong.
        """
        return self.project
    
    def get_name(self):
        """ Retrieve the name of the model.
        
        Returns
        -------
        str.
            Name of the model.
        """
        return self.name

    def get_processes(self):
        """ Retrieve all the processes in the model.

            Returns
            -------
            list of Process Obj.
                All processes in the model.
        """
        return self.processes
    
    def get_products(self):
        """ Retrieve all the products in the model.

            Returns
            -------
            list of Product Obj.
                All products in the model.
        """
        return self.products
    
    def get_all_items(self):
        """ Retrieve all the products and processes in the model.
        
            Returns
            -------
            list of Master Obj.
                All products and processess in the model.

        """
        return self.get_products() + self.get_processes()

    def get_impacts(self):
        """ Retrieve all the impacts in the model categorized by life cycle stage.

            Returns
            -------
            dict.
                Impact objects categorized by life cycle stage {life cycle stage (str): list of Impacts Obj.}
        """
        for item in self.get_all_items():
            item.update_inventory_records()

        return self.impacts
    
    def get_emissions(self):
        """ Retrieve all the emissions in the model categorized by life cycle stage.

            Returns
            -------
            dict.
                Emission objects categorized by life cycle stage {life cycle stage (str): list of Emissions Obj.}
        """
        return self.emissions
    
    def get_carbon_storage(self):
        """ Retrieve all the carbon storage in the model categorized by life cycle stage.

            Returns
            -------
            dict.
                Carbon storage objects categorized by life cycle stage {life cycle stage (str): list of Carbon Storage Obj.}
        """
        return self.carbon_storage
            
    # ================================
    # Methods to add items to the model
    # ================================
    def add_process(self, name, stage, qty, unit, impacts_from):
        """ Create and add process to the model.

        Parameters
        ----------
        name : str.
            Name of the process.
        stage : str.
            Life cycle stage.
        qty : float
            Quantity processed.
        unit : Unit Obj
            Unit of the quantity.
        impacts_from : str
            Name of the impact database entry from which to use impacts.

        Returns
        -------
        Process Obj.
            Process object created.
        """
        n = len(self.get_processes())
        process = Process.new(n, name, self, stage, qty, unit, impacts_from)

        process.set_qty(qty)
        process.set_unit(unit)
        
        self.processes.append(process)
        
        return process
    
    def add_transportation_process(self, name, stage, transported_distance, unit, impacts_from):
        """ Create and add process to the model.

        Parameters
        ----------
        name : str.
            Name of the process.
        stage : str.
            Life cycle stage.
        qty : float
            Quantity processed.
        unit : Unit Obj
            Unit of the quantity.
        impacts_from : str
            Name of the impact database entry from which to use impacts.

        Returns
        -------
        Process Obj.
            Process object created.
        """
        n = len(self.get_processes()) 
        process = TransportationProcess.new(n, name, self, stage, transported_distance, unit, impacts_from)

        self.processes.append(process)
        
        return process
    
    def add_product(self, name, stage, qty, unit, impacts_from):
        """ Create and add product to the model.

        Parameters
        ----------
        name : str.
            Name of the product.
        stage : str.
            Life cycle stage.
        qty : float
            Product quantity.
        unit : Unit Obj.
            Unit of measurement.            
        impacts_from : str
            Name of the impact database entry from which to use impacts.

        Returns
        -------
        Product Obj.
            Product object created.
        """
        n = len(self.get_products())
        product = Product.new(n, name, self, stage, qty, unit, impacts_from)

        self.products.append(product)
        
        return product
    
    def add_energy(self, name, stage, qty, unit, impacts_from):
        """ Create and add energy product to the model.

        Parameters
        ----------
        name : str.
            Name of the product.
        stage : str.
            Life cycle stage: 'A1', 'A2', 'A3'.
        qty : float
            Product quantity.
        unit : Unit Obj.
            Unit of measurement.
        impacts_from : str
            Name of the impact database entry from which to use impacts.

        Returns
        -------
        Product Obj.
            Energy product object created.
        """
        n = len(self.get_products())
        energy = Fuel.new(n, name, self, stage, qty, unit, impacts_from)

        self.products.append(energy)
        
        return energy
    
    def add_electricity(self, name, stage, qty, unit=KILO * WATT_HOUR):
        """ Create and add electricity product to the model.

        Parameters
        ----------
        name : str.
            Name of the product.
        stage : str.
            Life cycle stage: 'A1', 'A2', 'A3'.
        qty : float
            Product quantity.
        unit : Unit Obj.
            Unit of measurement.
    
        Returns
        -------
        Product Obj.
            Electricity object created.
        """
        n = len(self.get_products())
        electricity = Electricity.new(n, name, self, stage, qty, unit)
        
        self.products.append(electricity)
        
        return electricity
    
    def add_emission(self, name, stage, qty, unit, impacts_from):
        """ Create and add emission product to the model.

        Parameters
        ----------
        name : str.
            Name of the emission product.
        stage : str.
            Life cycle stage: 'A1', 'A2', 'A3'.
        qty : float
            Product quantity.
        unit : Unit Obj.
            Unit of measurement.   
        impacts_from : str
            Name of the impact database entry from which to use impacts.

        Returns
        -------
        Product Obj.
            Emission object created.
        """
        n = len(self.get_products())
        emission = Emission.new(n, name, self, stage, qty, unit, impacts_from)

        self.products.append(emission)
        
        return emission

    def add_waste(self, name, stage, qty, unit, impacts_from):
        """ Create and add waste product to the model.

        Parameters
        ----------
        name : str.
            Name of the waste product.
        stage : str.
            Life cycle stage: 'A1', 'A2', 'A3'.
        qty : float
            Product quantity.
        unit : Unit Obj.
            Unit of measurement.   
        impacts_from : str
            Name of the impact database entry from which to use impacts.

        Returns
        -------
        Product Obj.
            Waste object created.
        """
        n = len(self.get_products())
        waste = Waste.new(n, name, self, stage, qty, unit, impacts_from)

        self.products.append(waste)

        return waste   

    # ================================
    # Methods to interact with items
    # ================================
    def find_item(self, name):
        """ Find an item (product/process) in the model, given a name string.
            If multiple objects of the same name exist, returns all.
        
        Parameters
        ----------
        name : str.
            Product/Process name searched for.

        Returns
        -------
        Master Obj.
            Product / Process object
        """
        items = [item for item in self.get_products() + self.get_processes() if item.get_name() == name]

        if len(items) == 0:
            return None
        else:
            return items 
    
    def delete_item(self, obj):
        """ Removes products or processes, along with the impact objects, from the model.

            Parameters
            ----------
            obj : Master Obj.
                Product or process to be removed from the model.
        """
        if type(obj) == Product:
            self.get_products().remove(obj)
            for process in self.get_processes():
                if type(process) is TransportationProcess:
                    if obj in process.get_transported_products():
                        process.get_transported_products().remove(obj)
                        process.set_transported_weight()
        elif type(obj) == Process:
            self.get_processes().remove(obj)
            
        obj.remove_inventory_records_from_model(obj.get_life_cycle_stage())

        del obj

        gc.collect()


if __name__ == '__main__':
    pass
