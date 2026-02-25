
from pod_lca.lca_modules.building import Building
from pod_lca.lca_modules.location import Location
from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter

my_location = Location.from_str("98126, Seattle")
template_model_data ={
    "building_type":"residential",
    "structure_type":"doe_prototype",
    "enclosure-opaque":"Brick, wood framing",
    "enclosure-translucent":"Glazing, operable window",
    "roof":"Asphalt shingle roofing",
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
