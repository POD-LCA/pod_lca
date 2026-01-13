from pod_lca.utilities import config

from pod_lca.lca_modules.building_envelope import Layer
from pod_lca.lca_modules.operational.read_write import find_materials, find_no_mass_materials, find_materials_air_gap
from pod_lca.lca_modules.building_envelope import FramedWall

# from pod_lca.lca_modules.building_envelope import Envelope
# from pod_lca.lca_modules.building import Building
# from pod_lca.lca_modules.location import Location
from pod_lca.units import INCH
from pod_lca.units import METER


for i in range(100): print('')



# make framed envelope - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

layers = {0: {'classification':'exterior_cladding', 'material': 'Clay brick', 'thickness_in': 0.75},
          1: {'classification':'air_gap', 'material': 'Generic Wall Air Gap', 'thickness_in': 1.5},
          2: {'classification':'exterior_insulation', 'material': 'Expanded polystyrene (EPS) Type 1', 'thickness_in': 1.5},
          3: {'classification':'sheathing', 'material': 'Gypsum board', 'thickness_in': 0.5},
          4: {'classification':'framing_insulation', 'material': 'Mineral wool blanket baseline', 'thickness_in': 0.0},
          5: {'classification':'interior_finish', 'material': 'Gypsum board', 'thickness_in': 0.5}}

framing = {'type': 'Metal', 'member': '400S125-18', 'spacing_in': 16.0}

path = config['file_paths']['operational']['CONSTRUCTIONS']

data = find_materials(path, {})
data = find_materials_air_gap(path, data)
data = find_no_mass_materials(path, data)


layers_ = {}
for lk in layers:
    name = layers[lk]['material']
    thickness = layers[lk]['thickness_in']
    mdata = data['materials'][name]
    l = Layer.from_data(mdata, thickness)
    layers_[lk] = l


w = FramedWall.from_layers_framing('framed_wall_test', layers_, framing)

print(w)



