
from pod_lca.impacts import ImpactsDatabase
from pod_lca.location import Location
from pod_lca.material_screening import Project
from pod_lca.material_screening import Model
from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter

project = Project()

concrete_yard = Location.from_str("98126, seattle")
project.set_location(concrete_yard)

custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(r'data/impacts_podlca_material-data.csv')
project.set_database(custom_impact_database)

file_path = 'scripts\concrete_example.csv'
model_0 = project.add_model('concrete', file_path)

print(model_0)
print(project)

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(project.get_impacts_by_LCstages_models("GWP", ['concrete']), "GWP by Life Cycle Stages for all models", "Life Cycle Stages", "GWP")
graph.show()
