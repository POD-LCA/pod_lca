__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu, kiun@uw.edu"
__version__ = "0.1.0"


import Impacts
import Location

class Project_logestic_manager:


    def __init__(self, name= None):

        self.name = name
        self.link = []
        self.impacts = [Impacts(self)]
        self.location = Location(self)


    def get_impact(self):

        pass


    def create_links(self):

        pass






