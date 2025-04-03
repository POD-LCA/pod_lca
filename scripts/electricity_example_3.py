from lca_modules.material.project_manager import Project 
from lca_modules.location.location import Location
from utilities.units.common_units import WATT_HOUR, KILO 
from plotters.plots.line_plot import LinePlot
from plotters.plotters.matplotlib_plotter import MatplotlibPlotter

my_manufacturing_project = Project()

my_factory_location = Location.from_str("USA")
# my_factory_location = Location.from_str("Washington State, USA")
my_manufacturing_project.set_location(my_factory_location)

model_one = my_manufacturing_project.add_model("model_01")

# user adding electricity to the model
electricity = model_one.add_electricity(name="Electricity", stage="A3", qty=1000, unit=KILO * WATT_HOUR)

