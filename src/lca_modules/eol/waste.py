from lca_modules.material.master import Master
from lca_modules.impacts.impacts import Impacts
from lca_modules.eol import WASTE_PROCESS_DICT
from lca_modules.impacts.impact_categories import IMPACT_CATEGOREIS

import gc


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class Waste(Master):
    """ Waste product handling the end-of-life or product. This inherit from the material.Master object.
    
        Attributes
        ----------
        parent : BuildingComponent Obj. or Master Obj.
            The thing that which was converted to waste.
        waste_processes : list of WasteProcess Obj.
            List of processes the waste will be subjected to. These processes are in parallel.
        process_mix : dict
            The mix of processes the waste product will be subject to: {process name (str): percentage (str or float)}.
            Percentage can be in the form of string with a % sign or decimal value.              
        impacts : dict.
            Impact objects categorized by life cycle stage {life cycle stage (str): list of Impacts Obj.}
    """
    def __init__(self):
        super().__init__()
        self.parent = None
        self.is_waste = True
        self.waste_processess = []
        self.process_mix = {}
        self.impacts = {'C2':[], 'C3':[], 'C4':[], 'D':[]}

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, parent, database_item, qty, unit, process_mix):
        """ Create new waste product.
        
            Parameters
            ----------
            parent : BuildingComponent Obj. or Master Obj.
                The thing that which was converted to waste.
            database_item : str
                Material name corresponding to the database entry which gives the unit impact of the product.
            qty : float
                Quantity of the product/process.
            unit : Unit Obj
                Unit of measurement corresponding to the quantity of the product/process.
            process_mix : dict
                The mix of processes the waste product will be subject to: {process name (str): percentage (str or float)}.
                Percentage can be in the form of string with a % sign or decimal value.        
        """

        waste_item = cls()

        waste_item.set_parent(parent)
        waste_item.set_name('Waste' + database_item)
        waste_item.set_impact_database_entry(database_item)
        waste_item.set_qty(qty)
        waste_item.set_unit(unit)

        waste_item.set_waste_processess(process_mix)

        return waste_item

    # ================================
    # Setters
    # ================================  
    def set_parent(self, parent):
        """ Set parent of the waste product.
        
            Parameters
            ----------
            parent : BuildingComponent Obj. or Master Obj.
                The thing that which was converted to waste.
        """
        self.parent = parent

        return self

    def set_waste_processess(self, process_mix=None):
        """ Set waste processe for the waste product. Also sets the process mix.

            Parameters
            ----------
            waste_processes : list of WasteProcess Obj.
                List of processes the waste will be subjected to. These processes are in parallel.
        """
        
        process_exist = True
        for waste_process_name in WASTE_PROCESS_DICT.keys():
            mix_percent_input = process_mix[waste_process_name]
            if isinstance(mix_percent_input, float) or isinstance(mix_percent_input, int):
                mix_percent = mix_percent_input
            elif isinstance(mix_percent_input, str):
                if mix_percent_input in ['NA', 'N/A']:
                    process_exist = False
                if mix_percent_input[-1] == "%":
                    mix_percent = float(mix_percent_input[:-1]) / 100.0
                else:
                    mix_percent = float(mix_percent_input)
            else:
                raise TypeError(f"mix percentages are of unrecognized type. Must be float, int, or string.")
            
            if process_exist:
                process_qty = self.get_qty() * mix_percent

                waste_process_obj = WasteProcess.new(self, 
                                                     waste_process_name, 
                                                     process_qty, 
                                                     self.get_unit(), 
                                                     WASTE_PROCESS_DICT[waste_process_name])
                
                self.waste_processess.append(waste_process_obj)
        
        self.process_mix = process_mix

        return self

    # ================================
    # Getters
    # ================================
    def get_parent(self):
        """ Get parent of the waste product.
        
            Returns
            -------
            BuildingComponent Obj. or Master Obj.
                The thing that which was converted to waste.
        """
        return self.parent
    
    def get_waste_processes(self):
        """ Get waste processe for the waste product.

            Returns
            -------
            process_mix : dict
                The mix of processes the waste product will be subject to: {process name (str): percentage (str or float)}.
                Percentage can be in the form of string with a % sign or decimal value. 
        """

        return self.waste_processess
    
    def get_mix(self):
        """ Get the mix of process the waste product is subjected to.
        
            Returns
            -------
            process_mix : dict
                The mix of processes the waste product will be subject to: {process name (str): percentage (str or float)}.
                Percentage can be in the form of string with a % sign or decimal value.       
        """
        return self.process_mix

    # ================================
    # Methods
    # ================================
    def update_impacts(self):
        
        if self.get_waste_processes():
            pass # TODO write this method

    def update_mix(self, mix):

        pass # TODO write method


