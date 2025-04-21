from lca_modules.material.master import Master
from lca_modules.eol import WASTE_PROCESS_DICT
from lca_modules.eol.waste_processing import WasteProcess
from utilities.objects.array_methods import get_attribute_as_list

from math import isnan


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
        self.waste_processes = []
        self.process_mix = {}
        self.impacts = {'C2':[], 'C3':[], 'C4':[]}

    def __str__(self):
        str = "="*50 + "\n" + f"Waste Product ({self.get_name()})\n" + "="*50 + "\n"
        str += f"Total qty: {self.get_qty()} {self.get_unit().get_standard_notation()}\n"
        str += "Process mix:\n"
        for process in self.get_waste_processes():
            mix_percent = self.get_process_mix()[process.get_process_name()]
            if isinstance(mix_percent, (float, int)):
                mix_percent = f"{mix_percent * 100:.2%f}\%"
            str += f"\t {process.get_process_name()} : {process.get_qty()} {process.get_unit().get_standard_notation()} ({mix_percent})\n"

        return str

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
        waste_item.set_name('Waste ' + database_item)
        waste_item.set_impact_database_entry(database_item)
        waste_item.set_qty(qty)
        waste_item.set_unit(unit)

        waste_item.set_waste_processess(process_mix)

        waste_item.update_impacts()

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
            process_mix : dict
                The mix of processes the waste product will be subject to: {process name (str): percentage (str or float)}.
                Percentage can be in the form of string with a % sign or decimal value. 
        """
        # TODO: remove dependence on WASTE_PROCESS_DICT and use the impact directory
        #       consider the possibility of having both C3 and C4 for the same mix component
        for waste_process_name in WASTE_PROCESS_DICT.keys():
            process_exist = True
            mix_percent_input = process_mix[waste_process_name]
            if isinstance(mix_percent_input, float) or isinstance(mix_percent_input, int):
                if isnan(mix_percent_input):
                    process_exist = False
                else:
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
                
                self.waste_processes.append(waste_process_obj)

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
            waste_processes : list of WasteProcess Obj.
                List of processes the waste will be subjected to. These processes are in parallel.
        """

        return self.waste_processes
    
    def get_process_mix(self):
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
        """ Update the transportation and processing impacts of the waste (C2-C4).
        """

        if self.get_waste_processes():

            impacts = self.get_impacts()
            for key in impacts.keys():
                impacts[key] = []

            for process in self.get_waste_processes():
                process_impact = process.get_unit_impacts() * process.get_qty()
                impacts[process.get_life_cycle_stage()].append(process_impact)

            # TODO: updating transportation ("C2" impacts)

        return self

    def update_process_mix(self, process_mix, overide=False):
        """ Update the waste process mix.
        
            Parameters
            ----------
            process_mix : dict
                The mix of processes the waste product will be subject to: {process name (str): percentage (str or float)}.
                Percentage can be in the form of string with a % sign or decimal value.
            overide : bool
                If true, allows any process to be added, if not only processes created in default are allowed.            
        
        """

        # check mix sum to 100%
        tol = 0.00001
        for key, value in process_mix.values():
            if isinstance(value, str):
                if value[-1] == "%":
                    process_mix[key] = float(value[:-1]) / 100

        sum =  sum(value for value in process_mix.values() if isinstance(value, (int, float)))
        if not abs(sum - 1) < tol:
            raise ValueError(f"Total of mix does not add upp to 100%. Value reached {sum*100}\%.")

        # check if unavailable proceses are in the mix.
        if not overide:
            available_processes = get_attribute_as_list(self.get_waste_processes(), 'process_name')
            for key, value in process_mix.items():
                if not (key in available_processes): # add only allowable processes.
                    raise KeyError(f"Waste process of {key} is not available for {self.get_name()}")

        for process in self.get_waste_processes():
            if process.get_process_name() in process_mix.keys():
                new_qty = self.get_qty() * process_mix[key]
            else:
                new_qty = 0.0
            process.set_qty(new_qty)

        # TODO: update transportation links

        self.update_impacts()

        return self
        
if __name__ == '__main__':
    pass
