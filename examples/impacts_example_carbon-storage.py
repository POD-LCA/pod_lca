
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.impacts import ImpactsDatabase
from pod_lca.materials_screening import Project
from pod_lca.units import KG_CARBON_DIOXIDE
from pod_lca.units import KILOGRAM

project = Project()

custom_impact_database = ImpactsDatabase.new("My database")
custom_impact_database.set_data(r'data/impacts_podlca_data.csv', additional_headers='Mineral Carbonation Potential')
project.set_impact_database(custom_impact_database)

my_model = project.add_model("CLT_01")

# Biogenic C
hardwood_bark = my_model.add_product(name="hardwood bark", stage="A1", qty=2, unit=KILOGRAM, impacts_from='Bark, hardwood, average, at forest road,  NE-NC')
print(hardwood_bark.get_impacts())
print("adjusted GWP:", hardwood_bark.get_impacts().get_adjusted_GWP())

# Mineral C
aggregate = my_model.add_product(name="aggregate", stage="A1", qty=1, unit=KILOGRAM, impacts_from='Aggregate; Vulcan Materials; 3/4" x #4 Gravel')
aggregate.set_mineral_carbon_intensity(qty=0.5, unit=KG_CARBON_DIOXIDE)
print(aggregate.get_impacts())
print("adjusted GWP:", aggregate.get_impacts().get_adjusted_GWP())
