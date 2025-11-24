
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from copy import deepcopy


class Scenario:

    def __init__(self):
        # project parametes
        self.location = None

        # transportation scenarios
        self.supply_chain = None
        self.mode = None
        self.efficiency = None

        # electricity scenarios
        self.decarbonization_scenario = None

        # construction scenarios


        # replacement scenarios


        # end of life scenarios


        # results
        self.results = None

    @classmethod
    def new(cls, building):

        scenario = cls()
        
        scenario.set_parameters(building)
        scenario.set_result()

        return scenario


    def set_parameters(self, building):
        # project parametes
        self.location = building.get_location().get_name()

        # transportation scenarios
        self.supply_chain = None
        self.mode = None
        self.efficiency = None

        # electricity scenarios
        self.decarbonization_scenario = self.get_operational_electricity_product().get_decarbonization_scenario()

        # construction scenarios


        # replacement scenarios


        # end of life scenarios


        return self
    
    def set_result(self):
        # TODO: what results to save... e.g., totals, grouped by, objects
        return self


if __name__ == '__main__':
    pass
