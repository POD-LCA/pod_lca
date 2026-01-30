__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building_envelope.construction import Construction
from pod_lca.units import Quantity as Q
from pod_lca.units import METER, SQUARE_METER, KELVIN, WATT

m2KW = (SQUARE_METER * KELVIN) / WATT
mKW = (METER * KELVIN) / WATT


class Wall(Construction):
    def __init__(self):
        super().__init__()
        self.__type__ = 'Wall'


class FramedWall(Construction):
    def __init__(self):
        super().__init__()
        self.__type__ = 'Wall'
        self.framing = None
        self.r = None
        self.u = None


    @classmethod
    def from_layers_framing(cls, name, layers, framing):
        fwall = cls.create(name)
        fwall.layer_order = {lk: layers[lk].name for lk in layers}
        fwall.layers = layers
        fwall.framing = framing
        return fwall
    
    def compute_wall_r(self):

        Ra   = Q(0., m2KW)
        Rb   = Q(0., m2KW)
        ri   = Q(0., mKW)
        rins = Q(0., mKW)
        for key in self.layers:
            layer = self.layers[key]
            classification      = layer.classification
            thickness           = layer.thickness
            # material_property   = layer.material_property

            if classification == "exterior_cladding":
                # Ra += self.compute_layer_r(material_property, thickness)
                Ra += layer.get_r(thickness)

            elif classification == "air_gap":
                # Ra += self.compute_layer_r(material_property, None)
                Ra += layer.get_r(None)

            elif classification == "exterior_insulation":
                Ra += layer.get_r(thickness)
                ri += layer.get_resistivity(thickness)

            elif classification == "sheathing":
                di = thickness
                Ra += layer.get_r(thickness)
                ri += layer.get_resistivity(thickness)

            elif classification == "framing_insulation":
                rins = layer.get_resistivity(thickness)

            elif classification == "interior_finish":
                Rb += layer.get_r(thickness)
                # interior_finish_material = material_property
                interior_finish_thickness = thickness

        # Add air films
        Ra += Q(.2  / 5.678, m2KW)  # ft²·°F·h/Btu --> (m2K/W)
        Rb += Q(.7  / 5.678, m2KW)  # ft²·°F·h/Btu --> (m2K/W)

        ratio = ri / rins if rins > 0 else 0
        self.framing.get_zf(ratio)

        framing_type = self.framing.type
        spacing = self.framing.spacing

        if framing_type == "Metal":
            r, u = self.framing.metal_bridge(ri=ri, rins=rins, di=di, Ra=Ra, Rb=Rb)
            self.r = r
            self.u = u

        elif framing_type == "Wood":
            width = 1.5  # default 2-by construction
            k_wood = .12  # W/m-K (typical softwood) conductivity
            self.r = self.framing.wood_bridge(s=spacing, width=width, ds=ds, k=k_wood, Ra=Ra, Rb=Rb, rins=rins)

        else:
            raise ValueError(f"Unknown framing type: {framing_type}")

