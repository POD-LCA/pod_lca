for i in range(50): print('')

from pod_lca.lca_modules.building import Building
from pod_lca.lca_modules.building_envelope import Envelope
from pod_lca.lca_modules.building_envelope import Construction
from pod_lca.lca_modules.operational import write_idf_from_building
from pod_lca.units import METER
from pod_lca.utilities import config

for i in range(50): print('')

x = 10
y = 20

b = Building()
floor_plan = [[0,0,0], [x,0,0], [x,y,0], [0,y,0]]
b.add_floor(floor_no=1, floor_plan=floor_plan, geometry_unit=METER, floor_height=3., below_grade=False, on_ground=True)
floor = b.floors['1']

e = Envelope.from_floor(floor)

# add constructions - - - - - 

name = 'Typical Insulated Steel Framed Exterior Wall-R16'
path = config['file_paths']['operational']['CONSTRUCTIONS']
c = Construction.from_idf(name, path)
e.add_construction(c, 'walls')
print(e.constructions)

# write_idf_from_building(b)
