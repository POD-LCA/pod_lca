__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


from pod_lca.utilities import config

from pod_lca.lca_modules.building import Building

from pod_lca.lca_modules.building_structure import BuildingStructure

from pod_lca.lca_modules.location import Location


from pod_lca.lca_modules.building_envelope import BuildingEnvelope
from pod_lca.lca_modules.building_envelope import Envelope
from pod_lca.lca_modules.building_envelope import Layer
from pod_lca.lca_modules.building_envelope import Framing
from pod_lca.lca_modules.building_envelope import FramedWall
from pod_lca.lca_modules.building_envelope import Floor
from pod_lca.lca_modules.building_envelope import Ceiling
from pod_lca.lca_modules.building_envelope import Window
from pod_lca.lca_modules.building_envelope import EnvelopeMaterialProperty

from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterial
from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterialAirGap
from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterialNoMass
from pod_lca.lca_modules.building_envelope.material_property import WindowMaterialGlazing
from pod_lca.lca_modules.building_envelope.material_property import WindowMaterialGas



from pod_lca.lca_modules.operational.read_write import find_materials
from pod_lca.lca_modules.operational.read_write import find_no_mass_materials
from pod_lca.lca_modules.operational.read_write import find_materials_air_gap

from pod_lca.units import INCH, METER, SQUARE_METER, CUBIC_METER, WATT, KELVIN, KILOGRAM, JOULE
from pod_lca.units import Quantity as Q


for i in range(100): print('')

constructions_path = config['file_paths']['operational']['CONSTRUCTIONS']

# general inputs - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

bname = 'Tomas'
btype = 'Residential'
location = Location.from_str("98126, Seattle")
built_year =  2025
life_span = 100


x = Q(20, METER)
y = Q(10, METER)
zero = Q(0, METER)
floor_to_floor = Q(3, METER)
num_stories = 5
floor_plan = [[zero,zero,zero],
              [x/2, -y/4,zero],
              [x,zero,zero],
              [x,y,zero],
              [x/2, y+(y/4),zero],
              [zero,y,zero]] 



# make framed wall - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

mdata = {}
mdata['name']                = 'Clay brick'
mdata['roughness']           = 'MediumRough'
mdata['thickness']           = Q(0.01905, METER)    
mdata['conductivity']        = Q(0.78, (WATT / (METER * KELVIN)))       
mdata['density']             = Q(1920, (KILOGRAM / CUBIC_METER))       
mdata['specific_heat']       = Q(720, (JOULE / (KILOGRAM * KELVIN)))        
mdata['thermal_absorptance'] = 0.9        
mdata['solar_absorptance']   = 0.7        
mdata['visible_absorptance'] = 0.7        
m0 = EnvelopeMaterial.from_data(mdata)


mdata = {}
mdata['name']               = 'Generic Wall Air Gap'
mdata['thermal_resistance'] = Q(0.1603675, (SQUARE_METER * KELVIN) / WATT)
m1 = EnvelopeMaterialAirGap.from_data(mdata)

mdata = {}
mdata['name']                = 'Expanded polystyrene (EPS) Type 1'       
mdata['roughness']           = 'Rough'           
mdata['thermal_resistance']  = Q(3.17, (SQUARE_METER * KELVIN) / WATT)          
mdata['thermal_absorptance'] = 0.9000000      
mdata['solar_absorptance']   = 0.7500000      
mdata['visible_absorptance'] = 0.7500000
mdata['thickness']           = None
m2 = EnvelopeMaterialNoMass.from_data(mdata)


mdata = {}
mdata['name']                = 'Gypsum board'
mdata['roughness']           = 'MediumSmooth'
mdata['thickness']           = Q(0.0159, METER)    
mdata['conductivity']        = Q(0.159892999094055, (WATT / (METER * KELVIN)))       
mdata['density']             = Q(800.001829191177, (KILOGRAM / CUBIC_METER))       
mdata['specific_heat']       = Q(1089.29718545594, (JOULE / (KILOGRAM * KELVIN)))        
mdata['thermal_absorptance'] = 0.9        
mdata['solar_absorptance']   = 0.7        
mdata['visible_absorptance'] = 0.7        
m3 = EnvelopeMaterial.from_data(mdata)


mdata = {}
mdata['name']                = 'Mineral wool blanket baseline'       
mdata['roughness']           = 'Rough'           
mdata['thermal_resistance']  = Q(3.91, (SQUARE_METER * KELVIN) / WATT)          
mdata['thermal_absorptance'] = 0.9000000      
mdata['solar_absorptance']   = 0.7500000      
mdata['visible_absorptance'] = 0.7500000          
mdata['thickness']           = None
m4 = EnvelopeMaterialNoMass.from_data(mdata)

layers = {
          0: {'classification':'exterior_cladding', 'material': m0, 'thickness': Q(0.75, INCH).convert_to(METER)},
          1: {'classification':'air_gap', 'material': m1, 'thickness': Q(1.5,  INCH).convert_to(METER)},
          2: {'classification':'exterior_insulation', 'material': m2, 'thickness': Q(1.5, INCH).convert_to(METER)},
          3: {'classification':'sheathing', 'material': m3, 'thickness': Q(0.5, INCH).convert_to(METER)},
          4: {'classification':'framing_insulation', 'material': m4, 'thickness': Q(2.0, INCH).convert_to(METER)},
          5: {'classification':'interior_finish', 'material': m3, 'thickness': Q(0.5, INCH).convert_to(METER)}
          }

framing = {'name': 'metal_16in', 
           'type': 'Metal', 
           'member': '400S125-18', 
           'spacing': Q(16.0, INCH).convert_to(METER),
           'L':       Q(1.25, INCH).convert_to(METER),
           'ds':      Q(3.5, INCH).convert_to(METER),
           'dII':     Q(0.043, INCH).convert_to(METER)}

layers_ = {}
for lk in layers:
    name = layers[lk]['material']
    thickness = layers[lk]['thickness']
    classification = layers[lk]['classification']
    material_property = layers[lk]['material']
    l = Layer.from_property_and_thickness(name, material_property, thickness, classification)
    layers_[lk] = l

framing = Framing.from_data(framing)

w = FramedWall.from_layers_framing('framed_wall_test', layers_, framing)
w.compute_wall_r()


# make a floor - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

f = Floor.from_idf('Generic Interior Floor', constructions_path)

# make a ceiling - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

c = Ceiling.from_idf('Generic Interior Ceiling', constructions_path)

# make a window - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# window = Window.from_idf(window, b, surfaces, window_service_life)

# make an envelope - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

e = Envelope.from_components(floor_plan, floor_to_floor, wall=w, floor=f, ceiling=c)
be = BuildingEnvelope.from_envelope_and_stories(e, num_stories)
# make a structure - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

stype = 'Concrete' # 'Concrete', 'Steel', 'CLT', 'Light-Frame'
mui_type = 'low' # 'mid', 'hight'

s = BuildingStructure.from_sample_buildings(btype, stype, mui_type, floor_plan, num_stories)

# make an building - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

b = Building.from_assemblies(name, btype, location, built_year, life_span, s, be)

from pod_lca.lca_modules.operational.viewers import BuildingViewer

v = BuildingViewer(b)
v.show()

#TODO Fix envelope height thing
#TODO: Continue checking building_envelope implications