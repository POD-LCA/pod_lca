__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu, kiun@uw.edu"
__version__ = "0.1.0"


import Impacts

class Trasportmode:


    def __init__(self, name):

        self.name = name
        self.impacts = Impacts(self)
        self.limitations = []


    def check_limitations(self):

        pass