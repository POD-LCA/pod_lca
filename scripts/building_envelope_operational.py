import os
import pod_lca
# from pathlib import Path
# from pod_lca.building import Building
# from pod_lca.building import Scenario
# from pod_lca.location import Location
# from pod_lca.units import METER
# from pod_lca.utilities import DataImporter
from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter


from pod_lca.lca_modules.building import Building

from pod_lca.lca_modules.building_envelope import Envelope
from pod_lca.lca_modules.building_envelope import Wall
from pod_lca.lca_modules.building_envelope import Floor
from pod_lca.lca_modules.building_envelope import Ceiling
from pod_lca.lca_modules.building_envelope import Window
from pod_lca.lca_modules.building_envelope import Shading

from pod_lca.lca_modules.operational.operational_object import OperationalObject

from pod_lca.lca_modules.geometry.building_geometry import window_surfaces_from_wwr
from pod_lca.lca_modules.geometry.building_geometry import shading_surfaces_from_window

from pod_lca.lca_modules.location import Location
from pod_lca.units import METER
from pod_lca.utilities import config
from pod_lca.visualizer.plotters.building_plotter import plot_building

for i in range(50): print('')

# Create Building - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

x = 20
y = 10
floor_to_floor = 3
num_floors = 3
num_below_grade = 1

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


path = config['file_paths']['operational']['SYSTEMS']
b.operational_object = OperationalObject.from_idf(path)



# Add Envelope - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

path = config['file_paths']['operational']['CONSTRUCTIONS']
b.read_constructions_data(path)
b.read_material_properties_data(path)

wall_service_life = 30
structure_service_life = 60
window_service_life = 20

for fk in b.floors:
    floor = b.floors[fk]
    e = Envelope.from_floor(floor)
    floor.add_envelope(e)


    # add walls - - - - - - - - - - - - - - - - - - - - - - - - - - -

    walls = 'Generic Exterior Wall'
    surfaces = [e.surfaces[sk] for sk in e.wall_surface_keys]
    walls = Wall.from_idf(walls, b, surfaces, wall_service_life)
    e.add_construction(walls)

    # add floor slabs - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if floor.is_on_ground:
        gslab = 'Generic Ground Slab'
        surfaces = [e.surfaces['floor']]
        gslab = Floor.from_idf(gslab, b, surfaces, structure_service_life)
        e.add_construction(gslab)
    else:
        slab = 'Insulated 8in Slab Floor'
        surfaces = [e.surfaces['floor']]
        slab = Floor.from_idf(slab, b, surfaces, structure_service_life)
        e.add_construction(slab)


    # add ceiling slabs - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if floor.is_last:
        roof = 'Generic Roof'
        surfaces = [e.surfaces['ceiling']]
        roof = Ceiling.from_idf(roof, b, surfaces, structure_service_life)
        e.add_construction(roof)
    else:
        ciel = 'Generic Interior Ceiling'
        surfaces = [e.surfaces['ceiling']]
        ciel = Ceiling.from_idf(ciel, b, surfaces, structure_service_life)
        e.add_construction(ciel)



# # add windows - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

for fk in b.floors:
    if not b.floors[fk].is_below_grade:
        env = b.floors[fk].envelope
        wall_key = 'wall_1'
        wwr = .4
        window = 'Generic Double Pane'
        surfaces = window_surfaces_from_wwr(env, wall_key, wwr)
        window = Window.from_idf(window, b, surfaces, window_service_life)
        env.add_window(window, wall_key)

for fk in b.floors:
    if not b.floors[fk].is_below_grade:
        env = b.floors[fk].envelope
        wall_key = 'wall_3'
        wwr = .9
        window = 'Generic Double Pane'
        surfaces = window_surfaces_from_wwr(env, wall_key, wwr)
        window = Window.from_idf(window, b, surfaces, window_service_life)
        env.add_window(window, wall_key)


# # add shading devices - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# for fk in b.floors:
#     if not b.floors[fk].is_below_grade:
#         env = b.floors[fk].envelope
#         wks = env.windows.keys()
#         shading = 'Aluminum Shading'
#         for wk in wks:
#             window = env.windows[wk]
#             surfaces = shading_surfaces_from_window(window, top=1.5, left=1.5, right=1.5)
#             sh = Shading.from_idf(shading, b, surfaces, window_service_life)
#             env.add_construction(sh)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TODO: Wall quantities are still not substracting windows
# FIXME: Building plotter is missing shading devices
# TODO: Fix envelope idf errors (See eplus error file)
# TODO: Implement outdoor boundary condition generator
# TODO: Ceiling, not cieling

# # plot_building(b)
b.write_idf()
eplus_path = os.path.join(pod_lca.TEMP, 'EnergyPlus-25-1-0')
wea = config['file_paths']['operational']['SEATTLE']
b.run_operational_energy_model(eplus_path, pod_lca.TEMP, wea)


# print(b.get_impacts(scope='end of life', lc_stage='C2')) # {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}
# print(b.get_emissions(scope='product', lc_stage=None))

# drf_record = b.get_drf_record(time_horizon=100, time_step=1/12)
# drf_record.plot('cumulative radiative forcing')

# graph = BarChart.from_plotter(MatplotlibPlotter)
# graph.draw(b.get_impacts_by_assembly_lcstage('GWP'), "Environmental impacts (by life cycle stage) of Building assemblies by material.", "Assemblies", "GWP (in kg CO2eq)")
# graph.show()
