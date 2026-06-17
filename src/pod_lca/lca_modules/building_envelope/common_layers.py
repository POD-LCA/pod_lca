
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from .layer import Layer
from .layer import AncillaryMaterial
from ...units import Quantity
from ...units import KILOGRAM, INCH, SQUARE_FEET, FEET


class BrickLayer(Layer):

    def __init__(self):
        super().__init__()
        #FIXME: material property needed here instead of material name
        self.add_ancillary_material(Mortar("Type S Mortar"))

    def get_quantity(self, area=None, qty_in=None):
        if qty_in in ['volume', 'mass']:
            return 0.75 * super().get_quantity(area, qty_in)
        elif qty_in in ["area"]:
            return ValueError("Brick quantity cannot be computed in area.")
        else:
            raise ValueError("Quantity request not recognized.")


class SheathingLayer(Layer):

    def __init__(self):
        super().__init__()
        #FIXME: material property needed here instead of material name
        self.add_ancillary_material(Fastners("Fastners"))


class Mortar(AncillaryMaterial):

    def get_quantity(self, area=None, qty_in=None):
        if qty_in in ['volume', 'mass']:
            return (0.25 * self.parent.get_quantity(area, qty_in) + Quantity(0.75, INCH) * area) * 0.25 #  TODO Confirm the equation is correct
        elif qty_in in ["area"]:
            return ValueError("Brick quantity cannot be computed in area.")
        else:
            raise ValueError("Quantity request not recognized.")


class Fastners(AncillaryMaterial):

    def get_quantity(self, area=None, qty_in=None):
        return area * Quantity(1.18e-3, KILOGRAM)


class WoodStuds(AncillaryMaterial):

    def get_quantity(self, area=None, qty_in=None):
        if qty_in in ['volume', 'mass']:
            wall_area  = area.convert_to(SQUARE_FEET)
            framing = self.parent
            envelope = framing.parent.parent
            wall_height = envelope.floor_plan_obj.get_height().convert_to(FEET)
            spacing  = framing.spacing.convert_to(INCH)
            stud_width = framing.width.convert_to(INCH)
            stud_length= framing.length.convert_to(INCH)
            volume_per_ft2 = ((spacing*stud_width*stud_length*3+(10*12-3*stud_width)*stud_width*stud_length)/((spacing/12)*wall_height))/61023.7
            volume = volume_per_ft2 * wall_area
            return volume
        elif qty_in in ["area"]:
            raise ValueError('This material cant be measured in area')
        else:
            raise ValueError('This qty_in value is not supported')


class MetalStuds(AncillaryMaterial):

    def get_quantity(self, area=None, qty_in=None):
        raise ValueError('This studs type is not yet quantifiable')