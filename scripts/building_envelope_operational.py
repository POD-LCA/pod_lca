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
num_floors = 10
num_below_grade = 4

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


wall_service_life = 30
structure_service_life = 60
window_service_life = 20

for fk in b.floors:
    floor = b.floors[fk]
    e = Envelope.from_floor(floor)
    floor.add_envelope(e)

    # add constructions - - - - - - - - - - - - - - - - - - - - - - - - - - -

    path = config['file_paths']['operational']['CONSTRUCTIONS']

    if floor.is_on_ground:
        gslab = 'Generic Ground Slab'
        gslab = Construction.from_idf(gslab, path, b, wall_service_life)
        e.add_construction(gslab, 'floor')
    else:
        slab = 'Insulated 8in Slab Floor'
        slab = Construction.from_idf(slab, path, b, structure_service_life)
        e.add_construction(slab, 'floor')

    walls = 'Generic Exterior Wall'
    walls = Construction.from_idf(walls, path, b, wall_service_life)
    e.add_construction(walls, 'wall')

    if floor.is_last:
        roof = 'Generic Roof'
        roof = Construction.from_idf(roof, path, b, structure_service_life)
        e.add_construction(roof, 'cieling')
    else:
        ciel = 'Generic Interior Ceiling'
        ciel = Construction.from_idf(ciel, path, b, structure_service_life)
        e.add_construction(ciel, 'cieling')

b.update_envelope_surfaces()


# add windows - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

for fk in b.floors:
    if not b.floors[fk].is_below_grade:
        env = b.floors[fk].envelope
        wall_key = 'wall_1'
        wwr = .4
        construction = 'Generic Double Pane'
        construction = Construction.from_idf(construction, path, b, window_service_life)
        w = Window.from_wall_and_wwr(env, wall_key, wwr, construction)
        env.add_window(w)

for fk in b.floors:
    if not b.floors[fk].is_below_grade:
        env = b.floors[fk].envelope
        wall_key = 'wall_3'
        wwr = .9
        construction = 'Generic Double Pane'
        construction = Construction.from_idf(construction, path, b, window_service_life)
        w = Window.from_wall_and_wwr(env, wall_key, wwr, construction)
        env.add_window(w)


# add shading - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

for fk in b.floors:
    if not b.floors[fk].is_below_grade:
        env = b.floors[fk].envelope
        wks = env.windows
        construction = 'Aluminum Shading'
        construction = Construction.from_idf(construction, path, b, window_service_life)
        for wk in wks:
            sh = Shading.from_window(env.windows[wk], construction, 1.5, 1.5, 1.5)
            env.add_shading(sh)


# ###############################################
# # TODO: Continue HERE, fix window plotter
# # TODO: Add construction to shading devices
# # TODO: Write spaces


# plot_building(b)
# write_idf_from_building(b)


print(b.get_impacts(scope='end of life', lc_stage='C2')) # {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}
print(b.get_emissions(scope='product', lc_stage=None))

drf_record = b.get_drf_record(time_horizon=100, time_step=1/12)
drf_record.plot('cumulative radiative forcing')

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(b.get_impacts_by_assembly_lcstage('GWP'), "Environmental impacts (by life cycle stage) of Building assemblies by material.", "Assemblies", "GWP (in kg CO2eq)")
graph.show()
