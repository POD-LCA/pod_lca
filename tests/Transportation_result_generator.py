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
            travel_dist = string (row["travel_dist_scenario"])
            return_trip_factor = clean(row["return_trip_factor"])
            dist_unit = clean(row["unit"])
            mode_name = clean(row["mode"])
            feul_type = clean(row["feul"])
            mode_dms_name = clean(row["domestic_mode"])
            efficiency = clean(row["efficiency"])
            efficiency_dms = clean(row["efficiency_dms"])

            # Build project
            project = ProjectLogisticManager(
                name="Building A",
                shipping_dest=shipping_dest,
                shipping_org=shipping_org
            )

            # Create link
            project.create_link(
                material=material,
                qty=qty,
                travel_dist=travel_dist,
                return_trip_factor=return_trip_factor,
                dist_unit=dist_unit,
                mode_name=mode_name,
                feul_type=feul_type,
                mode_dms_name=mode_dms_name,
                efficiency=efficiency,
                efficiency_dms=efficiency_dms
            )

            # Collect outputs
            impact_dict = project.get_links()[0].get_impact().get_impact_dict()
            distances = project.get_links()[0].get_travel_dist()

            # Combine input and output into one row
            result_row = row.to_dict()
            result_row.update(impact_dict)
            result_row.update({
                "Domestic_distance_km": distances.get("Domestic", None),
                "Foreign_distance_km": distances.get("Foreign", None)
            })

            all_results.append(result_row)

        except Exception as e:
            print(f"Error processing row: {row.to_dict()}\n{e}")

    # Save results
    df_results = pd.DataFrame(all_results)
    df_results.to_csv(output_csv_path, index=False)
    print(f"Results saved to: {output_csv_path}")


if __name__ == "__main__":
    test_file_path = r"C:\Users\mhtaba\Desktop\transportation_test_file.csv"
    output_csv_path = r"C:\Users\mhtaba\Desktop\transportation_result_file.csv"
    run_test_files(test_file_path, output_csv_path)
