# This script compares the transportation impact values from the manual method (given in as a CSV file) with the values calculated using the Python Framework.

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from pod_lca.units import KILO
from pod_lca.units import KILOMETER
from pod_lca.units import WATT_HOUR
from pod_lca.transportation import USGlobalTransportationManager
from pod_lca.materials_screening import Product
from pod_lca.units import UNITS_MAP
from pod_lca.location import Location
from pod_lca.utilities import DataExporter
from pod_lca.utilities import DataImporter
from pod_lca.utilities import config


def test_transportation_global():
    test_data = "tests\\transportation-global_test_test-values.csv"
    output_file = "tests\\transportation-global_test_report.csv"
    test_dict = DataImporter.csv_to_dict(test_data, "test name")

    project = USGlobalTransportationManager.new("Building A")
    project.set_data_generator_mode()
    project.set_impact_database(r"src/pod_lca/data/transportation_podlca_emission.csv")
    electricity_report_unit = KILO * WATT_HOUR

    output_dict = {}
    impact_categories = config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"]
    emission_inventories = config["setup"]["INVENTORY_ITEMS"]["EMISSION_INVENTORIES"]
    inventories = impact_categories | emission_inventories
    tests_total = 0
    tests_passed = 0
    for test in test_dict:
        product = Product()
        product.set_name(test_dict[test]["product"])
        product.set_qty(float(test_dict[test]["qty"]))
        product.set_unit(UNITS_MAP[test_dict[test]["unit"]])
        product.set_sctg_code(test_dict[test]["sctg_code"])

        origin_faf_zone_obj = (
            None if test_dict[test]["faf_zone"] == "" else Location.from_faf_regions(test_dict[test]["faf_zone"])
        )
        destination_state_obj = (
            None if test_dict[test]["destination"] == "" else Location.from_US_state(test_dict[test]["destination"])
        )
        fr_mode = None if test_dict[test]["fr_mode"] == "" else test_dict[test]["fr_mode"]
        dms_mode = None if test_dict[test]["dms_mode"] == "" else test_dict[test]["dms_mode"]
        efficiency = None if test_dict[test]["efficiency"] == "" else test_dict[test]["efficiency"]

        project.add_good(
            good=product,
            shipping_dest=destination_state_obj,
            shipping_org=origin_faf_zone_obj,
            distance_unit=KILOMETER,
            mode_name=fr_mode,
            mode_efficiency=efficiency,
        )

        if dms_mode is not None:
            transportation_leg = project.get_transportation_leg(product)[0]
            domestic_transport_leg = transportation_leg.get_domestic_leg()
            domestic_transport_leg.set_mode(dms_mode, efficiency=efficiency)

        output_dict[test] = {
            "test name": test,
            "product": test_dict[test]["product"],
            "sctg_code": test_dict[test]["sctg_code"],
            "qty": test_dict[test]["qty"],
            "unit": test_dict[test]["unit"],
            "destination": test_dict[test]["destination"],
            "faf_zone": test_dict[test]["faf_zone"],
            "fr_mode": test_dict[test]["fr_mode"],
            "dms_mode": test_dict[test]["dms_mode"],
            "efficiency": test_dict[test]["efficiency"],
        }

        test_status = True
        foreign_transport_leg = project.get_transportation_leg(product)[0]
        domestic_transport_leg = foreign_transport_leg.get_domestic_leg()
        conversion_factor = KILOMETER.convert_to(UNITS_MAP[test_dict[test]["distance_unit"]])
        try:
            fr_distance = foreign_transport_leg.get_travel_dist() * conversion_factor
            dms_distance = domestic_transport_leg.get_travel_dist() * conversion_factor
        except Exception as e:
            # set results to N/A
            output_dict[test]["fr_distance (Python tool)"] = "N/A"
            output_dict[test]["fr_distance (Manual calc)"] = test_dict[test]["fr_distance"]
            output_dict[test]["dms_distance (Python tool)"] = "N/A"
            output_dict[test]["dms_distance (Manual calc)"] = test_dict[test]["dms_distance"]
            output_dict[test]["distance_unit"] = test_dict[test]["distance_unit"]
            output_dict[test]["fr_distance_difference (%)"] = "N/A"
            output_dict[test]["dms_distance_difference (%)"] = "N/A"
            for inventory in inventories:
                if inventory in test_dict[test]:
                    output_dict[test][inventory + "(" + inventories[inventory] + ")" + " Python tool"] = "N/A"
                    output_dict[test][inventory + "(" + inventories[inventory] + ")" + " Manual calc"] = test_dict[
                        test
                    ][inventory]
                    output_dict[test][inventory + "_difference (%)"] = "N/A"
            output_dict[test]["test status"] = "PASS" if test_dict[test]["fr_distance"] == "Error" else "FAIL"
            # Note error
            output_dict[test]["Notes"] = e
            continue

        # check distance
        test_dist_foreign = 0.0 if test_dict[test]["fr_distance"] == "Error" else float(test_dict[test]["fr_distance"])
        fr_dif = abs(fr_distance - test_dist_foreign) / ((fr_distance + test_dist_foreign) / 2)  # symmetric difference

        test_dist_domestic = (
            0.0 if test_dict[test]["dms_distance"] == "Error" else float(test_dict[test]["dms_distance"])
        )
        if test_dist_domestic > 0.0:
            dms_dif = abs(dms_distance - test_dist_domestic) / (
                (dms_distance + test_dist_domestic) / 2
            )  # symmetric difference
        else:
            dms_dif = 0.0

        output_dict[test]["fr_distance (Python tool)"] = fr_distance
        output_dict[test]["fr_distance (Manual calc)"] = test_dict[test]["fr_distance"]
        output_dict[test]["fr_distance_difference (%)"] = fr_dif * 100
        output_dict[test]["dms_distance (Python tool)"] = dms_distance
        output_dict[test]["dms_distance (Manual calc)"] = test_dict[test]["dms_distance"]
        output_dict[test]["dms_distance_difference (%)"] = dms_dif * 100

        output_dict[test]["distance_unit"] = test_dict[test]["distance_unit"]

        limit = 5.0 if fr_mode == "Air" else 0.5  # air distances can have larger variation
        if fr_dif * 100 > limit or dms_dif * 100 > limit:
            test_status = False
            dif = max(fr_dif, dms_dif)
            print(f"{test} failed on distance with a difference of {dif * 100:.2f}%")
            print(f"computed distance value: {fr_distance}")
            print(f"expected distance value: {test_dict[test]['fr_distance']}")

        # check inventories
        for leg in [foreign_transport_leg, domestic_transport_leg]:
            impacts = leg.get_impacts()
            emissions = leg.get_emissions()
            tag = "_fr" if leg == foreign_transport_leg else "_dms"
            for inventory in inventories:
                if inventory in impact_categories:
                    records = impacts
                elif inventory in emission_inventories:
                    records = emissions
                else:
                    raise KeyError(f"Inventory '{inventory}' not found in IMPACT_CATEGORIES or EMISSION_INVENTORIES.")
                if inventory + tag in test_dict[test]:
                    dif = abs(records.get_record(inventory) - float(test_dict[test][inventory + tag])) / (
                        (records.get_record(inventory) + float(test_dict[test][inventory + tag])) / 2
                    )  # symmetric difference

                    output_dict[test][inventory + tag + "(" + inventories[inventory] + ")" + " Python tool"] = (
                        records.get_record(inventory)
                    )
                    output_dict[test][inventory + tag + "(" + inventories[inventory] + ")" + " Manual calc"] = (
                        test_dict[test][inventory + tag]
                    )
                    output_dict[test][inventory + tag + "_difference (%)"] = dif * 100

                    if dif * 100 > limit:
                        test_status = False
                        print(f"{test} failed on {inventory+ tag} with a difference of {dif * 100:.2f}%")
                        print(f"computed impact value: {records.get_record(inventory)} {inventories[inventory]}")
                        print(f"expected impact value: {test_dict[test][inventory + tag]} {inventories[inventory]}")

        output_dict[test]["test status"] = "PASS" if test_status else "FAIL"
        output_dict[test]["Notes"] = ""

        tests_total += 1
        if test_status:
            tests_passed += 1

    DataExporter.dict_to_csv(output_dict, output_file)

    print(f">>>> Transportation-Foreign tests passed: {tests_passed} of {tests_total}")

    assert tests_passed == tests_total


if __name__ == "__main__":
    pass
