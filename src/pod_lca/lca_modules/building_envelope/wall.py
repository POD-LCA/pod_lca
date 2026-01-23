__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.building_envelope.construction import Construction


class Wall(Construction):
    def __init__(self):
        super().__init__()
        self.__type__ = 'Wall'


class FramedWall(Construction):
    def __init__(self):
        super().__init__()
        self.__type__ = 'Wall'
        self.framing = None


    @classmethod
    def from_layers_framing(cls, name, layers, framing):
        fwall = cls.create(name)
        fwall.layer_order = {lk: layers[lk].name for lk in layers}
        fwall.layers = layers
        fwall.framing = framing
        return fwall
    
    def compute_wall_r(self):

        Ra   = 0.0
        Rb   = 0.0
        ri   = 0.0
        rins = 0.0
        for key in self.layers:
            classification = self.layers[key].classification
            material_property       = self.layers[key].material_property
            thickness      = self.layers[key].thickness

            if classification == "exterior_cladding":
                Ra += self.compute_layer_r(material_property, thickness)

        #     elif classification == "air_gap":
        #         Ra += compute_layer_r(material, None, material_properties)

        #     elif classification == "exterior_insulation":
        #         Ra += compute_layer_r(material, thickness, material_properties)
        #         ri += compute_resistivity(material, material_properties)

        #     elif classification == "sheathing":
        #         di = thickness
        #         Ra += compute_layer_r(material, thickness, material_properties)
        #         ri += compute_resistivity(material, material_properties)

        #     elif classification == "framing_insulation":
        #         rins = compute_resistivity(material, material_properties)

        #     elif classification == "interior_finish":
        #         Rb += compute_layer_r(material, thickness, material_properties)
        #         interior_finish_material = material
        #         interior_finish_thickness = thickness

        # # Add air films
        # Ra += .2 # ft²·°F·h/Btu
        # Rb += .7 # ft²·°F·h/Btu


        # ratio = ri / rins if rins > 0 else 0
        # zf = get_zf(ds, ratio)


        # framing_type = framing['type']
        # spacing = framing['spacing_in']

        # if framing_type == "Metal":
        #     results = metal_bridge(s=spacing, ri=ri, rins=rins, ds=ds, dII=dii, di=di, L=l, Ra=Ra, Rb=Rb, zf=zf)

        # elif framing_type == "Wood":
        #     width = 1.5  # default 2-by construction
        #     k_wood = .12  # W/m-K (typical softwood) conductivity
        #     results = wood_bridge(s=spacing, width=width, ds=ds, k=k_wood, Ra=Ra, Rb=Rb, rins=rins)

        # else:
        #     raise ValueError(f"Unknown framing type: {framing_type}")

        # print(results)


    def compute_layer_r(self, material_property, thickness):
        mtype = material_property.__type__
        print(mtype)

        if hasattr(material_property, 'thermal_resistance'):
            if material_property.thermal_resistance:
                return float(material_property['thermal_resistance']) * 5.678

        if mtype == 'No Mass':
            return float(material_property['rsi_per_in']) * material_property * 5.678
        else:
            resistivity =  0.144 / float(material_property['conductivity'])
            return resistivity * thickness