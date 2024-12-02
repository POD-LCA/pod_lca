__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu, kiun@uw.edu"
__version__ = "0.1.0"



import Defaultscenario

class Logisticslink:


    def __init__(self, material, qty, travel_dist, return_travel_dist, disy_unit):

        self.material = material
        self.qty = qty
        self.travel_dist = travel_dist
        self.return_travel_dist = return_travel_dist
        self.disy_unit = disy_unit


    def compute_impact(self):

        pass

