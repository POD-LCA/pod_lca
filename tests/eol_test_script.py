
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from tqdm import tqdm

from pod_lca.building import Building
from pod_lca.building import BuildingComponent
from pod_lca.impacts import EOLImpactsDatabase
from pod_lca.impacts import Impacts
from pod_lca.location import Location
from pod_lca.units import UNITS_MAP
from pod_lca.utilities import DataImporter
from pod_lca.utilities import config

impact_data_file_path = r'data/impacts_podlca_eol-impacts.csv'
test_dict_file_path = r'tests/eol_test_test-cases.json'

test_data = r'tests/eol_test_test-values.csv'
output_file = r'tests/eol_test_report.csv'
test_data_dict = DataImporter.csv_to_dict(test_data, 'test name')

# create building
my_land_plot = Location.from_str("98126, Seattle")

test_building = Building.build(name='Test Building', type='Commercial', location=my_land_plot, built_year=2025, geometry=None) # Dealing with geometry is not within the scope of EOL

eol_impact_database = EOLImpactsDatabase.new("EOL database")
eol_impact_database.set_primary_key('Material')
eol_impact_database.set_process_key('Process')
eol_impact_database.set_life_cycle_stage_key('LCA Stage')
eol_impact_database.set_data(impact_data_file_path)

test_building.set_eol_database(eol_impact_database)

tests_dict = DataImporter.json_to_dict(test_dict_file_path)
impact_categories = config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']
output_dict = {}
for test_name in tqdm(tests_dict):
   parts = tests_dict[test_name]
   for part in parts:
      parts[part]['unit'] = UNITS_MAP[parts[part]['unit']]

   test_component = BuildingComponent.create(name=test_name, materials=[None]) # Making a building component from materials not within the scope of EOL
   test_building.add_component(test_component)
   test_component.deconstruct(parts)

   impact_dict = {'C3':Impacts.from_parent(test_component), 
                  'C4':Impacts.from_parent(test_component), 
                  'D':Impacts.from_parent(test_component)}
   for waste in test_component.get_waste_products():
      for lc_stage, impacts_lst in waste.get_impacts().items():
         if impacts_lst:
            for impact in impacts_lst:
               impact_dict[lc_stage] += impact

   output_dict[test_name] = {'test name':test_name}
   test_status = True
   for lc_stage, impact in impact_dict.items():
      for impact_cat in impact_categories:
         if impact_cat +'_' +  lc_stage in test_data_dict[test_name]:
            impacts = impact_dict[lc_stage]
            computed = impacts.get_record(impact_cat)
            reference = float(test_data_dict[test_name][impact_cat + '_' + lc_stage])
            if reference > 0.0 and computed > 0.0:
               dif = abs(computed - reference) / ((computed + reference) / 2 )  # symmetric difference
            else:
               dif = 0.0
            
            output_dict[test_name][impact_cat + '(' + impact_categories[impact_cat] + lc_stage + ')' + ' Python tool'] = computed
            output_dict[test_name][impact_cat + '(' + impact_categories[impact_cat] + lc_stage + ')' + ' Excel tool'] = reference
            output_dict[test_name][impact_cat + lc_stage + '_difference (%)'] = dif * 100

            if dif * 100 > 0.5:
                  test_status = False
                  print(f"{test_name} failed on {impact_cat} with a difference of {dif * 100:.2f}%")
                  print(f"computed impact value: {computed} {impact_categories[impact_cat]}")
                  print(f"expected impact value: {reference} {impact_categories[impact_cat]}")

   output_dict[test_name]['test status'] = 'PASS' if test_status else 'FAIL'


DataImporter.dict_to_csv(output_dict, output_file) 
