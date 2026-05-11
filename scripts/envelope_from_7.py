import sys
import importlib

def reload_library():
    # Wipe the entire library and all submodules from cache
    to_delete = [key for key in sys.modules if key == "pod_lca" or key.startswith("pod_lca.")]
    for key in to_delete:
        del sys.modules[key]

# Call this FIRST, before any library imports
reload_library()

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import os
import pod_lca

from pod_lca.utilities import config

from pod_lca.lca_modules.building import Building
from pod_lca.lca_modules.building import BuildingFloor

from pod_lca.lca_modules.building_structure import StatisticalStructure
from pod_lca.lca_modules.building_structure import Structure
from pod_lca.lca_modules.location import Location


from pod_lca.lca_modules.building_envelope import BuildingEnvelope
from pod_lca.lca_modules.building_envelope import Envelope
from pod_lca.lca_modules.building_envelope import Construction
from pod_lca.lca_modules.building_envelope import Layer
from pod_lca.lca_modules.building_envelope import Framing
from pod_lca.lca_modules.building_envelope import FramedWall
from pod_lca.lca_modules.building_envelope import Floor
from pod_lca.lca_modules.building_envelope import Ceiling
from pod_lca.lca_modules.building_envelope import Window
from pod_lca.lca_modules.building_envelope import EnvelopeMaterialProperty

from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterialPropertyMass
from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterialPropertyAirGap
from pod_lca.lca_modules.building_envelope.material_property import EnvelopeMaterialPropertyNoMass
from pod_lca.lca_modules.building_envelope.material_property import WindowMaterialPropertyGlazing
from pod_lca.lca_modules.building_envelope.material_property import WindowMaterialPropertyGas


from pod_lca.lca_modules.operational import OperationalEnergyObject
# from pod_lca.lca_modules.operational.read_write import find_materials
# from pod_lca.lca_modules.operational.read_write import find_no_mass_materials
# from pod_lca.lca_modules.operational.read_write import find_materials_air_gap

from pod_lca.units import INCH, METER, SQUARE_METER, CUBIC_METER, WATT, KELVIN, KILOGRAM, JOULE
from pod_lca.units import Quantity as Q

from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter


for i in range(100): print('')

constructions_path = config['file_paths']['operational']['CONSTRUCTIONS']

# general inputs - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

bname = 'Tomas'
btype = 'Residential'
location = Location.from_str("98126, Seattle")
built_year =  2025
life_span = 100

x = Q(20, METER)
y = Q(50, METER)
zero = Q(0, METER)
floor_to_floor = Q(3, METER)
num_stories = 8
# floor_plan = [[zero,zero,zero],
#               [x/2, -y/4,zero],
#               [x,zero,zero],
#               [x,y,zero],
#               [x/2, y+(y/4),zero],
#               [zero,y,zero]] 

floor_plan = [[zero,zero,zero],
              [zero,y,zero], 
              [x/2, y+(y/4),zero],
              [x,y,zero],
              [x,zero,zero],
              [x/2, -y/4,zero]]
flr = BuildingFloor.from_floor_plan(floor_plan, floor_to_floor, btype)

# make framed wall - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


m0 = EnvelopeMaterialPropertyMass.from_idf('Clay brick', constructions_path)
m1 = EnvelopeMaterialPropertyAirGap.from_idf('Generic Wall Air Gap', constructions_path)
m2 = EnvelopeMaterialPropertyNoMass.from_idf('Expanded polystyrene (EPS) Type 1', constructions_path)
m3 = EnvelopeMaterialPropertyMass.from_idf('Gypsum board', constructions_path)
m4 = EnvelopeMaterialPropertyNoMass.from_idf('Mineral wool blanket baseline', constructions_path)



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
    name = layers[lk]['material'].name
    thickness = layers[lk]['thickness']
    classification = layers[lk]['classification']
    material_property = layers[lk]['material']
    l = Layer.from_property_and_thickness(name, material_property, thickness, classification)
    layers_[lk] = l

layers_[0].set_structural(True)

framing = Framing.from_data(framing)

framed_wall = FramedWall.from_layers_framing('framed_wall_test', layers_, framing)
framed_wall.compute_wall_r()

# make a floor - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

f = Floor.from_idf('Generic Interior Floor', constructions_path)

# make a ceiling - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

c = Ceiling.from_idf('Generic Interior Ceiling', constructions_path)

# make a window - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

window1 = Window.from_idf('Generic Double Pane', constructions_path)

w = Q(3, METER)
h = Q(2, METER)
wall_key1 = 'wall_1'
window1.set_width_height(w, h)

wall_key2 = 'wall_2'
wwr = .9
window2 = Window.from_idf('Generic Double Pane', constructions_path)
window2.set_wwr(wwr)

windows = {wall_key1: window1, wall_key2: window2}

# make an envelope - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ename = 'tomas_envelope'
e = Envelope.from_components(ename, flr, wall=framed_wall, floor=f, ceiling=c, windows=windows)

be = BuildingEnvelope.from_envelope_and_stories(e, num_stories)

# make a structure - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

stype = 'Concrete' # 'Concrete', 'Steel', 'CLT', 'Light-Frame'
mui_type = 'low' # 'mid', 'high'

s_floor = Structure.create(stype, flr)
s = StatisticalStructure.create(s_floor, num_stories)
s.build(mui_type)

# make a building - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

b = Building.from_assemblies(bname, location, built_year, life_span, s, be)

# overide defaults - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# b.set_eplus_path("temp/EnergyPlus-25-1-0/") # default looks standard system locations
# b.set_eplus_out_folder("temp/out") # default writes to a temp folder
# b.set_idf_file_path("temp/temp_operational.idf") # default writes to a temp file
# b.set_weather_file_path("src/pod_lca/data/operational_weather_seattle.epw") # default based on climate zone
b.operational_energy_method = 'eplus' # {'eplus', 'EUIs'}, default is 'eplus'

# get operational impacts - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# print(b.get_operational_impacts()) # default is 'total'

# # # run embodied - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

print(b.get_impacts(scope='all')) # {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}
# print(b.get_emissions(scope='product'))

drf_record = b.get_drf_record(time_horizon=100, time_step=1/12)
drf_record.plot('cumulative radiative forcing')

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(b.get_impacts_by_assembly_lcstage('GWP'), "Environmental impacts (by life cycle stage) of Building assemblies by material.", "Assemblies", "GWP (in kg CO2eq)")
graph.show()

# # #TODO: Implement no mass material with Framed Wall properties (not usual layaered wall)

# FIXME: Grashopper example geometry issue, have check on polygon open/closed. 