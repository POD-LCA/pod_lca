from material import HOME
from material.projectManager.projectManager import Project
from material.visualizer.bar_chart import BarChart

project = Project()
project.get_database().import_data_from_CSV(HOME + '\databaseManager\impact_data_new.csv')

file_path = HOME + '\Examples\Smoothie_example.csv'

model = project.create_model_from_csv(file_path, 'Smoothie')

hot_spots = project.get_calculator().hot_spot_analysis(model='Smoothie', impact_category='ODP', printout=True)

graph = BarChart(project)
graph.set_impact_category("GWP")
graph.set_active_models(['Smoothie'])
graph.show()
