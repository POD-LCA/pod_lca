__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import numpy as np
from bisect import bisect_left

from .common_layers import WoodStuds
from ...units import Quantity as Q
from ...units import INCH
from ...units import KELVIN
from ...units import METER
from ...units import MILI
from ...units import WATT
from ...utilities import config
from ...utilities import DataImporter


class Framing(object):
    """ Framing object representing the structural elements in envelope
    walls. Designed to compute thermal bridges (not structural properties). 
    
    Attributes
    ----------
    name : str
        The name of the framing instance. 
    type : str
        Type of framing (Metal, Wood)
    member : str
        Framing member name. 
    spacing : ~pod_lca.units.Quantity
        The spacing between framing members. 
    """

    def __init__(self):
        self.name                 = None
        self.__type__             = None
        self.material_property    = None
        self.spacing              = None
        self.width                = None
        self.length               = None
        self.parent               = None
        self.anciallary_materials = []

    def set_parent(self, parent):
        self.parent = parent

    def add_ancillary_material(self, ancillary_mat):
        """Add an ancillary material to the layer.
        """
        self.anciallary_materials.append(ancillary_mat)
        ancillary_mat.parent = self

class WoodFraming(Framing):

    def __init__(self):
        super().__init__()
        self.__type__           = 'Wood'

    @classmethod
    def from_parameters(cls, name, material_property, spacing, width, length):
        framing = cls()
        framing.name                = name
        framing.material_property   = material_property
        framing.spacing             = spacing
        framing.width               = width
        framing.length              = length
        framing.add_ancillary_material(WoodStuds(material_property))
        #TODO: add nails, etc...
        return framing

    def compute_bridge(self, Ra, Rb, rins, **kwargs):
        """Computes the updated R and U given the thermal bridging
        caused by wooden framing, using the parallel path method. 

        Parameters
        ----------
        Ra : ~pod_lca.units.Quantity
            Assembly thermal resistance (exluding interior finish)

        Rb : ~pod_lca.units.Quantity
            Interior finish thermal resistance

        rins : ~pod_lca.units.Quantity
            Framing insulation resistivity
        """

        conductivity = self.material_property.conductivity

        COND_TO_RIMP = 0.144
        # --------------------------
        # 1. Framing fraction
        # --------------------------
        # Fraction of wall area occupied by studs:
        f_stud = self.width / self.spacing
        f_stud = min(max(f_stud, 0.01), 0.30)   # keep reasonable bounds
        f_ins = 1 - f_stud

        # --------------------------
        # 2. Compute R-values
        # --------------------------

        # Cavity insulation:
        R_cavity = rins * self.length

        # Wood stud resistance:
        # R = (1/k)*0.144 × thickness (in)
        R_wood_stud = (1 / conductivity) * COND_TO_RIMP * self.length

        # --------------------------
        # 3. Framing path
        # --------------------------
        R_stud_path = Ra + R_wood_stud + Rb

        # --------------------------
        # 4. Insulated path
        # --------------------------
        R_insulated_path = Ra + R_cavity + Rb

        # --------------------------
        # 5. Overall assembly by parallel method
        # --------------------------
        u = f_stud * (1 / R_stud_path) + f_ins * (1 / R_insulated_path)
        r = 1 / u

        return r, u

    def get_ancillary_materials(self):
        return self.anciallary_materials


