
import os
from pathlib import Path
import pod_lca
from pod_lca.building import Building
from pod_lca.building import Scenario
from pod_lca.location import Location
from pod_lca.units import METER
from pod_lca.utilities import DataImporter
from pod_lca.visualizer import BarChart
from pod_lca.visualizer import MatplotlibPlotter
from pod_lca.utilities import config
from pod_lca.visualizer.plotters.building_plotter import plot_building


for i in range(50): print('')

current_folder = Path(__file__).resolve().parents[0]

my_location = Location.from_str("98126, Seattle")
template_model_path = current_folder / 'Template_Model_BOM.csv'
template_model_data = DataImporter.json_to_dict(current_folder / 'Template_Model_data.json')

env_constructions_path = config['file_paths']['operational']['CONSTRUCTIONS']
operational_sys_path = config['file_paths']['operational']['SYSTEMS']

my_building = Building.from_template_model(name='template building', 
                                           type='Commercial', 
                                           location=my_location, 
                                           built_year=2025,
                                           life_span=60,
                                           file_path=template_model_path, 
                                           building_data=template_model_data,
                                           env_constructions_path=env_constructions_path,
                                           operational_sys_path=operational_sys_path)


# plot_building(my_building)

my_building.write_idf()
eplus_path = os.path.join(pod_lca.TEMP, 'EnergyPlus-25-1-0')
wea = config['file_paths']['operational']['SEATTLE']
my_building.run_operational_energy_model(eplus_path, pod_lca.TEMP, wea)


print(my_building.get_impacts(scope='end of life', lc_stage='C2')) # {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}
print(my_building.get_emissions(scope='product', lc_stage=None))

drf_record = my_building.get_drf_record(time_horizon=100, time_step=1/12)
drf_record.plot('cumulative radiative forcing')

graph = BarChart.from_plotter(MatplotlibPlotter)
graph.draw(my_building.get_impacts_by_assembly_lcstage('GWP'), "Environmental impacts (by life cycle stage) of Building assemblies by material.", "Assemblies", "GWP (in kg CO2eq)")
graph.show()

