from pod_lca.impacts import Emissions
from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcingRecord
from pod_lca.impacts import ExponentDecayEmissionProfile
from pod_lca.impacts import UniformEmissionProfile
from pod_lca.impacts import NormEmissionProfile
from pod_lca.impacts import LogNormEmissionProfile
from pod_lca.impacts import LinearEmissionProfile
from pod_lca.impacts import InverseSquareRootEmissionProfile

# Change plot settings below the example DLCI, then click run to generate the plot and results file. 

# Creating a DRF record from a CSV file of emissions dictionaries
drf_record = DynamicRadiativeForcingRecord()
drf_record.set_start_year(0)
drf_record.set_time_horizon(100)
drf_record.set_time_step(1 / 12)

# Set DLCI File path
test_DLCI_file_path = "examples/drf_example_dlci.csv"
drf_record.add_emissions_from_csv(test_DLCI_file_path)

# Dynamic Radiative Forcing Record evaluation and plot settings:
drf_record.set_data()

# Select plot color scheme
colors = ['#002060', '#00337F', '#4472C4', '#8FAADC', '#D9E2F3',
          '#3F1C59', '#5B2A8F', '#7030A0', '#B4A7D6', '#EAD1DC',
          '#7F0000', '#9C0000', '#C00000', '#E26B6B', '#F4CCCC',
          '#7F1C00', '#9C2B00', '#ED7D31', '#F4B183', '#FCE4D6',
          '#7F6000', '#9F7700', '#FFC000', '#FFD966', '#FFF2CC',
          '#1F4D1F', '#2D6A2D', '#70AD47', '#A9D08E', '#E2EFDA'
          ]

drf_record.plot(
    "AGTP", # plot options: 'emission intensity', 'atmospheric concentration', 'instantaneous radiative forcing', 'cumulative radiative forcing', 'GWP-dynamic', 'AGTP'
    "stackplot", # plot types: 'lineplot', 'stackplot'
    group_by="greenhouse_gas", # group_by options: "greenhouse_gas", "material", "lca_stage"
    colors = colors
)

# Save the DRF record to a CSV file:
output_file = "temp/drf_record_temp.csv"
drf_record.save(output_file)
