for i in range(50): print('')

from pod_lca.lca_modules.building import Building
from pod_lca.lca_modules.building_envelope import Envelope
from pod_lca.lca_modules.building_envelope import Construction
from pod_lca.lca_modules.operational import write_idf_from_building
from pod_lca.units import METER
from pod_lca.utilities import config
from pod_lca.visualizer.plotters.building_plotter import plot_building

for i in range(50): print('')

#TODO: What happens if I make many floors?
#TODO: How do we make it easier to many stacked floors?

# Create Building - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

x = 10
y = 20
floor_to_floor = 3
num_floors = 10

b = Building()
for i in range(num_floors):
    z = floor_to_floor * i
    # floor_plan = [[0,0,z], [x,0,z], [x/2,y/2,z]]
    # floor_plan = [[0,0,z], [x,0,z], [x,y,z], [0,y,z]]
    floor_plan = [[0,0,z], [x/2, -y/4, z], [x,0,z], [x,y,z], [0,y,z]]
    b.add_floor(floor_no=i + 1, 
                floor_plan=floor_plan, 
                geometry_unit=METER, 
                floor_height=floor_to_floor, 
                below_grade=False, 
                on_ground=(i==0))


# Add Envelope - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

for fk in b.floors:
    floor = b.floors[fk]
    e = Envelope.from_floor(floor)
    floor.add_envelope(e)

    # add constructions - - - - - - - - - - - - - - - - - - - - - - - - - - -

    path = config['file_paths']['operational']['CONSTRUCTIONS']

    walls = 'Generic Exterior Wall'
    walls = Construction.from_idf(walls, path)
    e.add_construction(walls, 'wall')

    gslab = 'Generic Ground Slab'
    gslab = Construction.from_idf(gslab, path)
    e.add_construction(gslab, 'floor')

    ciel = 'Generic Interior Ceiling'
    ciel = Construction.from_idf(ciel, path)
    e.add_construction(ciel, 'cieling')


plot_building(b)

# print(e.constructions)

# TODO: Continue HERE, envelopes/surfaces need to know boundary condition:
# Outdoors, or Adiabatic or Ground
# Probably needs to be computed at the building level

# write_idf_from_building(b)
