from tqdm import tqdm

from pod_lca.impacts import openLCA
from pod_lca.units import JOULE
from pod_lca.units import MEGA
from pod_lca.utilities import DataExporter
from pod_lca.utilities import DataImporter

# ================================================
# INSTRUCTIONS
# ================================================
# The following steps shall be followed to create the connection between POD|LCA Python framework and the OpenLCA application.

# 1. Open the OpenLCA application
# 2. Import the database into OpenLCA. The following is the procedure to import source data from a zip file (for importing a database from zolca files or other means, refer to the OpenLCA manual).
#    It is also necessary to import and customize the desired LCIA impact evaluation methods to the database
#       2a. Database > New Database > From scratch
#       2b. In the pop-up enter the database name and set ‘Database content’ as ‘Complete reference units’
#       2c. On the navigation panel, select and right-click on the database created and select import > Other…
#       2d. Select ‘Linked Data (JSON-LD)’ and follow the instructions to import the *.zip file. Select ‘update data sets with newer versions’
# 3. Start up the Inter-Process Communication (IPC) server.
#    The database intended for impact evaluation must be open before starting the IPC server.
#       3a. Tools > Developer Tools > IPC Server
#       3b. Set Port to 8080
#       3c. Click the green arrow
# 4. Set the IMPACT_SOURCE_DATABASE variable in the config file to 'FLCAC' or 'ecoinvent', as necessary.
# 5. Run this script


