__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.materials_screening import Project
from pod_lca.location import Location
from pod_lca.units import KILO
from pod_lca.units import WATT_HOUR
from pod_lca.utilities import config
from pod_lca.visualizer import LinePlot
from pod_lca.visualizer import MatplotlibPlotter

my_manufacturing_project = Project()

my_factory_location = Location.from_str("USA")
my_manufacturing_project.set_location(my_factory_location)

model_one = my_manufacturing_project.add_model("model_01")

electricity = model_one.add_electricity(name="Electricity", stage="A3", qty=1000, unit=KILO * WATT_HOUR)

# electricity impact changes over time
years = [2025, 2030, 2035, 2040, 2045, 2050]
qty = [1000, 1200, 1250, 1000, 750, 500]
impact_categories = config["setup"]["INVENTORY_ITEMS"]["IMPACT_CATEGORIES"]
data_dict = {category: {} for category in impact_categories}
for scenario in [
    "MidCase",
    "LowRECost",
    "HighRECost",
    "HighDemandGrowth",
    "Decarb95by2050",
]:
    for category in impact_categories:
        data_dict[category][scenario] = []

    electricity.set_scenario(scenario)
    for y, q in zip(years, qty):
        electricity.set_year(y)
        electricity.set_qty(q)

        impacts = electricity.get_impacts()
        for category in impact_categories:
            data_dict[category][scenario].append((y, impacts.get_record(category)))

for category in impact_categories:
    graph = LinePlot.from_plotter(MatplotlibPlotter)
    graph.draw(
        data_dict[category], "Electricity Emissions over years", "Year", f"{category} ({impact_categories[category]})"
    )
    graph.show()
