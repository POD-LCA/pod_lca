from lca_modules.material.master import Master
from lca_modules.impacts.impacts import Impacts

class Waste(Master):

    def __init__(self):
        super().__init__()
        self.is_waste = True
        self.waste_processess = []
        self.impacts = {'C2':[], 'C3':[], 'C4':[], 'D':[]}

    @classmethod
    def new(cls, database_item=None, eol_mix=None):


        waste_item = cls()

        waste_item.set_database_entry(database_item, eol_mix.keys())

    def set_database_entry(self, database_entry_name, waste_processes):

        pass
        #TODO: create and set Waste Processing objects/ create transportaton links

    def set_mix(self, mix):

        pass

    def get_mix():

        pass # TODO calculate from the quantitites


    def update_impacts(self):
        
        pass


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


    @classmethod
    def new(cls, parent, name, qty, unit, life_cycle_stage):

        #TODO: passing the impact database entry

        waste_process = cls()

        waste_process.set_parent()
        waste_process.set_process_name()
        waste_process.set_qty()
        waste_process.set_unit()
        waste_process.set_life_cycle_stage()

        return waste_process
    
    def set_parent(self, parent):
        """ Set parent Waste objec of the Waste Processing.
        
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

        pass
        # TODO set unit impacts using self
        
    def set_qty(self, qty):

        self.qty = qty

        self.update_impacts # TODO: update impacts of the parent

    def set_unit(self, unit):

        pass 
        # TODO: unit conversion and update qty

    def set_life_cycle_stage(self, life_cycle_stage):

        pass
        # TODO: update at Building/Component and Waste levels

    def set_location(self, location):

        self.location = location
        
        # TODO: update the transportation



    

