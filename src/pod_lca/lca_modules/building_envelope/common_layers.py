
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from .material_property import EnvelopeMaterialPropertyMass
from .framing import Framing
from .layer import Layer
from .layer import AncillaryMaterial
from ...units import Quantity
from ...units import KILOGRAM, INCH, SQUARE_FEET, FEET, CUBIC_METER
from ...utilities import config
from ...utilities import DataImporter


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

    def __init__(self, material_property=None):
        if material_property is None:
            material_property = EnvelopeMaterialPropertyMass()
            material_property.name = "Steel plate, fabricated"
        super().__init__(material_property)

    def get_quantity(self, area=None, qty_in=None):
        if isinstance(self.parent, SheathingLayer): 
            area_in_ft2 = area.convert_to(SQUARE_FEET)
            return Quantity(1.18e-3, KILOGRAM) * area_in_ft2.value
        elif isinstance(self.parent, Framing): 
            area_in_ft2 = area.convert_to(SQUARE_FEET)
            if isinstance(self.parent.anciallary_materials[0], WoodStuds): # FIXME: not a robust tests---requires studs to be added first in the framing
                return Quantity(6.33e-3, KILOGRAM) * area_in_ft2.value
            elif isinstance(self.parent.anciallary_materials[0], MetalStuds): # FIXME: not a robust tests---requires studs to be added first in the framing
                return Quantity(7.05e-3, KILOGRAM) * area_in_ft2.value
        else:
            raise ValueError("Parent layer not recognized to be using fastners.")


class WoodStuds(AncillaryMaterial):

    def get_quantity(self, area=None, qty_in=None):
        if qty_in in ['volume', 'mass']:
            framing = self.parent
            envelope = framing.parent.parent

            wall_area  = area.convert_to(SQUARE_FEET)
            wall_height = envelope.floor_plan_obj.get_height().convert_to(FEET).value
            spacing  = framing.spacing.convert_to(INCH).value
            stud_width = framing.width.convert_to(INCH).value
            stud_length= framing.length.convert_to(INCH).value

            volume_per_ft2 = ((spacing * stud_width * stud_length * 3 + (10 * 12 - 3 * stud_width) * stud_width * stud_length) / ((spacing / 12) * wall_height)) / 61023.7
            volume = Quantity(volume_per_ft2, CUBIC_METER) * wall_area.value
            return volume
        elif qty_in in ["area"]:
            raise ValueError('This material cant be measured in area')
        else:
            raise ValueError('This qty_in value is not supported')


class MetalStuds(AncillaryMaterial):

    def get_quantity(self, area=None, qty_in=None):
        if qty_in in ['volume', 'mass']:
            wall_area  = area.convert_to(SQUARE_FEET)
            framing = self.parent
            envelope = framing.parent.parent

            wall_height = envelope.floor_plan_obj.get_height().convert_to(FEET).value
            spacing  = framing.spacing.convert_to(INCH).value
            
            stud_design_table = DataImporter.csv_to_pandas(config['file_paths']['building']['STEEL_STUD_DESIGN_TABLE'])
            A_stud = stud_design_table.loc[stud_design_table['Section'] == framing.section_id, 'Stud_Area'].values[0]
            A_track = stud_design_table.loc[stud_design_table['Section'] == framing.section_id, 'Track_Area'].values[0]

            volume_per_ft2 = (spacing * A_stud * 3 + (wall_height * 12 * A_track)) / ((spacing / 12) * wall_height) / 61023.7
            volume = Quantity(volume_per_ft2, CUBIC_METER) * wall_area.value
            return volume
        elif qty_in in ["area"]:
            raise ValueError('This material cant be measured in area')
        else:
            raise ValueError('This qty_in value is not supported')