class WasteProcess:


    def __init__(self):
        self.parent = None
        self.process_name = None
        self.qty = 0.0
        self.unit = None
        self.life_cycle_stage = None
        self.unit_impacts = Impacts.from_parent(self)
        self.location = None
        self.transportation_link = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, parent, process_name, qty, unit, life_cycle_stage):

        waste_process = cls()

        waste_process.set_parent(parent)
        waste_process.set_process_name(process_name)
        waste_process.set_qty(qty)
        waste_process.set_unit(unit)
        waste_process.set_life_cycle_stage(life_cycle_stage)

        #TODO: create transportaton links

        return waste_process

    # ================================
    # Setters
    # ================================    
    def set_parent(self, parent):
        """ Set parent Waste object of the Waste Processing.
        
            Parameters
            ----------
            parent : Waste Obj.
                Waste object for which the waste processing belong.
        """
        self.parent = parent

        return parent
    
    def set_process_name(self, name):
        """ Set the process name.

            Parameters
            ----------
            name : str
                Name of the process: e.g., 'Landfill', 'Recycle', 'Compost'

        """
        self.process_name = name

        self.set_unit_impacts()
        
        return self

    def set_unit_impacts(self):

        material = self.get_parent().get_impact_database_entry()
        process = self.get_process_name()
        database = self.get_parent().get_parent().get_building().get_eol_database()

        database_entry = database.get_data_entry(material, process)
        impacts = {key: database_entry[key] for key in IMPACT_CATEGOREIS}

        self.get_unit_impacts().update_impact_qty(impacts)

        
    def set_qty(self, qty):

        self.qty = qty

        self.get_parent().update_impacts() # TODO: update impacts of the parent

    def set_unit(self, unit):
        """ Set unit of measurement for the waste amount processed.
        
            Parameters
            ----------
            unit : Unit Obj.
                Unit of measurement.
        """

        if self.get_unit() is None:
            self.unit = unit
        else:
            value_in = self.get_qty()
            unit_in = self.get_unit()

            conversion_factor = unit_in.get_conversion_factor(unit)

            if conversion_factor is not None:
                self.unit = unit
                self.set_qty(value_in * conversion_factor)
            else:
                raise ValueError(f"The new unit ({unit}) is incompatible with the existing unit ({unit_in}).")

        return self

    def set_life_cycle_stage(self, life_cycle_stage):
        """ Set life cycle stage of the product/process.

            Parameters
            ----------
            life_cycle_stage : str
                Life cycle stage of the product/process.
        """

        if self.get_life_cycle_stage() is None:
            self.life_cycle_stage = life_cycle_stage
        else:
            previous_stage = self.get_life_cycle_stage()
            self.life_cycle_stage = life_cycle_stage
            
            impact_obj = self.get_impacts()
            parent_impacts_list = self.get_parent().get_impacts()[previous_stage]
            for impact in parent_impacts_list:
                if impact == impact_obj:
                    parent_impacts_list.remove(impact_obj)
                    break

            self.get_parent().get_impacts()[life_cycle_stage].append(impact_obj)

        return self

    def set_location(self, location):

        self.location = location
        
        # TODO: update the transportation

    # ================================
    # Getters
    # ================================
    def get_parent(self):
        """ Get parent Waste object of the Waste Processing.
        
            Returns
            -------
            Waste Obj.
                Waste object for which the waste processing belong.
        """

        return self.parent
    
    def get_unit(self):
        """ Get unit of measurement for the waste amount processed.
        
            Returns
            -------
            unit : Unit Obj.
                Unit of measurement.
        """        

        return self.unit
    
    def get_life_cycle_stage(self):
        """ Retrieve the life cycle stage corresponding to the waste process.

            Returns
            -------
            str
                Corresponding life cycle stage.

        """

        return self.life_cycle_stage

    def get_process_name(self):
        """ Get the process name.

            Returns
            -------
            str
                Name of the process: e.g., 'Landfill', 'Recycle', 'Compost'

        """       
        return self.process_name
    
    def get_unit_impacts(self):

        return self.unit_impacts


if __name__ == '__main__':
    pass
