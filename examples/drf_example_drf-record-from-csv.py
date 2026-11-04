__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "Modified BSD License"
__email__ = "etel5501@uw.edu"
__version__ = "0.1.0"

from pathlib import Path
import matplotlib.pyplot as plt

from pod_lca.impacts import Emissions
from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcingRecord
from pod_lca.impacts import ExponentDecayEmissionProfile
from pod_lca.impacts import UniformEmissionProfile
from pod_lca.impacts import NormEmissionProfile
from pod_lca.impacts import LogNormEmissionProfile
from pod_lca.impacts import LinearEmissionProfile
from pod_lca.impacts import InverseSquareRootEmissionProfile
from pod_lca.materials_screening import Master
from pod_lca.materials_screening import Model
from pod_lca.materials_screening import Project

project = Project.new()
model = Model.in_project(project)
lca_stages = ("A1-A3", "A4","A5","B1","B4","B6","C1","C2","C3","C4","D")
for stage_records in (model.impacts, model.emissions, model.carbon_storage):
    for stage in lca_stages:
        stage_records.setdefault(stage, [])

# Change plot settings below the example DLCI, then click run to generate the plot and results file. 

# Creating a DRF record from a CSV file of emissions dictionaries
test_DLCI_file_path = "examples/drf_example_dlci.csv"
drf_record = DynamicRadiativeForcingRecord.from_csv(test_DLCI_file_path, 
                                                   start_year=0, 
                                                   time_horizon=100, 
                                                   time_step=1/12)

emissions_list = drf_record.get_emissions_list()
for emission in emissions_list:
    emission_profile = emission.get_temporal_emission_profile()
    name = emission_profile.get_name()
    lca_stage = emission_profile.get_attr()
    parent = Master.new(None, name, model, lca_stage, 1, None, None)
    emission.set_parent(parent)


# Dynamic Radiative Forcing Record evaluation and plot settings:
drf_record.set_data()

# Generate one color per plotted product using a colormap.
grouped_data = drf_record.get_grouped_data("emission intensity", "product")
colormap = plt.get_cmap("viridis", max(len(grouped_data), 1))
colors = [colormap(i) for i in range(len(grouped_data))]


drf_record.plot(
    "AGTP", # plot options: 'emission intensity', 'atmospheric concentration', 'instantaneous radiative forcing', 'cumulative radiative forcing', 'GWP-dynamic', 'AGTP'
    "stackplot", # plot types: 'lineplot', 'stackplot'
    group_by="product", # group_by options: "greenhouse_gas", "product", "lca_stage"
    colors = colors
)

# Save the DRF record to a CSV file:
output_file = "temp/drf_record_temp.csv"
file_path = Path(output_file)
file_path.parent.mkdir(parents=True, exist_ok=True)
drf_record.save(output_file)
