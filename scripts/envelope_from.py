__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"



from pod_lca.utilities import config

from pod_lca.lca_modules.building_envelope import Layer
from pod_lca.lca_modules.building_envelope import Framing
from pod_lca.lca_modules.building_envelope import FramedWall
from pod_lca.lca_modules.building_envelope import Window
from pod_lca.lca_modules.building_envelope import Envelope

from pod_lca.lca_modules.operational.read_write import find_materials, find_no_mass_materials, find_materials_air_gap

from pod_lca.units import INCH
from pod_lca.units import METER
from pod_lca.units import Quantity as Q


for i in range(100): print('')

constructions_path = config['file_paths']['operational']['CONSTRUCTIONS']

#TODO: All IDF reading functions must implement Quantity / Units

data = find_materials(constructions_path, {})
data = find_materials_air_gap(constructions_path, data)
data = find_no_mass_materials(constructions_path, data)

# general inputs - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

x = Q(20, METER)
y = Q(10, METER)
zero = Q(0, METER)
floor_to_floor = Q(3, METER)

floor_plan = [[zero,zero,zero],
              [x/2, -y/4,zero],
              [x,zero,zero],
              [x,y,zero],
              [x/2, y+(y/4),zero],
              [zero,y,zero]] 

# make framed wall - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

layers = {
          0: {'classification':'exterior_cladding', 'material': 'Clay brick', 'thickness': Q(0.75, INCH).convert_to(METER)},
          1: {'classification':'air_gap', 'material': 'Generic Wall Air Gap', 'thickness': Q(1.5,  INCH).convert_to(METER)},
          2: {'classification':'exterior_insulation', 'material': 'Expanded polystyrene (EPS) Type 1', 'thickness': Q(1.5, INCH).convert_to(METER)},
          3: {'classification':'sheathing', 'material': 'Gypsum board', 'thickness': Q(0.5, INCH).convert_to(METER)},
          4: {'classification':'framing_insulation', 'material': 'Mineral wool blanket baseline', 'thickness': Q(2.0, INCH).convert_to(METER)},
          5: {'classification':'interior_finish', 'material': 'Gypsum board', 'thickness': Q(0.5, INCH).convert_to(METER)}
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
    mdata = data['materials'][name]
    l = Layer.from_data(mdata, thickness, classification)
    layers_[lk] = l

framing = Framing.from_data(framing)

w = FramedWall.from_layers_framing('framed_wall_test', layers_, framing)
w.compute_wall_r()

# make a window - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# window = Window.from_idf(window, b, surfaces, window_service_life)

# make an envelope - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

e = Envelope.from_components(floor_plan, floor_to_floor, wall=w)
print(e.surfaces['floor'].construction)

# make an building - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



