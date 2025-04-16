from lca_modules.location.location import Location
from lca_modules.material.project_manager import Project
from lca_modules.material.model import Model
from lca_modules.material.calculator import Calculator
from lca_modules.impacts.impacts_database import ImpactsDatabase
from plotters.plots.bar_chart import BarChart
from plotters.plotters.matplotlib_plotter import MatplotlibPlotter


project = Project()

concrete_yard = Location.from_str("98126, seattle")
project.set_location(concrete_yard)

custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(r'data/impact_data.csv')
project.set_database(custom_impact_database)

file_path = 'data\concrete_example.csv'
model_0 = Model.from_CSV(file_path, project, 'concrete')

print(model_0)
print(project)

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(Calculator.get_impacts_by_LCstages_models("GWP", [model_0]), "GWP by Life Cycle Stages for all models", "Life Cycle Stages", "GWP")
graph.show()
