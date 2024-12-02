__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu, kiun@uw.edu"
__version__ = "0.1.0"



import Impacts

class Defaultscenario:


    def __init__(self, name, data_folder):

        self.name = name
        self.alt_names = []
        self.data_folder = data_folder
        self.material_map = {}


    def get_distance(self, material):

        pass

    def get_mode(self, material):

    pass


    def get_distance(self, material):

    pass




class National(Defaultscenario):


    def __init__(self):

        self.name = "National"


class Reginal(Defaultscenario):


    def __init__(self):

        self.name = "Regional"


class Global(Defaultscenario):


    def __init__(self):

        self.name = "Global"