# CLT model from M2.2 Go/No-Go: Material LCA Framework Prototype (https://drive.google.com/file/d/1bh152x9gXN1INkqn-unv-IDL5lAz41lw/view?usp=drive_link)

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.location import Location
from pod_lca.materials_screening import Project
from pod_lca.impacts import ImpactsDatabase
from pod_lca.uncertainty import HotSpotAnalysis
from pod_lca.uncertainty import DataQualityAnalysis
from pod_lca.uncertainty import SensitivityAnalysis

from pod_lca.units import KILOGRAM, KILOMETER, WATT_HOUR, CUBIC_METER
from pod_lca.units import KILO

project = Project()

factory = Location.from_str("98126, seattle")
project.set_location(factory)

custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(
    r"src/pod_lca/data/impacts_podlca_material-data.csv",
    impact_headers_map={"GWP": "GWP", "AP": "AP", "EP": "EP", "ODP": "ODP", "SFP": "POCP"},
)
custom_impact_database.set_data_entry(
    "Electricity_New",
    1.0,
    KILO * WATT_HOUR,
    impacts={"GWP": 0.503, "AP": 0.0036, "EP": 5.83e-05, "ODP": 7.6e-11, "POCP": 3.37e-2},
)
project.set_impact_database(custom_impact_database)

CLT_model = project.add_model("CLT_01")

lumber = CLT_model.add_product(name="Lumber", stage="A1", qty=562.75, unit=KILOGRAM, impacts_from="Lumber_[CORRIM_LCA]")
meth_diphenyl_d = CLT_model.add_product(
    name="Methylene diphenyl diisocyanate resin",
    stage="A1",
    qty=3.22,
    unit=KILOGRAM,
    impacts_from="Methylene diphenyl diisocyanate resin_[FHWA_MTU]",
    sctg_code=26,
)
prop_glycol = CLT_model.add_product(
    name="Propylene glycol", stage="A1", qty=2.77, unit=KILOGRAM, impacts_from="Propylene glycol_[ecoinvent]"
)
dummy_PUR_1 = CLT_model.add_product(name="PUR_1", stage="A1", qty=0.05, unit=KILOGRAM, impacts_from=None,sctg_code=28)
dummy_PUR_2 = CLT_model.add_product(name="PUR_2", stage="A1", qty=0.01, unit=KILOGRAM, impacts_from=None,sctg_code=28)
dummy_PUR_3 = CLT_model.add_product(name="PUR_3", stage="A1", qty=0.01, unit=KILOGRAM, impacts_from=None,sctg_code=28)
electricity = CLT_model.add_electricity(name="Electricity", stage="A3", qty=128.75, unit=KILO * WATT_HOUR)
natural_gas = CLT_model.add_energy(
    name="Natural gas", stage="A3", qty=2.63, unit=CUBIC_METER, impacts_from="Natural gas_insustrial_equipment_[USLCI]"
)

# Hotspot analysis
hotspot_analysis = HotSpotAnalysis.from_model(CLT_model)
hot_spots_GWP = hotspot_analysis.run(impact_category="GWP")
print(hotspot_analysis)

# Data Quality Assessment
data_quality_assessment = DataQualityAnalysis.from_model(CLT_model)
print(electricity.get_pedigree_score())
electricity.get_pedigree_score().update_pedigree_scores(
    {
        "reliability": 1,
        "completeness": 1,
        "temporal correlation": 4,
        "geographical correlation": 1,
        "technological representativeness": 3,
    }
)
lumber.get_pedigree_score().update_pedigree_scores(
    {
        "reliability": 1,
        "completeness": 2,
        "temporal correlation": 2,
        "geographical correlation": 2,
        "technological representativeness": 4,
    }
)
DQS, nDQS = data_quality_assessment.calculate_model_DQS("GWP")
data_quality_assessment.print_results()

# # Sensitivity Analysis
result_range = SensitivityAnalysis.compute_sensitivity_of_param(
    electricity,
    "impact_database_entry",
    impact_cat="GWP",
    options=["Electricity_NWPP(eGrid)_[USLCI]", "Electricity_UnknownHigh_[USLCI]", "Electricity_UnknownLow_[USLCI]"],
)
result_range = SensitivityAnalysis.compute_sensitivity_of_param(lumber, "qty", impact_cat="GWP", range=(506.48, 619.03))
result_range = SensitivityAnalysis.compute_sensitivity_of_params(
    CLT_model,
    [
        {"obj": lumber_by_truck, "param": "transported_distance", "range": (226.57, 453.13)},
        {"obj": PUR1_by_truck, "param": "transported_distance", "range": (1620, 3240)},
        {"obj": PUR2_by_truck, "param": "transported_distance", "range": (48600, 97200)},
    ],
    impact_cat="GWP",
)
# FIXME: Example to be fixed to extract transportation impacts