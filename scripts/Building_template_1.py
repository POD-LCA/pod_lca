
from pod_lca.building import Building
from pod_lca.location import Location
from pod_lca.units import METER
from pod_lca.utilities import DataImporter

my_location = Location.from_str("98126, Seattle")
template_model_path = 'scripts\Template_Model_BOM.csv'
template_model_data = DataImporter.json_to_dict('scripts\Template_Model_data.json')

my_building = Building.from_template_model(name='template building', 
                                           type='Commercial', 
                                           location=my_location, 
                                           built_year=2025,
                                           life_span=60,
                                           file_path=template_model_path, 
                                           building_data=template_model_data)

print(my_building.get_impacts(scope='end of life', lc_stage='C2')) # {'all', 'product', 'transportation', 'construction', 'replacement', 'operational energy', 'end of life'}
print(my_building.get_emissions(scope='product', lc_stage=None))

drf_record = my_building.get_drf_record(time_horizon=100, time_step=1/12)
drf_record.plot('instantaneous radiative forcing')