class MetalFraming(Framing):

    def __init__(self):
        super().__init__()
        self.__type__           = 'Metal'
        self.metal_thickness    = None

    @classmethod
    def from_parameters(cls, name, material_property, spacing, metal_thickness=None, width=None, length=None, section_id=None): # TODO: Keep both defined width/length/thickness or defined section options or only the latter...?
        framing = cls()
        framing.name                = name
        framing.material_property   = material_property
        framing.spacing             = spacing
        framing.metal_thickness     = metal_thickness
        framing.width               = width
        framing.length              = length
        framing.section_id          = section_id
        if section_id:
            stud_design_table = DataImporter.csv_to_pandas(config['file_paths']['building']['STEEL_STUD_DESIGN_TABLE'])
            framing.width           = Q(stud_design_table.loc[stud_design_table['Section'] == framing.section_id, 'width (in)'].values[0], INCH)
            framing.length          = Q(stud_design_table.loc[stud_design_table['Section'] == framing.section_id, 'depth (in)'].values[0], INCH)
            framing.metal_thickness = Q(stud_design_table.loc[stud_design_table['Section'] == framing.section_id, 'thickness (mm)'].values[0], MILI * METER)

        return framing

    def compute_bridge(self, Ra, Rb, rins, **kwargs):
        """Computes the updated R and U given the thermal bridging
        caused by metal framing. 

        Parameters
        ----------
        Ra : ~pod_lca.units.Quantity
            Assembly thermal resistance (exluding interior finish)

        Rb : ~pod_lca.units.Quantity
            Interior finish thermal resistance

        rins : ~pod_lca.units.Quantity
            Framing insulation resistivity
            

        Returns
        -------
        r : ~pod_lca.units.Quantity
            Thermal resiastance of the assembly including the thermal bridge. 

        u : ~pod_lca.units.Quantity
            Thermal conductance of the assembly including the thermal bridge.  

        """


        # -------------------------------
        # Metal resistivity constant
        # -------------------------------
        conductivity = self.material_property.conductivity
        resistivity = 1.0 / conductivity
        

        # -------------------------------
        # Geometry
        # -------------------------------

        dist_between_flanges = self.length - (2 * self.metal_thickness)
        if dist_between_flanges < 0:
            raise ValueError("Metal stud too thick: dI < 0.")

        sheathing_thickness = kwargs['di']
        ratio = kwargs['ratio']
        zf = self.get_zf(ratio)
        W = self.width + (zf * sheathing_thickness)


        # 3. Resistances

        dIxri = rins * dist_between_flanges
        dIIxri = rins * self.metal_thickness
        dIxrmet = resistivity * dist_between_flanges
        dIIxrmet = resistivity * self.metal_thickness

        # 4. Web & flange resistance
        RI = (dIxrmet * dIxri * W / (dist_between_flanges * (dIIxri - dIIxrmet) + W * dIxrmet)).convert_to((METER * METER * KELVIN) / WATT)
        RII = (dIIxrmet * dIIxri * W / (self.width * (dIIxri - dIIxrmet) + W * dIIxrmet)).convert_to((METER * METER * KELVIN) / WATT)

        # 5. Summations
        sum_Rcav = Ra + Rb + dIxri + 2.0 * dIIxri
        sum_RW = Ra + Rb + RI + 2.0 * RII


        r = Q((sum_RW.value * sum_Rcav.value * self.spacing.value) / (W.value * (sum_Rcav.value - sum_RW.value) + self.spacing.value * sum_RW.value), 
                      (METER * METER * KELVIN) / WATT)
        u = r.invert()

        return r, u

    def get_zf(self, ratio):
        """Computes the modified zone factor given a resistivity ratio
        between insulation and sheathing. 

        Parameters
        ----------
        ratio : float
            (ri / rins) ratio. 

        Returns
        -------
        zf : float
            The modified zone factor. 
        """
        ratios = np.array([
            0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8,
            2.0, 2.2, 2.4, 2.6, 2.8, 3.0
        ])

        # zf values for stud depth: 3.5 in
        zf_35 = np.array([
            1.20, 1.30, 1.45, 1.55, 1.65, 1.70, 1.80, 1.85,
            1.90, 1.95, 2.00, 2.05, 2.10, 2.15
        ])

        # zf values for stud depth: 4.0 in
        zf_40 = np.array([
            1.30, 1.35, 1.60, 1.70, 1.80, 1.90, 1.95, 2.05,
            2.10, 2.15, 2.20, 2.25, 2.30, 2.35
        ])

        # zf values for stud depth: 6.0 in
        zf_60 = np.array([
            1.60, 1.80, 2.00, 2.10, 2.20, 2.30, 2.40, 2.50,
            2.60, 2.65, 2.73, 2.80, 2.85, 2.92
        ])



        # Interpolate for each stud size
        z_35 = self.interp_along_ratio(ratios, zf_35, ratio)
        z_40 = self.interp_along_ratio(ratios, zf_40, ratio)
        z_60 = self.interp_along_ratio(ratios, zf_60, ratio)

        # Interpolate between stud depths
        if self.length <= Q(3.5, INCH):
            zf = z_35
        elif self.length >= Q(6.0, INCH):
            zf = z_60
        elif self.length <= Q(4.0, INCH):
            zf = z_35 + (z_40 - z_35) * (self.length - Q(3.5, INCH)) / Q(4.0 - 3.5, INCH)
        else:
            # Between 4.0 and 6.0:
            zf = z_40 + (z_60 - z_40) * (self.length - Q(4.0, INCH)) / Q(6.0 - 4.0, INCH)
        return zf

    def interp_along_ratio(self, ratios, values, x):
        """Interpolation function used in the R value calculation
        """
        if x <= ratios[0]:
            return values[0]
        if x >= ratios[-1]:
            return values[-1]

        idx = bisect_left(ratios, x)
        x0, x1 = ratios[idx - 1], ratios[idx]
        y0, y1 = values[idx - 1], values[idx]

        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    
    def get_ancillary_materials(self):
        return self.anciallary_materials