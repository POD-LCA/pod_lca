__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "etel5501@uw.edu;kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.lca_modules.impacts import openLCA
from pod_lca.units import JOULE
from pod_lca.units import MEGA
from pod_lca.utilities import config
from pod_lca.utilities import DataExporter
from pod_lca.utilities import DataImporter


# ================================================
# IMPACTS AND EMISSIONS SOURCE DATA
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

IMPACT_SOURCE_DATABASE = config["setup"]["impacts"]["IMPACT_SOURCE_DATABASE"]

openLCA_client = openLCA.set_connection()

# process list
process_list_all = openLCA.get_process_list(openLCA_client)
if IMPACT_SOURCE_DATABASE == "FLCAC":
    process_list = process_list_all
elif IMPACT_SOURCE_DATABASE == "ecoinvent391":
    filter_by = [
        "01",
        "02",
        "13",
        "16",
        "17",
        "19",
        "20",
        "22",
        "23",
        "24",
        "25",
        "27",
        "35",
        "36",
        "38",
        "F",
        "H",
        "8292",
    ]
    process_list = openLCA.filter_processes_by(process_list_all, filter_by)

# inventories (impacts and emissions)
impact_categories = DataImporter.json_to_dict("src/pod_lca/data/impacts_" + IMPACT_SOURCE_DATABASE.lower() + "_categories.json")
for impact_category in impact_categories.keys():
    if impact_category not in config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"]:
        raise ValueError(
            f"Impact category '{impact_category}' not recognized. Impact category keys recognized: {config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']}."
        )
    else:
        if (
            config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"][impact_category]
            != impact_categories[impact_category]["refUnit"]
        ):
            raise ValueError(
                f"Impact category '{impact_category}' unit mismatch. Expected: {config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES'][impact_category]}, Found: {impact_categories[impact_category]['refUnit']}"
            )

emission_inventories = DataImporter.json_to_dict(
    "src/pod_lca/data/impacts_" + IMPACT_SOURCE_DATABASE.lower() + "_emission-inventories.json"
)
for emission in emission_inventories.keys():
    if emission not in config["setup"]["INVENTORY_ITEMS"]["EMISSION_INVENTORIES"]:
        raise ValueError(
            f"Impact category '{emission}' not recognized. Impact category keys recognized: {config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES']}."
        )
    else:
        if (
            config["setup"]["INVENTORY_ITEMS"]["EMISSION_INVENTORIES"][emission]
            != emission_inventories[emission]["refUnit"]
        ):
            raise ValueError(
                f"Emission inventory '{emission}' unit mismatch. Expected: {config['setup']['INVENTORY_ITEMS']['EMISSION_INVENTORIES'][emission]}, Found: {emission_inventories[emission]['refUnit']}"
            )

# impact method
if IMPACT_SOURCE_DATABASE == "FLCAC":
    impact_method_uuid = "0ed73bce-2198-4148-8c4d-8b2ce68b6e1a"
elif IMPACT_SOURCE_DATABASE == "ecoinvent391":
    impact_method_uuid = "5d5b2a0c-0a99-48d4-93e9-2f2b9d852655"

# impact groupings
renewable_fuels_process_list = DataImporter.csv_to_list(
    "src/pod_lca/data/impacts_" + IMPACT_SOURCE_DATABASE.lower() + "_renewable-fuels-group.csv", column_header="UUID"
)
nonrenewable_fuels_process_list = DataImporter.csv_to_list(
    "src/pod_lca/data/impacts_" + IMPACT_SOURCE_DATABASE.lower() + "_nonrenewable-fuels-group.csv", column_header="UUID"
)
heating_values = DataImporter.csv_to_dict("src/pod_lca/data/impacts_" + IMPACT_SOURCE_DATABASE.lower() + "_heating-values.csv", "UUID")

if IMPACT_SOURCE_DATABASE == "FLCAC":
    group_by = [
        {"name": "electricity", "ids": 2211},
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

elif IMPACT_SOURCE_DATABASE == "ecoinvent391":
    electricity_process_list = DataImporter.csv_to_list(
        "src/pod_lca/data/impacts_ecoinvent391_electricity-group.csv", column_header="UUID"
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
    openLCA_client, process_list, impact_categories | emission_inventories, impact_method_uuid, group_by
)

# Note: When using ecoinvent391, renewable fuel group contributions need to be recalculated for all processes that use wood chips as a raw material (instead of fuel).
# wood chips: (uuids: d47a4435-3089-4263-af99-8611eed2698c, 7fe99768-d571-4bc2-a272-7df585bd0d48)
if IMPACT_SOURCE_DATABASE == "ecoinvent391":
    uuid_list_with_wood_chips = DataImporter.csv_to_list(
        "src/pod_lca/data/impacts_ecoinvent391_uuid-list-with-wood-chips.csv", column_header="UUID"
    )
    process_list = openLCA.get_process_list(openLCA_client, uuid_list_with_wood_chips)

    renewable_fuels_process_list = DataImporter.csv_to_list(
        "src/pod_lca/data/impacts_ecoinvent391_renewable-fuels-group-no-wood-chips.csv", column_header="UUID"
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

# save results
save_path = "src/pod_lca/data/impacts_" + IMPACT_SOURCE_DATABASE + "_categorized-data.csv"
DataExporter.dict_to_csv(results, save_path)
