
from tqdm import tqdm
from time import time

from pod_lca.units import KILO
from pod_lca.units import KILOMETER
from pod_lca.units import M_TON
from pod_lca.units import WATT_HOUR
from pod_lca.location import Location
from pod_lca.material_screening import Master
from pod_lca.transportation import USDomesticLogisticProject
from pod_lca.transportation import CFSDataset
from pod_lca.transportation import ElectricTransportMode
from pod_lca.utilities import config
from pod_lca.utilities import DataImporter


output_file = "save_files\\transportation_dataset_temp.csv"

states_list = list(DataImporter.json_to_dict(config['file_paths']['transportation']['CFS_STATE_CODE']).keys())

origin_states = [None] + states_list
# destination_states = [None] + states_list
destination_states = ['Alaska']

tranpsort_scenarios = ["National", "Regional_c", "Regional", "Local"]
Material_names = ["Aggregates"]
# Material_names = ["Photovoltaics", "Aggregates", "Cement", "Glass", "Piping"]
qty = 1
unit = M_TON

# travel_modes = ["Truck", "Rail", "Air", "Barge", "E_Truck"]
travel_modes = ["E_Truck"]
travel_mode_efficiency = ["Low", "Median", "High"]

project = USDomesticLogisticProject.new("Building A")
project.set_impact_database(r'data/transportation_podlca_emission.csv')
CFSDataset = project.get_dataset()
electricity_report_unit = KILO * WATT_HOUR

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
                
                project.add_good(product, 
                                None,
                                destination_state_obj, 
                                origin_state_obj,
                                None,
                                KILOMETER)  
                link = project.get_link(product)[0]              
                for scenario in scenarios:
                    link.set_transport_scenario(scenario)
                    for travel_mode in travel_modes:
                        for eff in travel_mode_efficiency:
                            link.set_mode(travel_mode, efficiency=eff)

                            try:
                                distance = link.get_travel_dist()
                                RTT =  project.goods_links_map[product][0].get_return_trip_factor()
                                impacts = project.get_impacts(product)
                                emissions = project.get_emissions(product)

                                if isinstance(link.get_mode(), ElectricTransportMode):
                                    electricity_consumption, electricity_consumption_unit = link.get_mode().get_electricity_consumption() 
                                    conversion_factor = electricity_consumption_unit.convert_to(electricity_report_unit)
                                    electricity_consumption *= conversion_factor
                                else:
                                    0.0
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
                                'return trip factor': RTT,
                                f'electricity consumption ({electricity_report_unit.get_standard_notation()})': electricity_consumption}
                            for impact_cat in impact_categories:
                                output_dict[str(sequence_no)][impact_cat + '(' + impact_categories[impact_cat] + ')'] = impacts.get_record(impact_cat)
                            for emission in emission_inventories:
                                output_dict[str(sequence_no)][emission + '(' + emission_inventories[emission] + ')'] = emissions.get_record(emission)

                            sequence_no += 1

DataImporter.dict_to_csv(output_dict, output_file)
