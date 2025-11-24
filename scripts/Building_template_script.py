
from pathlib import Path
from pod_lca.building import Building
from pod_lca.location import Location
from pod_lca.utilities import DataImporter
from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter


for i in range(50): print('')

current_folder = Path(__file__).resolve().parents[0]

my_location = Location.from_str("98126, Seattle")
template_model_data = DataImporter.json_to_dict(current_folder / 'Template_Model_data.json')

my_building = Building.from_template_model(name='template building',
                                           location=my_location, 
                                           built_year=2025,
                                           life_span=60,
                                           building_data=template_model_data)


# plot_building(my_building)

# my_building.write_idf()
# eplus_path = os.path.join(pod_lca.TEMP, 'EnergyPlus-25-1-0')
# wea = config['file_paths']['operational']['SEATTLE']
# my_building.run_operational_energy_model(eplus_path, pod_lca.TEMP, wea)


print(my_building.get_impacts(scope='product',)) # {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}
print(my_building.get_impacts(scope='construction'))
print(my_building.get_impacts(scope='end of life', lc_stage='C1'))
print(my_building.get_impacts(scope='end of life', lc_stage='C2'))
print(my_building.get_impacts(scope='end of life', lc_stage='C3'))
print(my_building.get_impacts(scope='end of life', lc_stage='C4'))

drf_record = my_building.get_drf_record(time_horizon=100, time_step=1/12)
drf_record.plot('cumulative radiative forcing')

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(my_building.get_impacts_by_assembly_lcstage('GWP'), "Environmental impacts (by life cycle stage) of Building assemblies by material.", "Assemblies", "GWP (in kg CO2eq)")
graph.show()
