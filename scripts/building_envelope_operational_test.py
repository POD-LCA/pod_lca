from pod_lca.lca_modules.building import Building
from pod_lca.lca_modules.building_envelope import Envelope
from pod_lca.lca_modules.building_envelope import Construction
from pod_lca.lca_modules.building_envelope import Window
from pod_lca.lca_modules.building_envelope import Shading
from pod_lca.lca_modules.operational import write_idf_from_building
from pod_lca.lca_modules.location import Location
from pod_lca.units import METER
from pod_lca.utilities import config
from pod_lca.visualizer.plotters.building_plotter import plot_building

for i in range(50): print('')

#TODO: How do we make it easier to many stacked floors?

# Create Building - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

x = 20
y = 10
floor_to_floor = 3
num_floors = 1
num_below_grade = 0


my_location = Location.from_str('Seattle, USA')
b = Building.from_parameters(name='test',
                             type='commercial',
                             location=my_location,
                             built_year=2025,
                             life_span=60,
                             no_floors=num_floors, 
                             f2f_height=floor_to_floor, 
                             floor_plan=[[0,0], [x/2, -y/4], [x,0], [x,y], [x/2, y+(y/4)], [0,y]], 
                             floors_below_grade=num_below_grade, 
                             geometry_units=METER)

# Add Envelope - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

wall_service_life = 60

floor = b.floors['1']
e = Envelope.from_floor(floor)
floor.add_envelope(e)

# add constructions - - - - - - - - - - - - - - - - - - - - - - - - - - -

path = config['file_paths']['operational']['CONSTRUCTIONS']

gslab = 'Generic Ground Slab'
gslab = Construction.from_idf(gslab, path, b, wall_service_life)
e.add_construction(gslab, 'floor')