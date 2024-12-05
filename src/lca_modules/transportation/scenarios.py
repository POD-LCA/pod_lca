__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"


class DefaultScenario:
    
    def __init__(self, name):
        self.name = name
        self.scenario_impact = {}

    def compute_impact(self):
        raise NotImplementedError("compute_impact must be implemented in subclasses")

class Local(DefaultScenario):
    def __init__(self):
        super().__init__("Local")

class Regional(DefaultScenario):
    def __init__(self):
        super().__init__("Regional")

class RegionalC(DefaultScenario):
    def __init__(self):
        super().__init__("Regional_c")

class National(DefaultScenario):
    def __init__(self):
        super().__init__("National")