from tqdm import tqdm
import time
import uuid

from pod_lca.units import KILO
from pod_lca.units import KILOMETER
from pod_lca.units import M_TON
from pod_lca.units import WATT_HOUR
from pod_lca.location import Location
from pod_lca.materials_screening import Product
from pod_lca.transportation import USDomesticTransportationManager
from pod_lca.transportation import ElectricTransportMode
from pod_lca.utilities import config
from pod_lca.utilities import DataImporter
from pod_lca.utilities import DataExporter

# ================================================
# INSTRUCTIONS
# ================================================
# Follow the instruction for generating the data set for the version-of-record 

# 1. Run tests/transportation_domestic-test_script.py. If all tests pass, you are ready to generate the dataset.
# 2. Check the output file location and make sure the their is no existing file of same name, or if exists, it is empty.
# 3. Set the version_of_record parameter to True
# 4. Run the script

output_file = "save_files\\transportation_dataset_domestic.csv"
version_of_record = False

states_list = list(DataImporter.json_to_dict(config["file_paths"]["transportation"]["CFS_STATE_CODE"]).keys())
origin_states = [None] + states_list
destination_states = [None] + states_list

tranpsort_scenarios = ["Local", "Achievable", "Conservative"]
Material_names = {
    "10": {"SCTG code": "10", "material": "monumental or building stone"},
    "11": {"SCTG code": "11", "material": "natural sands"},
    "12": {"SCTG code": "12", "material": "gravel and crushed stone (excludes dolomite and slate)"},
    "13": {"SCTG code": "13", "material": "other non-metallic minerals not elsewhere classified"},
    "19": {"SCTG code": "19", "material": "other coal and petroleum products, not elsewhere classified"},
    "23": {"SCTG code": "23", "material": "other chemical products and preparations"},
    "24": {"SCTG code": "24", "material": "plastics and rubber"},
    "25": {"SCTG code": "25", "material": "logs and other wood in the rough"},
    "26": {"SCTG code": "26", "material": "wood products"},
    "31": {"SCTG code": "31", "material": "non-metallic mineral products"},
    "32": {"SCTG code": "32", "material": "base metal in primary or semi-finished forms and in finished basic shapes"},
    "33": {"SCTG code": "33", "material": "articles of base metal"},
    "34": {"SCTG code": "34", "material": "machinery"},
}
qty = 1
unit = M_TON

travel_modes = ["Truck", "Rail", "Air", "Barge", "E_Truck"]
travel_mode_efficiency = ["Low", "Median", "High"]

project = USDomesticTransportationManager.new("Building A")
project.set_data_generator_mode()
project.set_impact_database(r'data/transportation_podlca_emission.csv')
electricity_report_unit = KILO * WATT_HOUR

impact_categories = config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"]
emission_inventories = config["setup"]["INVENTORY_ITEMS"]["EMISSION_INVENTORIES"]

last_save_time = time.time()

sequence_no = 1
for sctg_code, material in Material_names.items():
    material = material["material"]
    print(material)
    product = Product()
    product.set_name(material)
    product.set_qty(qty)
    product.set_unit(unit)
    product.set_sctg_code(sctg_code)

    output_dict = {}
    for origin_state in tqdm(origin_states):
        for destination_state in destination_states:
            if destination_state is None and origin_state is not None:
                continue
            origin_state_obj = Location.from_US_state(origin_state) if origin_state is not None else None
            destination_state_obj = Location.from_US_state(destination_state) if destination_state is not None else None
            scenarios = tranpsort_scenarios if origin_state is None else ['N/A']
            
            project.add_good(product, 
                            None,
                            destination_state_obj, 
                            origin_state_obj,
                            None,
                            KILOMETER)  
            transport_leg = project.get_transportation_leg(product)[0] 
            for travel_mode in travel_modes:             
                for scenario in scenarios:
                    transport_leg.set_transport_scenario(scenario)
                    for eff in travel_mode_efficiency:
                        transport_leg.set_mode(travel_mode, efficiency=eff)
                        try:
                            distance = transport_leg.get_travel_dist()
                            RTT = project.transport_legs[product][0].get_return_trip_factor()
                            impacts = project.get_impacts(product)
                            emissions = project.get_emissions(product)

                            if isinstance(transport_leg.get_mode(), ElectricTransportMode):
                                electricity_consumption, electricity_consumption_unit = (
                                    transport_leg.get_mode().get_electricity_consumption()
                                )
                                conversion_factor = electricity_consumption_unit.convert_to(electricity_report_unit)
                                electricity_consumption *= conversion_factor
                            else:
                                electricity_consumption = 0.0
                        except:
                            continue

                        output_dict[str(sequence_no)] = {
                            **({"uuid": uuid.uuid4()} if version_of_record else {}),
                            'Material': material,
                            'SCTG code': product.get_sctg_code(digits=2),
                            'Scenario scope': 'Domestic',
                            'scenario': transport_leg.get_transport_scenario(),
                            'destination state':destination_state, 
                            'origin state': origin_state,
                            'FAF foreign zone': 'N/A',
                            'dms_orig_port': 'N/A',
                            'domestic mode': travel_mode, 
                            'domestic mode efficiency': eff,
                            'domestic distance (km)': distance,
                            'foreign mode': 'N/A', 
                            'foreign mode efficiency': 'N/A',
                            'foreign distance (km)': 'N/A',
                            'return trip factor': RTT,
                            f'electricity consumption ({electricity_report_unit.get_standard_notation()})': electricity_consumption}
                        
                        for impact_cat in impact_categories:
                            output_dict[str(sequence_no)][
                                impact_cat + " (" + impact_categories[impact_cat] + "/ tonne)"
                            ] = ("NO DATA" if impacts is None else impacts.get_record(impact_cat))
                        for emission in emission_inventories:
                            output_dict[str(sequence_no)][
                                emission + " (" + emission_inventories[emission] + "/ tonne)"
                            ] = ("NO DATA" if emissions is None else emissions.get_record(emission))

                        for impact_cat in impact_categories:
                            output_dict[str(sequence_no)][
                                impact_cat + "_domestic (" + impact_categories[impact_cat] + "/ km * tonne)"
                            ] = (
                                "NO DATA"
                                if impacts is None
                                else transport_leg.get_mode().get_unit_impacts().get_record(impact_cat)
                            )
                        for emission in emission_inventories:
                            output_dict[str(sequence_no)][
                                emission + "_domestic (" + emission_inventories[emission] + "/ km *  tonne)"
                            ] = (
                                "NO DATA"
                                if emissions is None
                                else transport_leg.get_mode().get_unit_emissions().get_record(emission)
                            )

                        sequence_no += 1

                    if transport_leg.get_transport_scenario() == 'No Scenario':
                        break
                
    DataExporter.dict_to_csv(output_dict, output_file, append=True)
    print(f"\n Backup written at {time.strftime('%H:%M:%S')}")
