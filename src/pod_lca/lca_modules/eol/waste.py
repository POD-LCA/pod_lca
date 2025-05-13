
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from math import isnan

from . import WasteProcess
from ..material_screening import Master
from ...utilities import ArrayMethods
from ...utilities import config
from ...utilities import log


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
    bio_based : bool
        True if the material is bio-based.          
    """

    def __init__(self):
        super().__init__()
        self.parent = None
        self.is_waste = True
        self.waste_processes = []
        self.process_mix = {}
        self.impacts = {'C2':[], 'C3':[], 'C4':[], 'D':[]}
        self.emissions = {'C2':[], 'C3':[], 'C4':[], 'D':[]}
        self.bio_based = True

    def __str__(self):
        str = "="*50 + "\n" + f"Waste Product ({self.get_name()})\n" + "="*50 + "\n"
        str += f"Total qty: {self.get_qty()} {self.get_unit().get_standard_notation()}\n"
        str += "Process mix:\n"
        for process in self.get_waste_processes():
            if not process.get_linked_process(to=False):
                mix_percent = self.get_process_mix()[process.get_process_name()]
                if isinstance(mix_percent, (float, int)):
                    mix_percent = f"{mix_percent * 100:.2%f}\%"
                str += f"\t {process.get_process_name()} : {process.get_qty()} {process.get_unit().get_standard_notation()} ({mix_percent})\n"

        return str

    # ================================
    # Constructors
    # ================================
    @classmethod
    def new(cls, parent, database_item, qty, unit, process_mix, bio_based=None):
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
        bio_based : bool
            True if the material is bio-based.       
        """
        waste_item = cls()

        waste_item.set_parent(parent)
        waste_item.set_name('Waste ' + database_item)
        waste_item.set_bio_based(bio_based)
        waste_item.set_impact_database_entry(database_item)
        waste_item.set_qty(qty)
        waste_item.set_unit(unit)

        waste_item.set_waste_processess(process_mix)

        waste_item.update_inventory_records()

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

    def set_impact_database_entry(self, database_item:str):
        """ Sets the database (impacts) entry corresponding to the item.
            This method will also update the corresponding impact quanitities.
        
        Parameters
        ----------
        database_item : str.
            The name of the database item which gives the item impacts.
        """
        database = self.get_parent().get_building().get_eol_database()
        row_id = database.data.index[(database.data[database.get_primary_key()] == database_item)]
        if len(row_id) == 0:
            if self.get_bio_based():
                database_item = config['setup']['eol']['EOL_DEFAULT_KEY'] + '_BIOBASED'
            else:
                database_item = config['setup']['eol']['EOL_DEFAULT_KEY'] + '_OTHER'

        self.impact_database_entry = database_item
        self.update_inventory_records()

        return self
        
    def set_waste_processess(self, process_mix=None):
        """ Set waste processe for the waste product. Also sets the process mix.

        Parameters
        ----------
        process_mix : dict
            The mix of processes the waste product will be subject to: {process name (str): percentage (str or float)}.
            Percentage can be in the form of string with a % sign or decimal value. 
        """
        waste_process_dict = config['setup']['eol']['WASTE_PROCESS_STAGES']
        if Waste.check_mix_sum(process_mix):
            for waste_process_name in waste_process_dict.keys():
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

                    lc_stage = waste_process_dict[waste_process_name]
                    linked_process = False
                    if isinstance(lc_stage, list):
                        lc_stage = waste_process_dict[waste_process_name][0]
                        linked_process = True

                    waste_process_obj = WasteProcess.new(self, 
                                                        waste_process_name, 
                                                        process_qty, 
                                                        self.get_unit(), 
                                                        lc_stage)
                    
                    self.waste_processes.append(waste_process_obj)
                    
                    if linked_process:
                        for lc_stage in waste_process_dict[waste_process_name][1:]:
                            try:
                                linked_from = waste_process_obj
                                waste_process_obj = WasteProcess.new(self, 
                                                                    waste_process_name, 
                                                                    process_qty, 
                                                                    self.get_unit(), 
                                                                    lc_stage)
                                linked_from.set_linked_process(waste_process_obj)

                                self.waste_processes.append(waste_process_obj)
                            except ImportError as e:
                                log(e, "Error")

            
            self.process_mix = process_mix

            return self
        
    def set_bio_based(self, is_bio_based):
        """ Set the bio-based nature of the material.
        
        Parameters
        ----------
        is_bio_based : bool
            True, if the material is bio-based.
        """
        if is_bio_based is None:
            self.bio_based = False
        else:
            self.bio_based = is_bio_based

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

    def get_bio_based(self):
        """ Get the bio-based nature of the material.
        
        Returns
        -------
        bool
            True, if the material is bio-based.
        """
        return self.bio_based

    # ================================
    # Methods
    # ================================
    def update_inventory_records(self):
        """ Update the transportation and processing impacts of the waste (C2-C4).
        """
        if self.get_waste_processes():

            impacts = self.get_impacts()
            for key in impacts.keys():
                impacts[key] = []

            emissions = self.get_emissions()
            for key in emissions.keys():
                emissions[key] = []

            for process in self.get_waste_processes():
                process_impact = process.get_unit_impacts() * process.get_qty()
                process_emission = process.get_unit_emissions() * process.get_qty()
                impacts[process.get_life_cycle_stage()].append(process_impact)
                emissions[process.get_life_cycle_stage()].append(process_emission)

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
        if Waste.check_mix_sum(process_mix):
            # check if unavailable proceses are in the mix.
            if not overide:
                available_processes = ArrayMethods.get_attribute_as_list(self.get_waste_processes(), 'process_name')
                for key, value in process_mix.items():
                    if not (key in available_processes): # add only allowable processes.
                        raise KeyError(f"Waste process of {key} is not available for {self.get_name()}")

            for process in self.get_waste_processes():
                if process.get_process_name() in process_mix.keys():
                    if process.get_linked_process(to=False) is None:
                        new_qty = self.get_qty() * process_mix[key]
                else:
                    new_qty = 0.0
                process.set_qty(new_qty)

            # TODO: update transportation links

            self.update_inventory_records()

            return self
    
    @staticmethod
    def check_mix_sum(process_mix, tol=0.00001):
        """ check if the process mix adds up to 100%.
        
        Parameters
        ----------
        process_mix : dict
            The mix of processes the waste product will be subject to: {process name (str): percentage (str or float)}.
            Percentage can be in the form of string with a % sign or decimal value.  
        tol : float
            Tolerence checked against

        Returns
        -------
        bool
            True if the sum of the mix percentages adds upto a 100%, within tolerence.
        """
        sum = 0.0
        for key, value in process_mix.items():
            if isinstance(value, str):
                if value[-1] == "%":
                    value = float(value[:-1]) / 100
            elif isnan(value):
                value = 0.0
            sum += value

        if abs(sum - 1) < tol:
            return True
        else:
            raise ValueError(f"Total of mix does not add upp to 100%. Value reached {sum*100}\%.")
        
        
if __name__ == '__main__':
    pass
