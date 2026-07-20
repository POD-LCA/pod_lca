__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building_envelope.construction import Construction
from pod_lca.lca_modules.building_envelope.layer import Layer, AncillaryMaterial
from pod_lca.units import Quantity as Q
from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterialPropertyNoMass
from pod_lca.units import METER, SQUARE_METER, KELVIN, WATT

m2KW = (SQUARE_METER * KELVIN) / WATT
mKW = (METER * KELVIN) / WATT


class Wall(Construction):
    """Wall construction object based on the 
    ~pod_lca.building_envelope.Construction class. 
    """
    def __init__(self):
        super().__init__()
        self.__type__ = 'Wall'


class FramedWall(Construction):
    """Framed Wall construction object based on the 
    ~pod_lca.building_envelope.Construction class.
    
    Attributes
    ----------
    __type__ : str
        The type of construction "FramedWall"

    framing :  ~pod_lca.building_envelope.Framing
        The framing object used by the wall
    
    r : ~pod_lca.units.Quantity
        The thermal resistance of the framed wall

    u : ~pod_lca.units.Quantity
        The thermal conductance of the framed wall

    virtual_layers : (dict of) ~pod_lca.building_envelope.Layer
        The layers created for the e+ siumulation, not real layers,
        ignored for embodied impact calculations. 

    virtual_layer_order : list
        The order of the virtual layers from outside to inside. 
    """
    def __init__(self):
        super().__init__()
        self.__type__ = 'FramedWall'
        self.framing = None
        self.resistance = None
        self.conductance = None
        self.virtual_layers = {}
        self.virtual_layer_order = []


    @classmethod
    def from_layers_framing(cls, name, layers, framing):
        """Create a framed wall instance from layers and framing. 

        Parameters
        ----------
        name : str
            The name of the framed wall instance. 

        layers : (dict of) ~pod_lca.building_envelope.Layer
            The layers of the framed wall. 
        
        framing : ~pod_lca.building_envelope.Framing
            The framing object used by the wall. 

        Returns
        -------
        fwall :  ~pod_lca.building_envelope.FramedWall
            The framed wall instance. 

        """
        fwall = cls.from_materials(name)
        fwall.layer_order = [lk for lk in layers]
        fwall.layers = layers
        fwall.framing = framing

        for i in range(len(fwall.layers)):
            fwall.layers[i].parent_construction = fwall
        
        fwall.compute_wall_r()

        vmat = EnvelopeMaterialPropertyNoMass()
        vmat.thickness           = Q(1, METER)
        vmat.conductivity        = vmat.thickness / fwall.resistance
        vmat.roughness           = 'MediumRough'
        vmat.thermal_absorptance = 0.9
        vmat.solar_absorptance   = 0.7
        vmat.visible_absorptance = 0.7
        vlayer = Layer()
        vlayer.name = '{}_virtual_layer'.format(name)
        vlayer.parent_construction = fwall
        vlayer.material_property = vmat
        vlayer._thickness = vmat.thickness
        vlayer.unit = None
        vlayer.classification = 'virtual_layer'
        vlayer.is_structural = False

        last_layer = fwall.layer_order[-1]

        fwall.virtual_layers['interior'] = vlayer
        fwall.virtual_layers[last_layer] = fwall.layers[last_layer]
        fwall.virtual_layer_order.append('interior') 
        fwall.virtual_layer_order.append(last_layer)
        
        framing.set_parent(fwall)
        return fwall
    
    def compute_wall_r(self):
        """Computes the R value and U value of the framed wall,
        including the thermal bridges caused by the framing. 
        """
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

        self.resistance, self.conductance = self.framing.compute_bridge(Ra=Ra, Rb=Rb, rins=rins, di=di, ratio=ratio)

    def get_constituent_materials(self):
        constituent_materials = super().get_constituent_materials()
        
        framing_ancillary = self.framing.get_ancillary_materials()
        constituent_materials.extend(framing_ancillary)
        return constituent_materials
