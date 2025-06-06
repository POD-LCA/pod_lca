from lca_modules.transportation.project_logistic_manager import ProjectLogisticManager
import pandas as pd

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"


def clean(value):
    return None if pd.isna(value) else value

def string (value):
    return "None" if pd.isna(value) else value

def run_test_files(test_file_path, output_csv_path):
    test_inputs = pd.read_csv(test_file_path)
    all_results = []

    for _, row in test_inputs.iterrows():
        try:
            # Clean all required inputs
            shipping_dest = clean(row["destination"])
            shipping_org = clean(row["origin"])
            material = clean(row["material"])
            qty = clean(row["qty"])
            qty_unit = clean(row["qty_unit"])
            travel_dist = string (row["travel_dist"])
            travel_dist_unit = clean(row["travel_dist_unit"])
            return_trip_factor = clean(row["return_trip_factor"])
            mode_domestic = clean(row["mode_domestic"])
            mode_domestic_fuel_type = clean(row["mode_domestic_fuel_type"])
            mode_domestic_efficiency = clean(row["mode_domestic_efficiency"])
            mode_foreign = clean(row["mode_foreign"])
            mode_foreign_fuel_type = clean(row["mode_foreign_fuel_type"])
            mode_foreign_efficiency = clean(row["mode_foreign_efficiency"])

            project = ProjectLogisticManager.new("Building A")
            # Build project
            truck_1 = project.add_link (link_name = "QC_Impact", shipping_dest = shipping_dest, shipping_org = shipping_org,
                                        material = material, qty = qty, qty_unit = qty_unit, travel_dist = travel_dist,
                                        travel_dist_unit = travel_dist_unit , return_trip_factor = return_trip_factor, mode_domestic = mode_domestic,
                                        mode_domestic_fuel_type = mode_domestic_fuel_type, mode_domestic_efficiency= mode_domestic_efficiency,
                                        mode_foreign= mode_foreign, mode_foreign_fuel_type = mode_foreign_fuel_type, mode_foreign_efficiency = mode_foreign_efficiency)

            truck_1.compute_impact()
            domestic_impact = truck_1.get_impact_domestic().get_impact_dict()
            foreign_impact = truck_1.get_impact_foreign().get_impact_dict()
            distances = truck_1.get_link_distances()
            return_trip_factor = truck_1.get_return_trip_factor()
            electricity = truck_1.get_electricity_consumption()


            # Combine input and output into one row
            result_row = row.to_dict()
            domestic_impact_prefixed = {f"Domestic_{k}": v for k, v in domestic_impact.items()}
            foreign_impact_prefixed = {f"Foreign_{k}": v for k, v in foreign_impact.items()}

            result_row.update(domestic_impact_prefixed)
            result_row.update(foreign_impact_prefixed)
            result_row.update({
                "Domestic_distance_km": distances.get("Domestic", None),
                "Foreign_distance_km": distances.get("Foreign", None)
            })
            result_row.update({"Return_trip_factor": return_trip_factor})
            result_row.update({"Electricity": electricity })

            all_results.append(result_row)

        except Exception as e:
            print(f"Error processing row: {row.to_dict()}\n{e}")

    # Save results
    df_results = pd.DataFrame(all_results)
    df_results.to_csv(output_csv_path, index=False)
    print(f"Results saved to: {output_csv_path}")


if __name__ == "__main__":

    """"
    This script is designed to run a series of tests.
    the input files should be in the form of a CSV file.
    """
    
    test_file_path = r"tests\transportation_QC_5nd.csv"
    output_csv_path = r"tests\transportation_QC_5nd_result.csv"
    run_test_files(test_file_path, output_csv_path)
