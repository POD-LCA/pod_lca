
from lca_modules.location.location import Location
from lca_modules.material.project_manager import Project 
from utilities.data_imports.data_importer import Data_Importer
from utilities.settings import config
from utilities.units.common_units import WATT_HOUR
from utilities.units.metric_prefixes import KILO, MEGA

from tqdm import tqdm

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

# This script generates a CSV file with electricity data for different cities, years, and scenarios.

city_list = ['Seattle', 'Portland', 'Los Angeles', 'Denver', 'Chicago', 'Atlanta']

year_list = [2025, 2030, 2035, 2040, 2045, 2050]
scenario_list = ['MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035']
qty = 1
unit = MEGA * WATT_HOUR

output_file = "save_files\\electricity_city_values.csv"

my_manufacturing_project = Project()
output_dict = {}

impact_categories = config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']
emission_inventories = config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES']

sequence_no = 1
for city in tqdm(city_list):
    my_factory_location = Location.from_str(city)
    my_manufacturing_project.set_location(my_factory_location)
    model_one = my_manufacturing_project.add_model("model_01")

    for year in year_list:
        for scenario in scenario_list:

            electricity = model_one.add_electricity(name="Electricity", stage="A3", qty=1, unit=unit)
            electricity.set_year(year)
            electricity.set_scenario(scenario)
            output_dict[str(sequence_no)] = { 
                                                'city': city,
                                                'Zip Code': my_factory_location.get_zip(), 
                                                'spatial resolution': electricity.get_supplier().get_spatial_resolution(), 
                                                'year': year, 
                                                'cambium_scenario': scenario,
                                                'qty': qty, 
                                                'unit': unit.get_standard_notation()}
                                                    
            impacts = electricity.get_impacts()
            emissions = electricity.get_emissions()
            
            for impact_cat in impact_categories:
                output_dict[str(sequence_no)][impact_cat + '(' + impact_categories[impact_cat] + ')'] = impacts.get_record(impact_cat)
            for emission in emission_inventories:
                output_dict[str(sequence_no)][emission + '(' + emission_inventories[emission] + ')'] = emissions.get_record(emission)
            sequence_no += 1

Data_Importer.dict_to_csv(output_dict, output_file)
