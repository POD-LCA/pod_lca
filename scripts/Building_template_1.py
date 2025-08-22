
from pod_lca.building import Building
from pod_lca.location import Location
from pod_lca.impacts import ImpactsDatabase
from pod_lca.units import METER
from pod_lca.utilities import DataImporter


my_location = Location.from_US_zip('98102')
template_model_path = 'scripts\Template_Model_BOM.csv'
template_model_data = DataImporter.json_to_dict('scripts\Template_Model_data.json')

database = ImpactsDatabase.new('pod_lca building database')
database.set_data('data\impacts_podlca_building-materials-data.csv')

my_building = Building()
my_building.set_material_database(database)

my_building = my_building.set_template_model(name='template building', 
                                           type='Commercial', 
                                           location=my_location, 
                                           built_year=2025,
                                           file_path=template_model_path, 
                                           building_data=template_model_data)

print(my_building.get_impacts(scope='product'))
print(my_building.get_emissions(scope='product'))