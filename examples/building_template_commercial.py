
from pod_lca.lca_modules.building import Building
from pod_lca.lca_modules.location import Location
from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter

my_location = Location.from_str("98126, Seattle")
template_model_data = {
    "building_type":"commercial",
    "structure_type":"bp-steel",
    "enclosure-opaque":"rain-screen-thin-brick",
    "enclosure-translucent":"glazing-double-pane",
    "no_floors":6,
    "f2f_height":3.0,
    "floor_plan":[[0.0 , 0.0], [0.0, 180.0], [120.0, 180.0], [120.0, 0.0]],
    "floors_below_grade":1,
    "wwr":0.7,
    "geometry_units":"ft",
    "logistic_type":"local",
    "construction_energy_use":80,
    "construction_energy_use_unit":"MWh"
}

my_building = Building.from_template_model(name='template building',
                                           location=my_location, 
                                           built_year=2025,
                                           life_span=60,
                                           **template_model_data)

print(my_building.get_impacts(scope='product',)) # {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}

drf_record = my_building.get_drf_record(time_horizon=100, time_step=1/12)
drf_record.plot('cumulative radiative forcing')

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(my_building.get_impacts_by_assembly_lcstage('GWP'), "Environmental impacts (by life cycle stage) of building assemblies by material.", "Assemblies", "GWP (in kg CO2eq)")
graph.show()
