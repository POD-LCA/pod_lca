
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import BuildingStructure


class ConcreteStructure(BuildingStructure):
    """ Concrete structure from first principles."""

    def __init__(self):
        super().__init__()


    def build(self):
        """Built Concrete Structure from first principles.
        """
        pass # TODO: To be implemented


if __name__ == '__main__':
    pass    
            