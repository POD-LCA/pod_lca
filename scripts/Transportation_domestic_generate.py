
from tqdm import tqdm
from time import time

from pod_lca.units import KILOMETER
from pod_lca.units import M_TON
from pod_lca.location import Location
from pod_lca.material_screening import Master
from pod_lca.transportation import ProjectLogisticManager
from pod_lca.transportation import CFSDataset
from pod_lca.utilities import config
from pod_lca.utilities import DataImporter


output_file = "save_files\\transportation_dataset_temp.csv"

origin_states = [None, "Washington", "California"]
destination_states = [None, "Colorado", "Illinois"]

tranpsort_scenarios = ["National", "Regional", "Regional_c", "Local"]
Material_names = ["Photovoltaics", "Aggregates", "Cement", "Glass", "Piping"]
qty = 1
unit = M_TON

travel_modes = ["Truck", "Rail", "Air", "Barge"]
travel_mode_efficiency = ["Low", "Median", "High"]
travel_fuel_types = ["Regular"]

project = ProjectLogisticManager.new("Building A")
project.set_database(r'data/transportation_podlca_emission.csv')

impact_categories = config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']
emission_inventories = config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES']

output_dict = {}
sequence_no = 1
for material in Material_names:
    print(material)
    product = Master()
    product.set_name(material)
    product.set_qty(qty)
    product.set_unit(unit)

    for origin_state in tqdm(origin_states):
        for destination_state in destination_states:
            if not (origin_state == destination_state) or (origin_state is None and destination_state is None):
                origin_state_obj = Location.from_US_state(origin_state) if not origin_state is None else None
                destination_state_obj = Location.from_US_state(destination_state) if not destination_state is None else None
                scenarios = tranpsort_scenarios if (destination_state is None or  origin_state_obj is None) else [None]
                for scenario in scenarios:
                    for travel_mode in travel_modes:
                        for eff in travel_mode_efficiency:
                            for travel_fuel_type in travel_fuel_types:

                                project.add_good(product, 
                                                None,
                                                destination_state_obj, 
                                                origin_state_obj,
                                                scenario,
                                                KILOMETER, 
                                                None, 
                                                travel_mode,
                                                travel_fuel_type, 
                                                eff)

                                try:
                                    distance = project.goods_links_map[product][0].get_travel_dist()
                                    RTT =  project.goods_links_map[product][0].get_return_trip_factor()
                                    impacts = project.get_impacts(product)
                                    emissions = project.get_emissions(product)
                                except:
                                    continue

                                output_dict[str(sequence_no)] = {  
                                    'material': material,
                                    'scenario': scenario,
                                    'destination state':destination_state, 
                                    'origin state': origin_state,
                                    'SCTG code': CFSDataset.get_sctg_code(material), 
                                    'domestic mode': travel_mode, 
                                    'domestic mode efficiency': eff,
                                    'domestic distance (km)': distance,
                                    'return trip factor': RTT}
                                for impact_cat in impact_categories:
                                    output_dict[str(sequence_no)][impact_cat + '(' + impact_categories[impact_cat] + ')'] = impacts.get_record(impact_cat)
                                for emission in emission_inventories:
                                    output_dict[str(sequence_no)][emission + '(' + emission_inventories[emission] + ')'] = emissions.get_record(emission)

                                sequence_no += 1

DataImporter.dict_to_csv(output_dict, output_file)
