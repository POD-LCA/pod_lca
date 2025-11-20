from tqdm import tqdm
import time

from pod_lca.units import KILO
from pod_lca.units import KILOMETER
from pod_lca.units import M_TON
from pod_lca.units import WATT_HOUR
from pod_lca.location import Location
from pod_lca.materials_screening import Product
from pod_lca.transportation import USGlobalTransportationManager
from pod_lca.transportation import ElectricTransportMode
from pod_lca.utilities import config
from pod_lca.utilities import DataImporter
from pod_lca.utilities import DataExporter


output_file = "save_files\\transportation_dataset_global.csv"

states_list = list(DataImporter.json_to_dict(config["file_paths"]["transportation"]["CFS_STATE_CODE"]).keys())

origin_locations = [
    "Canada",
    "Mexico",
    "Rest of America",
    "Europe",
    "Africa",
    "SW & Central Asia",
    "Eastern Asia",
    "SE Asia & Oceania",
]
destination_states = states_list

tranpsort_scenarios = ["Global"]
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

travel_modes = ["Truck", "Rail", "Ocean", "Air"]
travel_mode_efficiency = ["Low", "Median", "High"]

project = USGlobalTransportationManager.new("Building A")
project.get_dataset().force_location = False  # Stops defaulting to closest state
project.get_dataset().force_mode = False  # Stops defaulting to default mode
project.set_impact_database(r"data/transportation_podlca_emission.csv")
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

    for origin in tqdm(origin_locations):
        output_dict = {}  # data dict
        for destination_state in destination_states:
            origin_obj = (
                Location.from_faf_regions(origin) if origin not in ["Canada", "Mexico"] else Location.from_str(origin)
            )
            destination_state_obj = Location.from_US_state(destination_state) if destination_state is not None else None
            scenarios = tranpsort_scenarios
            project.add_good(product, None, destination_state_obj, origin_obj, None, KILOMETER)
            foreign_transport_leg = project.get_transportation_leg(product)[0]
            domestic_transport_leg = foreign_transport_leg.get_domestic_leg()

            for scenario in scenarios:
                foreign_transport_leg.set_transport_scenario(scenario)
                if origin not in ["Canada", "Mexico"]:
                    travel_modes = ["Ocean", "Air"]
                for foreign_travel_mode in travel_modes:
                    for foreign_travel_eff in travel_mode_efficiency:
                        foreign_transport_leg.set_mode(foreign_travel_mode, efficiency=foreign_travel_eff)
                        local_travel_modes = (
                            ["Truck", "E_Truck", "Rail", "Air"]
                            if foreign_travel_mode == "Ocean"
                            else [foreign_travel_mode]
                        )
                        for local_travel_mode in local_travel_modes:
                            local_travel_mode_efficiencies = (
                                [foreign_travel_eff]
                                if local_travel_mode == foreign_travel_mode
                                else travel_mode_efficiency
                            )
                            for local_travel_eff in local_travel_mode_efficiencies:
                                domestic_transport_leg.set_mode(local_travel_mode, efficiency=local_travel_eff)
                                domestic_port = (
                                    destination_state_obj.get_us_coast()
                                    if destination_state is not None and foreign_travel_mode == "Ocean"
                                    else "N/A"
                                )

                                try:
                                    foreign_distance = foreign_transport_leg.get_travel_dist()
                                    domestic_distance = domestic_transport_leg.get_travel_dist()
                                    RTT = project.transport_legs[product][0].get_return_trip_factor()
                                    impacts = project.get_impacts(product)
                                    emissions = project.get_emissions(product)

                                    if isinstance(foreign_transport_leg.get_mode(), ElectricTransportMode):
                                        electricity_consumption, electricity_consumption_unit = (
                                            foreign_transport_leg.get_mode().get_electricity_consumption()
                                        )
                                        conversion_factor = electricity_consumption_unit.convert_to(
                                            electricity_report_unit
                                        )
                                        electricity_consumption *= conversion_factor
                                    else:
                                        electricity_consumption = 0.0
                                except:
                                    continue
                                    # foreign_distance = 'NO DATA'
                                    # domestic_distance = 'NO DATA'
                                    # RTT = 'NO DATA'
                                    # impacts = None
                                    # emissions = None
                                    # electricity_consumption = 'NO DATA'

                                output_dict[str(sequence_no)] = {
                                    "Material": material,
                                    "SCTG code": product.get_sctg_code(digits=2),
                                    "Scenario scope": "Global",
                                    "scenario": "US_Average" if scenario == "Average" else scenario,
                                    "destination state": destination_state,
                                    "origin state": "N/A",
                                    "FAF foreign zone": origin,
                                    "dms_orig_port": domestic_port,
                                    "foreign mode": foreign_travel_mode,
                                    "domestic mode": local_travel_mode,
                                    "domestic mode efficiency": local_travel_eff,
                                    "foreign mode efficiency": foreign_travel_eff,
                                    "foreign distance (km)": foreign_distance,
                                    "domestic distance (km)": domestic_distance,
                                    "return trip factor": RTT,
                                }

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
                                        impact_cat + "_foreign (" + impact_categories[impact_cat] + "/ km * tonne)"
                                    ] = (
                                        "NO DATA"
                                        if impacts is None
                                        else foreign_transport_leg.get_mode().get_unit_impacts().get_record(impact_cat)
                                    )
                                for emission in emission_inventories:
                                    output_dict[str(sequence_no)][
                                        emission + "_foreign (" + emission_inventories[emission] + "/ km *  tonne)"
                                    ] = (
                                        "NO DATA"
                                        if emissions is None
                                        else foreign_transport_leg.get_mode().get_unit_emissions().get_record(emission)
                                    )

                                for impact_cat in impact_categories:
                                    output_dict[str(sequence_no)][
                                        impact_cat + "_domestic (" + impact_categories[impact_cat] + "/ km * tonne)"
                                    ] = (
                                        "NO DATA"
                                        if impacts is None
                                        else domestic_transport_leg.get_mode().get_unit_impacts().get_record(impact_cat)
                                    )
                                for emission in emission_inventories:
                                    output_dict[str(sequence_no)][
                                        emission + "_domestic (" + emission_inventories[emission] + "/ km *  tonne)"
                                    ] = (
                                        "NO DATA"
                                        if emissions is None
                                        else domestic_transport_leg.get_mode().get_unit_emissions().get_record(emission)
                                    )

                                sequence_no += 1

        DataExporter.dict_to_csv(output_dict, output_file, append=True)
        print(f"\n Backup written at {time.strftime('%H:%M:%S')}")


# DataExporter.dict_to_csv(output_dict, output_file)
