
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from .layer import Layer
from .layer import AncillaryMaterial
from ...units import Quantity
from ...units import KILOGRAM


class BrickLayer(Layer):

    def __init__(self):
        super().__init__()
        self.add_ancillary_material(Mortar("Type S Mortar"))

    def get_quantity(self, area=None, qty_in=None):
        return 0.75 * super().get_quantity()


class Mortar(AncillaryMaterial):

    def get_quantity(self, area=None, qty_in=None):
        return 0.25 * self.parent.get_quantity(area, qty_in)
    

class SheathingLayer(Layer):

    def __init__(self):
        super().__init__()
        self.add_ancillary_material(Fastners("Fastners"))


class Fastners(AncillaryMaterial):

    def get_quantity(self, area=None, qty_in=None):
        return area * Quantity(1.18e-3, KILOGRAM)
