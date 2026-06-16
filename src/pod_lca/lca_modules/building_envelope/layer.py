__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

from .material_property import EnvelopeMaterialPropertyMass
from .material_property import EnvelopeMaterialPropertyAirGap
from .material_property import EnvelopeMaterialPropertyNoMass
from .material_property import WindowMaterialPropertyGlazing
from .material_property import WindowMaterialPropertyGas

from pod_lca.units import METER, KELVIN, WATT

mKW = (METER * KELVIN) / WATT


class Layer(object):
    """ Base object to define layers in the building envelope.
    
    Attributes
    ----------
    name :  str
        The name of the layer instance
    
    parent_construction : ~pod_lca.building_envelope.Construction
        The construction to which the layer is assigned. 

    material_property :  ~pod_lca.building_envelope.MaterialProperty
        The material property of the material the layer is made of. 

    _thickness :  ~pod_lca.units.Quantity
        The thickness of the layer

    classification :  str
        The classification of the layer in the envelope ( exterior_cladding, air_gap,
        exterior_insulation, etc.). 

    is_structural : bool
        True of the layer is part of the building structure (slabs for example),
        false if the layer does not have structural properties. 

    structural_element: None or str
        What type of structrural element the layer is ("Slab", "Wall", "Roof")
    """
    def __init__(self):
        self.name = None
        self.parent_construction = None
        self.material_property = None
        self._thickness = None
        self.unit = None
        self.classification = None

        self.is_structural = False
        self.structural_element = None # {"Slab", "Wall", "Roof"}

        self.anciallary_materials = []

    def get_quantity(self, area=None, qty_in=None):
        """ Returns the quantity of the layer.
        
        Parameters
        ----------
        area : float
            The surface area of the layer
        qty_in : {'volume', 'area', 'mass'}
            Requested quantity measured in?
        """
        if qty_in in ['volume', 'mass']:
            return area * self.thickness
        elif qty_in in ["area"]:
            return area
        else:
            raise ValueError("Quantity request not recognized.")


    @property
    def thickness(self):
        """Returns the thickness of the layer
        """
        return self._thickness

    @thickness.setter
    def thickness(self, quantity):
        """Sets the thickness of the layer. 

        Parameters
        ----------
        quantity : ~pod_lca.units.Quantity
            The new thickness of the layer
        """
        self._thickness = quantity

        if self.parent_construction is not None:
            self.parent_construction.get_building().get_structure().update_structure(self.structural_element, self._thickness)

    @classmethod
    def from_data(cls, data, thickness, classification=None):
        """Creates a Layer instance from a data dictionary. 

        Parameters
        ----------
        data :  dict
            Dictionary containing all required inputs. 
        thickness : ~pod_lca.Quantity
            The thickness of the layer. 
        classiification : str
            The layer classification (exterior_cladding, air gap, etc.)

        Returns
        -------
        layer : ~pod_lca.building_envelope.Layer
            The layer instance. 
        """
        layer = cls()
        layer.name = data['name']
        layer.thickness = thickness
        layer.material_property = layer.add_envelope_material_property(data)
        layer.classification = classification
        return layer

    @classmethod
    def from_property_and_thickness(cls, name, material_property, thickness, classification=None):
        """Creates an instance of the Layer class from material property, thickness 
        and classification. 

        Parameters
        ----------
        material_property :  ~pod_lca.building_envelope.MaterialProperty
            The material property of the material the layer is made of. 
        
        thickness :  ~pod_lca.units.Quantity
            The thickness of the layer

        classification :  str
            The classification of the layer in the envelope ( exterior_cladding, air_gap,
            exterior_insulation, etc.). 

        Returns
        -------
        ~pod_lca.building_envelope.Layer
            The Layer instance
        """
        layer = cls()
        layer.name = name
        layer.thickness = thickness
        layer.material_property = material_property
        layer.classification = classification
        return layer

    def add_envelope_material_property(self, data):
        """Adds a material properrty to the layer

        Parameters
        ----------
        data :  dict
            Material property data dictionary. 

        Returns
        -------
        material_prop : ~pod_lca.building_envelope.MaterialProperty
            The material property object
        
        """
        mtype = data['__type__']
        if mtype == 'MaterialPropertyMass':
            material_prop = EnvelopeMaterialPropertyMass.from_data(data)
        elif mtype == 'MaterialPropertyAirGap':
            material_prop = EnvelopeMaterialPropertyAirGap.from_data(data)
        elif mtype == 'MaterialPropertyNoMass':
            material_prop = EnvelopeMaterialPropertyNoMass.from_data(data)
        elif mtype == 'WindowMaterialPropertyGlazing':
            material_prop = WindowMaterialPropertyGlazing.from_data(data)
        elif mtype == 'WindowMaterialPropertyGas':
            material_prop = WindowMaterialPropertyGas.from_data(data)
        else:
            raise ValueError('Material Property type {} has not been implemented yet'.format(mtype))

        return material_prop
    
    def get_r(self, thickness=None):
        """Returns the thermal resistance of the layer

        Parameters
        ----------
        thickness : ~pod_lca.units.Quantity
            (optional) The thickness of the layer if the R value should be computed 
            for a different thickness than currently assigned to the layer. 

        Returns
        -------
        ~pod_lca.units.Quantity
            The thermal resistance of the layer. 
        """
        mtype = self.material_property.__type__
        if mtype == 'MaterialPropertyMass':
            resistivity =  self.material_property.conductivity.invert()
            return resistivity * thickness
        elif mtype == 'EnvelopeMaterialPropertyAirGap':
            return self.material_property.thermal_resistance
        elif mtype == 'MaterialPropertyNoMass':
            return self.material_property.thermal_resistance
        else:
            raise ValueError('Material Property type {} has not been implemented yet'.format(mtype))

    def get_resistivity(self, thickness=None):
        """Returns the thermal resistivity of the layer

        Parameters
        ----------
        thickness : ~pod_lca.units.Quantity
            (optional) The thickness of the layer if the resistivity should be computed 
            for a different thickness than currently assigned to the layer. 

        Returns
        -------
        ~pod_lca.units.Quantity
            The thermal resistivity of the layer. 
        """
        mat = self.material_property
        mtype = mat.__type__
        if mtype == 'MaterialPropertyMass':
            return mat.conductivity.invert()
        elif mtype == 'MaterialPropertyNoMass':
            resistivity = mat.thermal_resistance / thickness
            # return Q(resistivity.value, mKW)
            return resistivity
        else:
            raise ValueError('Material Property type {} has not been implemented yet'.format(mtype))
        
    def set_structural(self, is_structural):
        """Sets the layer as structural. 
        """
        self.is_structural = is_structural

    def add_ancillary_material(self, ancillary_mat):
        """Add an ancillary material to the layer.
        """
        self.anciallary_materials.append(ancillary_mat)
        ancillary_mat.parent = self


class AncillaryMaterial(object):

    def __init__(self, mat_name):
        self.parent = None
        self.material = mat_name

    def get_quantity(self):
        pass


if __name__ == '__main__':
    pass