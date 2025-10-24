
__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..building import Material
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class EnvelopeMaterial(Material):
    """ Envelope material (contextual) that makes up assemblies in the building.
    
    Attributes
    ----------
    xxx : xxx
        xxx
    """
    def __init__(self):
        super().__init__()
    
if __name__ == '__main__':
    pass
