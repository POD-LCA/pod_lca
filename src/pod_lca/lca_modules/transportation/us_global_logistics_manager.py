
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from ..transportation import CFSDataset
from ..transportation import DomesticLink
from ..transportation import ForeignLink
from ..transportation import LogisticLink
from ..transportation import ProjectLogisticManager
from ...units import KILOMETER


class USGlobalLogisticProject(ProjectLogisticManager):
    """ A project in US uding domestic logistic.
    """

    def __init__(self):
        super().__init__()
        self.dataset = None
