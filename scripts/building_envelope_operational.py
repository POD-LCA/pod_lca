for i in range(50): print('')

from pod_lca.lca_modules.building import Building
from pod_lca.lca_modules.building_envelope import Envelope
from pod_lca.lca_modules.building_envelope import Construction
from pod_lca.lca_modules.operational import write_idf_from_building
from pod_lca.units import METER
from pod_lca.utilities import config

for i in range(50): print('')

# Create Building - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

x = 10
y = 20

b = Building()
floor_plan = [[0,0,0], [x,0,0], [x,y,0], [0,y,0]]
b.add_floor(floor_no=1, floor_plan=floor_plan, geometry_unit=METER, floor_height=3., below_grade=False, on_ground=True)
floor = b.floors['1']

# Add Envelope - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

e = Envelope.from_floor(floor)
floor.add_envelope(e)

# add constructions - - - - - - - - - - - - - - - - - - - - - - - - - - -

path = config['file_paths']['operational']['CONSTRUCTIONS']

walls = 'Typical Insulated Steel Framed Exterior Wall-R16'
walls = Construction.from_idf(walls, path)
e.add_construction(walls, 'wall')

gslab = 'Generic Ground Slab'
gslab = Construction.from_idf(gslab, path)
e.add_construction(gslab, 'floor')

ciel = 'Generic Interior Ceiling'
ciel = Construction.from_idf(ciel, path)
e.add_construction(ciel, 'cieling')

# print(e.constructions)

#TODO: Continue HERE, envelopes/surfaces need to know boundary condition:
# Outdoors, or Adiabatic or Ground
# Probably needs to be computed at the building level

write_idf_from_building(b)