def test_impacts_olca():
    test_data = "tests\\impacts_test-olca-ecoinvent_test-values.csv"
    output_file = "tests\\impacts_test-olca-ecoinvent_test_report.csv"

    IMPACT_SOURCE_DATABASE = "ecoinvent391"

    openLCA_client = openLCA.set_connection()

    ## process list
    # The first three processes use wood chips as a material (i.e., should use "ecoinvent391_renewable_fuels_NoWoodChips.csv" for the renewable fuels group)
    # The second three processes use wood chips as a fuel (i.e., should use "ecoinvent_renewable_fuels.csv" for the renewable fuels group)
    # There are also three random processes that had non-zero impacts for all three energy groups
    # Last, there is one waste treatment process.
    test_uuid_list = [
        "d1b276b6-52ab-40e8-87bc-4b03fa60526f",
        "7ad46f7a-6a93-46f0-9ca6-0c1b00bbd8cd",
        "6073fd6f-cb0b-4a4d-929d-e8a76cb724eb",
        "298c276b-945c-4d3a-b60c-a6bfeef40b17",
        "7d2e92e1-0685-4cdc-8b3b-d979c438c9f4",
        "30fa5314-9576-4a4a-a8f1-5aafc1f90c27",
        "faf039df-118b-4349-9a3d-1b6254d401eb",
        "917f0e08-7e3d-4a2a-b346-2176da0233e4",
        "7056ed6b-fe1a-4d53-971f-0d1682fb1eb9",
        "17f339b3-ac5f-4658-9203-be30b7fdb983",
    ]

    test_process_list = openLCA.get_process_list(openLCA_client, test_uuid_list)

    # inventories (impacts and emissions)
    impact_categories = DataImporter.json_to_dict("./data/impacts_" + IMPACT_SOURCE_DATABASE + "_categories.json")
    emission_inventories = DataImporter.json_to_dict(
        "./data/impacts_" + IMPACT_SOURCE_DATABASE + "_emission-inventories.json"
    )

    # impact method
    impact_method_uuid = "5d5b2a0c-0a99-48d4-93e9-2f2b9d852655"

    # impact groupings
    renewable_fuels_process_list = DataImporter.csv_to_list(
        "./data/impacts_" + IMPACT_SOURCE_DATABASE + "_renewable-fuels-group.csv", column_header="UUID"
    )
    nonrenewable_fuels_process_list = DataImporter.csv_to_list(
        "./data/impacts_" + IMPACT_SOURCE_DATABASE + "_nonrenewable-fuels-group.csv", column_header="UUID"
    )
    heating_values = DataImporter.csv_to_dict(
        "./data/impacts_" + IMPACT_SOURCE_DATABASE + "_heating-values.csv", "UUID"
    )

    electricity_process_list = DataImporter.csv_to_list(
        "./data/impacts_ecoinvent391_electricity-group.csv", column_header="UUID"
    )
    group_by = [
        {
            "name": "electricity",
            "ids": electricity_process_list,
            "unit": MEGA * JOULE,
            "conversion_map": heating_values,
        },
        {
            "name": "nonrenewable fuel combustion",
            "ids": nonrenewable_fuels_process_list,
            "unit": MEGA * JOULE,
            "conversion_map": heating_values,
        },
        {
            "name": "renewable fuel combustion",
            "ids": renewable_fuels_process_list,
            "unit": MEGA * JOULE,
            "conversion_map": heating_values,
        },
    ]

    results = openLCA.generate_impacts_dir(
        openLCA_client, test_process_list, impact_categories | emission_inventories, impact_method_uuid, group_by
    )

    # Note: When using ecoinvent391, renewable fuel group contributions need to be recalculated for all processes that use wood chips as a raw material (instead of fuel).
    # wood chips: (uuids: d47a4435-3089-4263-af99-8611eed2698c, 7fe99768-d571-4bc2-a272-7df585bd0d48)
    uuid_list_with_wood_chips = DataImporter.csv_to_list(
        "./data/impacts_ecoinvent391_uuid-list-with-wood-chips.csv", column_header="UUID"
    )
    test_uuid_list_with_chips = [uuid for uuid in test_uuid_list if uuid in uuid_list_with_wood_chips]
    process_list = openLCA.get_process_list(openLCA_client, test_uuid_list_with_chips)

    renewable_fuels_process_list = DataImporter.csv_to_list(
        "./data/impacts_ecoinvent391_renewable-fuels-group-no-wood-chips.csv", column_header="UUID"
    )

    group_by = [
        {
            "name": "renewable fuel combustion",
            "ids": renewable_fuels_process_list,
            "unit": MEGA * JOULE,
            "conversion_map": heating_values,
        }
    ]

    results_with_wood_chips = openLCA.generate_impacts_dir(
        openLCA_client, process_list, impact_categories | emission_inventories, impact_method_uuid, group_by
    )

    for uuid in results_with_wood_chips:
        if uuid in results:
            for inventory in impact_categories | emission_inventories:
                results[uuid]["renewable fuel combustion_" + inventory] = results_with_wood_chips[uuid][
                    "renewable fuel combustion_" + inventory
                ]

    # test results
    output_dict = {}
    test_dict = DataImporter.csv_to_dict(test_data, "UUID")
    tests_total = 0
    tests_passed = 0
    for uuid in tqdm(test_dict):
        test = test_dict[uuid]
        output_dict[uuid] = {
            "Category": test["Category"],
            "Name": test["Name"],
            "UUID": test["UUID"],
            "Location": test["Location"],
            "Process Type": test["Process Type"],
            "Description": test["Description"],
            "Unit": test["Unit"],
        }

        test_status = True
        for impact_category in impact_categories:
            key = impact_category + " [" + impact_categories[impact_category]["refUnit"] + "]"
            output_dict[uuid][impact_category + "test"] = float(test[key])
            output_dict[uuid][impact_category + "result"] = results[test["UUID"]][key]

            if abs(float(test[key])) > 0.0:
                diff = abs(float(test[key]) - results[test["UUID"]][key]) / float(test[key])
            else:
                diff = 0.0

            if diff > 0.01:
                test_status = False

        for header in ["electricity_", "nonrenewable fuel combustion_", "renewable fuel combustion_"]:
            for impact_category in impact_categories:
                output_dict[uuid][header + impact_category + "test"] = float(test[header + impact_category])
                output_dict[uuid][header + impact_category + "result"] = results[test["UUID"]][header + impact_category]

                if abs(float(test[header + impact_category])) > 0.0:
                    diff = abs(
                        float(test[header + impact_category]) - results[test["UUID"]][header + impact_category]
                    ) / float(test[header + impact_category])
                else:
                    diff = 0.0

                if diff > 0.01:
                    test_status = False

            output_dict[uuid][header + "qty" + "_test"] = float(test[header + "qty"])
            output_dict[uuid][header + "qty" + "_result"] = results[test["UUID"]][header + "qty"]

            if abs(float(test[header + "qty"])) > 0.0:
                diff = abs(float(test[header + "qty"]) - results[test["UUID"]][header + "qty"]) / float(
                    test[header + "qty"]
                )
            else:
                diff = 0.0

            if diff > 0.01:
                test_status = False

            output_dict[uuid][header + "unit" + "_test"] = test[header + "unit"]
            output_dict[uuid][header + "unit" + "_result"] = results[test["UUID"]][header + "unit"]

        output_dict[uuid]["status"] = "PASS" if test_status else "FAIL"

        tests_total += 1
        if test_status:
            tests_passed += 1

    DataExporter.dict_to_csv(output_dict, output_file)
    print(f"Olca impacts tests passed: {tests_passed} of {tests_total}")

    assert tests_passed == tests_total


if __name__ == "__main__":
    pass
