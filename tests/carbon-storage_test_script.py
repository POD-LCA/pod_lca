# This script compares the GWP impacts adjusted for carbon storage from the Excel tool (given in aa CSV file) with the values calculated using the Python Framework.

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from tqdm import tqdm

from pod_lca.impacts import ImpactsDatabase
from pod_lca.materials_screening import Project
from pod_lca.units import UNITS_MAP
from pod_lca.utilities import DataImporter
from pod_lca.utilities import DataExporter
from pod_lca.utilities import config

test_data = "tests\\carbon-storage_test_test-values.csv"
output_file = "tests\\carbon-storage_test_report.csv"
test_dict = DataImporter.csv_to_dict(test_data, "test name")

project = Project()

# concrete_yard = Location.from_str("Seattle, Washington")
# project.set_location(concrete_yard)

custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(r"data/impacts_podlca_data.csv", additional_headers="Mineral Carbonation Potential")
project.set_impact_database(custom_impact_database)

# project.set_transportation_mode_impact_database(r'data/transportation_podlca_emission.csv')

my_model = project.add_model("Test")
GWP_tag = config["setup"]["impacts"]["CARBONATION_EFFECTS_IMPACT_CATEGORY"]
GWP_unit_tag = "(" + config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"][GWP_tag] + ")"

output_dict = {}
for test in tqdm(test_dict):
    output_dict[test] = {"notes": ""}
    qty = test_dict[test]["Qty"]
    if isinstance(qty, str):
        qty = float(qty.replace(",", ""))

    product = my_model.add_product(
        name=test,
        stage="A1",
        qty=qty,
        unit=UNITS_MAP[test_dict[test]["Unit"]],
        impacts_from=test_dict[test]["Material"],
    )

    if test_dict[test]["set_mineral_carbon"].lower() == "yes":
        try:
            product.set_mineral_carbon_intensity(
                qty=float(test_dict[test]["mineral_C_Qty"]), unit=UNITS_MAP[test_dict[test]["mineral_C_Unit"]]
            )
        except Warning as w:
            output_dict[test]["notes"] = w

    output_dict[test]["test name"] = test
    output_dict[test]["Qty"] = qty
    output_dict[test]["Unit"] = test_dict[test]["Unit"]
    output_dict[test]["set_mineral_carbon"] = test_dict[test]["set_mineral_carbon"]
    output_dict[test]["mineral_C_Qty"] = test_dict[test]["mineral_C_Qty"]
    output_dict[test]["mineral_C_Unit"] = test_dict[test]["mineral_C_Unit"]

    GWP_Python = product.get_impacts().get_record("GWP")
    GWP_Excel_tool = float(test_dict[test]["GWP"])
    dif_GWP = 2 * abs(GWP_Python - GWP_Excel_tool) / abs(GWP_Python + GWP_Excel_tool)

    output_dict[test]["GWP_Python tool_" + GWP_unit_tag] = GWP_Python
    output_dict[test]["GWP_Excel tool_" + GWP_unit_tag] = GWP_Excel_tool
    output_dict[test]["GWP_difference (%)"] = dif_GWP * 100

    GWP_adjusted_Python = product.get_impacts().get_adjusted_GWP()
    GWP_adjusted_Excel_tool = float(test_dict[test]["GWP_adjusted"])
    dif_adjusted_GWP = (
        2 * abs(GWP_adjusted_Python - GWP_adjusted_Excel_tool) / abs(GWP_adjusted_Python + GWP_adjusted_Excel_tool)
    )

    output_dict[test]["GWP_adjusted_Python tool_" + GWP_unit_tag] = GWP_adjusted_Python
    output_dict[test]["GWP_adjusted_Excel tool_" + GWP_unit_tag] = GWP_adjusted_Excel_tool
    output_dict[test]["GWP_adjusted_difference (%)"] = dif_adjusted_GWP * 100

    if (dif_GWP * 100 < 0.5) and (dif_adjusted_GWP * 100 < 0.5):
        test_status = True
    else:
        test_status = False
        print(f"{test} failed")

    output_dict[test]["test status"] = "PASS" if test_status else "FAIL"

DataExporter.dict_to_csv(output_dict, output_file)
