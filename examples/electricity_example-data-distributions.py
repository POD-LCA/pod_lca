
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from numpy import percentile, linspace

from pod_lca.materials_screening import Project 
from pod_lca.location import Location
from pod_lca.units import KILO
from pod_lca.units import WATT_HOUR
from pod_lca.utilities import config
from pod_lca.visualizer import BoxPlot
from pod_lca.visualizer import Histogram
from pod_lca.visualizer import MatplotlibPlotter
from pod_lca.visualizer import ViolinPlot

my_manufacturing_project = Project()

# =================================
# Set project location
# ================================= 
my_factory_location = Location.from_str("USA") # 'National' location
# my_factory_location = Location.from_str("oklahoma") # 'Regional' location
# my_factory_location = Location.from_str("98102, USA") # 'Local' location

my_manufacturing_project.set_location(my_factory_location)

model_one = my_manufacturing_project.add_model("model_01")

electricity = model_one.add_electricity(name="Electricity", stage="A3", qty=1000, unit=KILO * WATT_HOUR)

print(electricity.get_impacts())

# =================================
# Impact distribution
# =================================
# distribution of unit impacts, from the electricity supplier
electricity_supplier = electricity.get_supplier()
impact_distribution = electricity_supplier.get_impact_distribution()

# distribution of impacts of the electricity product
distribution_list = electricity.get_data_distribution('impacts')

impact_categories = config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES']
plot_type = 'boxplot' # 'boxplot' or 'violinplot'
for distribution in distribution_list:
    # Parametric Statistics
    # This is preferred when the nature of the data is known (e.g., we know the electricity consumption varies normally).
    print(f"Distribution: {distribution.get_name()}")
    # print(distribution.get_dist_name())
    # print(f"Q0: {distribution.percentile(0)}")
    # print(f"Q1: {distribution.percentile(.25)}")
    # print(f"Q2: {distribution.percentile(.50)}")
    # print(f"Q3: {distribution.percentile(.75)}")
    # print(f"Q4: {distribution.percentile(1.00)}")
    graph = Histogram.from_plotter(MatplotlibPlotter)
    graph.draw(distribution.get_data(), no_bins=5, title=distribution.get_name(), x_label=impact_categories[distribution.get_name()], y_label='probability density', unitize=True)

    # x = linspace(distribution.percentile(0), distribution.percentile(.95), 100)
    # p = distribution.get_distribution().pdf(x)
    # graph.draw_pdf(x, p, label="fitted distribution")
    graph.show()

    # Non-parametric Statistics
    # This is prefeered when the nature of the data is unknown.
    print(percentile(distribution.get_data(), 0))
    print(percentile(distribution.get_data(), 25))
    print(percentile(distribution.get_data(), 50))
    print(percentile(distribution.get_data(), 75))
    print(percentile(distribution.get_data(), 100))

    if plot_type == 'boxplot':
        graph = BoxPlot.from_plotter(MatplotlibPlotter)
        graph.draw(distribution.get_data(), title=distribution.get_name(), x_label='', y_label=impact_categories[distribution.get_name()])
        graph.show()
    elif plot_type == 'violinplot':
        graph = ViolinPlot.from_plotter(MatplotlibPlotter)
        graph.draw(distribution.get_data(), title=distribution.get_name(), x_label='', y_label=impact_categories[distribution.get_name()])
        graph.show()
    else:
        raise ValueError("Invalid plot type. Choose 'boxplot' or 'violinplot'.")
