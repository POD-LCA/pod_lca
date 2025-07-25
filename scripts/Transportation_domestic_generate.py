
from tqdm import tqdm
import time

from pod_lca.units import KILO
from pod_lca.units import KILOMETER
from pod_lca.units import M_TON
from pod_lca.units import WATT_HOUR
from pod_lca.location import Location
from pod_lca.material_screening import Product
from pod_lca.transportation import USDomesticTransportationManager
from pod_lca.transportation import ElectricTransportMode
from pod_lca.utilities import config
from pod_lca.utilities import DataImporter


output_file = "save_files\\transportation_dataset_temp.csv"

states_list = list(DataImporter.json_to_dict(config['file_paths']['transportation']['CFS_STATE_CODE']).keys())

origin_states = [None] + states_list
destination_states = [None] + states_list

tranpsort_scenarios = ["National", "Regional_c", "Regional", "Local", "Average"]
Material_names = DataImporter.csv_to_dict(r'data/transportation_cf_sctg-codes.csv', primary_key='SCTG code')
qty = 1
unit = M_TON

travel_modes = ["Truck", "Rail", "Air", "Barge", "E_Truck"]
travel_mode_efficiency = ["Low", "Median", "High"]

project = USDomesticTransportationManager.new("Building A")
project.set_impact_database(r'data/transportation_podlca_emission.csv')
electricity_report_unit = KILO * WATT_HOUR

impact_categories = config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']
emission_inventories = config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES']

last_save_time = time.time()

output_dict = {}
sequence_no = 1
for sctg_code, material in Material_names.items():
    material = material['material']
    print(material)
    product = Product()
    product.set_name(material)
    product.set_qty(qty)
    product.set_unit(unit)
    product.set_sctg_code(sctg_code)

    for origin_state in tqdm(origin_states):
        for destination_state in destination_states:
            origin_state_obj = Location.from_US_state(origin_state) if not origin_state is None else None
            destination_state_obj = Location.from_US_state(destination_state) if not destination_state is None else None
            scenarios = tranpsort_scenarios if (destination_state is None or  origin_state_obj is None) else ["Average"]
            
            project.add_good(product, 
                            None,
                            destination_state_obj, 
                            origin_state_obj,
                            None,
                            KILOMETER)  
            transport_leg = project.get_transportation_leg(product)[0]              
            for scenario in scenarios:
                transport_leg.set_transport_scenario(scenario)
                for travel_mode in travel_modes:
                    for eff in travel_mode_efficiency:
                        transport_leg.set_mode(travel_mode, efficiency=eff)
                        try:
                            distance = transport_leg.get_travel_dist()
                            RTT =  project.transport_legs[product][0].get_return_trip_factor()
                            impacts = project.get_impacts(product)
                            emissions = project.get_emissions(product)

                            if isinstance(transport_leg.get_mode(), ElectricTransportMode):
                                electricity_consumption, electricity_consumption_unit = transport_leg.get_mode().get_electricity_consumption() 
                                conversion_factor = electricity_consumption_unit.convert_to(electricity_report_unit)
                                electricity_consumption *= conversion_factor
                            else:
                                electricity_consumption = 0.0
                        except:
                            distance = 'NO DATA'
                            RTT = 'NO DATA'
                            impacts = None
                            emissions = None
                            electricity_consumption = 'NO DATA'

                        output_dict[str(sequence_no)] = {  
                            'material': material,
                            'scenario': scenario,
                            'destination state':destination_state, 
                            'origin state': origin_state,
                            'SCTG code': product.get_sctg_code(digits=2), 
                            'domestic mode': travel_mode, 
                            'domestic mode efficiency': eff,
                            'domestic distance (km)': distance,
                            'return trip factor': RTT,
                            f'electricity consumption ({electricity_report_unit.get_standard_notation()})': electricity_consumption}
                        
                        for impact_cat in impact_categories:
                            output_dict[str(sequence_no)][impact_cat + '(' + impact_categories[impact_cat] + ')'] = 'NO DATA' if impacts is None else impacts.get_record(impact_cat)
                        for emission in emission_inventories:
                            output_dict[str(sequence_no)][emission + '(' + emission_inventories[emission] + ')'] = 'NO DATA' if emissions is None else  emissions.get_record(emission)

                        sequence_no += 1

                        # Periodically save to file every 10 minutes
                        current_time = time.time()
                        if current_time - last_save_time >= 600: 
                            DataImporter.dict_to_csv(output_dict, output_file)
                            print(f"\n Backup written at {time.strftime('%H:%M:%S')}")
                            last_save_time = current_time

DataImporter.dict_to_csv(output_dict, output_file)
