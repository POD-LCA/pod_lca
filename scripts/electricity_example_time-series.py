from lca_modules.material.project_manager import Project 
from lca_modules.location.location import Location
from utilities.settings import config
from utilities.units.common_units import WATT_HOUR, KILO 
from plotters.plots.line_plot import LinePlot
from plotters.plotters.matplotlib_plotter import MatplotlibPlotter

my_manufacturing_project = Project()

my_factory_location = Location.from_str("USA")
my_manufacturing_project.set_location(my_factory_location)

model_one = my_manufacturing_project.add_model("model_01")

electricity = model_one.add_electricity(name="Electricity", stage="A3", qty=1000, unit=KILO * WATT_HOUR)

# electricity impact changes over time
years = [2025, 2030, 2035, 2040, 2045, 2050]
qty = [1000, 1200, 1250, 1000, 750, 500]
IMPACT_CATEGORIES = config['setup']['impacts']['IMPACT_CATEGORIES']
data_dict = {category:{} for category in IMPACT_CATEGORIES}
for scenario in ['MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'Decarb95by2050',]:
    for category in IMPACT_CATEGORIES:
        data_dict[category][scenario] = []

    electricity.set_scenario(scenario) 
    for y, q in zip(years, qty):
        electricity.set_year(y)
        electricity.set_qty(q)

        impacts = electricity.get_impacts()
        for category in IMPACT_CATEGORIES:
            data_dict[category][scenario].append((y, impacts.get_impact(category)))

for category in IMPACT_CATEGORIES:
    graph = LinePlot.from_plotter(MatplotlibPlotter)
    graph.draw(data_dict[category], "Electricity Emissions over years", "Year", f"{category} ({IMPACT_CATEGORIES[category]})")
    graph.show()
