
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

import os
import csv
import time

import pandas as pd

from pod_lca.transportation import ProjectLogisticManager
from pod_lca.material_screening import Master
from pod_lca.units import UNITS_MAP
from pod_lca.transportation import DomesticLink, ForeignLink

def clean(value):
    return None if pd.isna(value) else value

def string(value):
    return "None" if pd.isna(value) else value

def run_test_files(test_file_path, output_csv_path):
    test_inputs = pd.read_csv(test_file_path)
    all_results = []
    rows_count = len(test_inputs)

    start_time = time.time()
    last_save_time = start_time

    for _, row in test_inputs.iterrows():

        # Print progress
        progress = (_ + 1) / rows_count * 100
        print(f"Processing row {_ + 1}/{rows_count} - Progress: {progress:.2f}%")
        # Clean all required inputs
        shipping_dest = clean(row["destination"])
        shipping_org = clean(row["origin"])
        material = clean(row["material"])
        qty = clean(row["qty"])
        qty_unit = clean(row["qty_unit"])
        travel_dist = string(row["travel_dist"])
        travel_dist_unit = clean(row["travel_dist_unit"])
        return_trip_factor = clean(row["return_trip_factor"])
        mode_domestic = clean(row["mode_domestic"])
        mode_domestic_fuel_type = clean(row["mode_domestic_fuel_type"])
        mode_domestic_efficiency = clean(row["mode_domestic_efficiency"])
        mode_foreign = clean(row["mode_foreign"])
        mode_foreign_fuel_type = clean(row["mode_foreign_fuel_type"])
        mode_foreign_efficiency = clean(row["mode_foreign_efficiency"])

        project = ProjectLogisticManager.new("Building A")

        # TODO: this to happen inside
        product = Master()
        product.set_name(material)
        product.set_qty(qty)
        product.set_unit(UNITS_MAP[qty_unit])

        
        mode = {'domestic': mode_domestic,
                'foreign': mode_foreign} if travel_dist in ["North_america", "Global", "Known"] else mode_domestic
        mode_fuel_type = {'domestic': mode_domestic_fuel_type,
                            'foreign': mode_foreign_fuel_type} if travel_dist in ["North_america", "Global", "Known"] else mode_domestic_fuel_type
        mode_efficiency = {'domestic': mode_domestic_efficiency,
                            'foreign': mode_foreign_efficiency} if travel_dist in ["North_america", "Global", "Known"] else mode_domestic_efficiency
        if isinstance(travel_dist, str):
            if travel_dist == "None":
                transport_scenario = None
            else:
                transport_scenario = travel_dist
            travel_dist = None
        else:
            travel_dist = travel_dist
            transport_scenario = None

        project.add_goods([product], 
                        shipping_dest, shipping_org,
                        transport_scenario,
                        travel_dist,
                        UNITS_MAP[travel_dist_unit], 
                        return_trip_factor, 
                        mode,
                        mode_fuel_type, 
                        mode_efficiency)
        # Build project
        # truck_1 = project.add_link(link_name="Local_impact", shipping_dest=shipping_dest, shipping_org=shipping_org,
        #                            material=material, qty=qty, qty_unit=qty_unit, travel_dist=travel_dist,
        #                            travel_dist_unit=travel_dist_unit, return_trip_factor=return_trip_factor,
        #                            mode_domestic=mode_domestic, mode_domestic_fuel_type=mode_domestic_fuel_type,
        #                            mode_domestic_efficiency=mode_domestic_efficiency,
        #                            mode_foreign=mode_foreign, mode_foreign_fuel_type=mode_foreign_fuel_type,
        #                            mode_foreign_efficiency=mode_foreign_efficiency)

        # truck_1.compute_impact()
        print(project.get_impacts())

        # if isinstance(, Domestic)
        distances = {}
        domestic_impact = None
        foreign_impact = None
        for link in project.get_link(product):
            if isinstance(link, DomesticLink):
                domestic_impact = link.get_impact()
                domestic_mode_impact = link.get_mode().get_unit_impacts()
                distances['domestic'] = link.get_travel_dist()
            elif isinstance(link, ForeignLink):
                foreign_impact = link.get_impact()
                foreign_mode_impact = link.get_mode().get_unit_impacts()
                distances['foreign'] = link.get_travel_dist()

        # try:
        #     new_domestic_mode = truck_1.get_mode_domestic().get_name()
        # except Exception:
        #     new_domestic_mode = None

        # try:
        #     new_foreign_mode = truck_1.get_mode_foreign().get_name()
        # except Exception:
        #     new_foreign_mode = None

        # try:
        #     new_destination = truck_1.get_shipping_dest().get_state()
        # except Exception:
        #     new_destination = None

        # try:
        #     new_shipping_org = truck_1.get_shipping_org().get_state()
        # except Exception:
        #     new_shipping_org = None

        # try:
        #     return_trip_factor = truck_1.get_return_trip_factor()
        # except Exception:
        #     return_trip_factor = None

        # try:
        #     electricity = truck_1.get_electricity_consumption()
        # except Exception:
        #     electricity = None

        # Combine input and output into one row
        result_row = row.to_dict()
        
        if domestic_impact is not None:
            domestic_impact_prefixed = {f"Domestic_{k}": v for k, v in domestic_impact.get_record_dict().items()}
            domestic_mode_impact_prefixed = {f"Domestic_mode_{k}": v for k, v in domestic_mode_impact.get_record_dict().items()} if domestic_mode_impact else {f"Domestic_mode_{k}": None for k, v in foreign_mode_impact.get_record_dict().items()}
            result_row.update(domestic_impact_prefixed)
            result_row.update(domestic_mode_impact_prefixed)
        if foreign_impact is not None:
            foreign_impact_prefixed = {f"Foreign_{k}": v for k, v in foreign_impact.get_record_dict().items()}
            foreign_mode_prefixed = {f"Foreign_mode_{k}": v for k, v in foreign_mode_impact.get_record_dict().items()} if foreign_mode_impact else {f"Foreign_mode_{k}": None for k, v in domestic_mode_impact.get_record_dict().items()}
            result_row.update(foreign_impact_prefixed)
            result_row.update(foreign_mode_prefixed)

        result_row.update({
            "Domestic_distance_km": distances.get("Domestic", None),
            "Foreign_distance_km": distances.get("Foreign", None)
        })

        # result_row.update({"New_destination": new_destination})
        # result_row.update({"New_shipping_org": new_shipping_org})

        # result_row.update({"Return_trip_factor": return_trip_factor})
        # result_row.update({"Electricity": electricity})
        # result_row.update({"New_domestic_mode": new_domestic_mode})
        # result_row.update({"New_foreign_mode": new_foreign_mode})

        all_results.append(result_row)

        # Periodically save to file every 10 minutes
        current_time = time.time()
        if current_time - last_save_time >= 600:  # 600 seconds = 10 minutes
            df_partial = pd.DataFrame(all_results)
            df_partial.to_csv(output_csv_path, index=False)
            print(f"Backup written at {time.strftime('%H:%M:%S')}")
            last_save_time = current_time

    # Final save
    df_results = pd.DataFrame(all_results)
    df_results.to_csv(output_csv_path, index=False)
    print(f"Results saved to: {output_csv_path}")


if __name__ == "__main__":
    """
    This script is designed to run a series of tests.
    the input files should be in the form of a CSV file.
    """

    test_file_path = r"tests\transportation_QC_5nd_TEMP.csv"
    output_csv_path = r"tests\transportation_test_report_TEMP.csv"
    run_test_files(test_file_path, output_csv_path)
