# Internal imports
from pod_lca.impacts import Emissions
from pod_lca.dynamic_radiative_forcing import DynamicRadiativeForcingRecord
from pod_lca.impacts import ExponentDecayEmissionProfile
from pod_lca.impacts import UniformEmissionProfile
from pod_lca.impacts import NormEmissionProfile
from pod_lca.impacts import LogNormEmissionProfile
from pod_lca.impacts import LinearEmissionProfile
from pod_lca.impacts import InverseSquareRootEmissionProfile

# External imports
import pandas as pd
from matplotlib import pyplot as plt


# ====== Example C: Creating a DRF record from a CSV file of emissions dictionaries =========

# **********Step 1: Select time horizon settings and output data to plot **********
# Instructions: Select the start year, time horizon, time step, and results to plot. 
start_year = 0 # select start year
time_horizon = 250 # select time horizon (years)
time_step = 1 / 12 # select time step (years)
results_to_plot = ['emission intensity','atmospheric concentration','instantaneous radiative forcing', 'cumulative radiative forcing', 'GWP-dynamic', 'AGTP'] # list one or more of: ['emission intensity', 'atmospheric concentration', 'instantaneous radiative forcing', 'cumulative radiative forcing', 'GWP-dynamic', 'AGTP']
plot_PTandRT_separately = True # if True, plot the product trajectory (PT) and reference trajectory (RT) separately, in addition to the net results. If False, only plot the net results.
plot_annotations = True # if True, annotate the net results at the requested time points. If False, do not annotate the net results.
annotation_years = [20, 100, 250] # list of years at which to annotate the net results. Only used if plot_annotations is True.
show_ghg_stacks = False # if True, show the GHG stacks for the PT and RT separately. If False, do not show the GHG stacks.


# **********Step 2: Create the Product Trajectory (PT) DLCI**********
PT_record = DynamicRadiativeForcingRecord()
PT_record.set_start_year(start_year)
PT_record.set_time_horizon(time_horizon)
PT_record.set_time_step(time_step)

# Set DLCI File path
test_DLCI_file_path = "examples/drf_example_dlci.csv"
PT_record.add_emissions_from_csv(test_DLCI_file_path)

# **********Step 3: Create the Reference Trajectory (RT) DLCI**********
RT_record = DynamicRadiativeForcingRecord()
RT_record.set_start_year(start_year)
RT_record.set_time_horizon(time_horizon)
RT_record.set_time_step(time_step)

# Set DLCI File path
test_DLCI_file_path = "examples/drf_example_dlci.csv"
RT_record.add_emissions_from_csv(test_DLCI_file_path)

# ********** Step 4: Dynamic Radiative Forcing Record evaluation and plot settings: **********
PT_record.set_data() # product and reference trajectories are stored as a POD|LCA DRF_record object
RT_record.set_data()

Net_record = pd.DataFrame() # Net results are stored as a pandas dataframe

# Net results are calculated as the difference between the product and reference trajectories for each data category and GHG:
data_categories = ['emission intensity', 'atmospheric concentration', 'instantaneous radiative forcing', 'cumulative radiative forcing', 'GWP-dynamic', 'AGTP']
ghgs = ['CO2', 'CH4', 'N2O']
for data_category in data_categories:
    PT_data = PT_record.get_data(data_category=data_category, xy_pairs=False)
    RT_data = RT_record.get_data(data_category=data_category, xy_pairs=False)
    Net_data_total = 0
    for ghg in ghgs:
        PT_data_ghg = PT_data[1][ghg]
        RT_data_ghg = RT_data[1][ghg]
        Net_data_ghg = PT_data_ghg - RT_data_ghg
        Net_data_total += Net_data_ghg # Add the net data for each GHG to the total net data
        Net_record[f"{data_category}_{ghg}"] = Net_data_ghg # Add the net data as a column for each GHG
    Net_record[f"{data_category}"] = Net_data_total # Add the total net data as a column
# Net_record['time'] = PT_data[0]
Net_record.insert(0, 'time', PT_data[0])

# Select plot colors
PT_colors = ['#002060', '#00337F', '#4472C4', '#8FAADC', '#D9E2F3',
          '#3F1C59', '#5B2A8F', '#7030A0', '#B4A7D6', '#EAD1DC',
          '#7F0000', '#9C0000', '#C00000', '#E26B6B', '#F4CCCC']

RT_colors = ['#7F1C00', '#9C2B00', '#ED7D31', '#F4B183', '#FCE4D6',
          '#1F4D1F', '#2D6A2D', '#70AD47', '#A9D08E', '#E2EFDA',
          '#7F6000', '#9F7700', '#FFC000', '#FFD966', '#FFF2CC']

Net_colors = ['#7F6000', '#9F7700', '#FFC000', '#FFD966', '#FFF2CC',
          '#7F1C00', '#9C2B00', '#ED7D31', '#F4B183', '#FCE4D6',
          '#1F4D1F', '#2D6A2D', '#70AD47', '#A9D08E', '#E2EFDA']

result_units = {'emission intensity': 'kg/yr',
                'atmospheric concentration': 'kg',
                'instantaneous radiative forcing': 'W/$m^2$',
                'cumulative radiative forcing': '$W \\cdot yr \\cdot m^{-2}$',
                'GWP-dynamic': 'kg CO2e',
                'AGTP': 'K'}

# Plots: customize with matplotlib.pyplot options as desired. (See matplotlib documentation for more information).
for result in results_to_plot:
    result_unit = result_units.get(result, "units")

    Net_plot = Net_record.plot(x='time', y=result, 
                    kind='line', 
                    color=Net_colors[0], 
                    label = f'Net {result}',
                    title=f'CCLIMB {result} analysis', 
                    xlabel='Year', 
                    ylabel=f'Net {result} [{result_unit}]', 
                    xlim=(start_year, start_year + time_horizon),
                    grid=False)


    # Plot PT and RT separately, if requested
    if plot_PTandRT_separately:
        # PT_record.plot(result, "stackplot", group_by="greenhouse_gas", colors = PT_colors)
        # RT_record.plot(result, "stackplot", group_by="greenhouse_gas", colors = RT_colors)

        PT_result = PT_record.get_data(data_category=result, xy_pairs=False)[1]
        RT_result = RT_record.get_data(data_category=result, xy_pairs=False)[1]
        PT_result[f"{result}"] = 0
        RT_result[f"{result}"] = 0

        for ghg in ghgs:
            PT_result_ghg = PT_result[ghg]
            RT_result_ghg = RT_result[ghg]
            PT_result[f"{result}"] += PT_result_ghg
            RT_result[f"{result}"] += RT_result_ghg

        PT_df = pd.DataFrame.from_dict(PT_result)
        RT_df = pd.DataFrame.from_dict(RT_result)

        PT_df.insert(0, 'time', PT_data[0])
        RT_df.insert(0, 'time', RT_data[0])

        Net_plot.plot(PT_df['time'], PT_df[result], 
                                 label=f'Product Trajectory {result}',
                                 color=PT_colors[0],
                                 linestyle='--',
                                 alpha=0.5)
        
        
        Net_plot.plot(RT_df['time'], RT_df[result], 
                                 label=f'Reference Trajectory {result}',
                                 color=RT_colors[0],
                                 linestyle='--',
                                 alpha=0.5)

    # Annotate the net result at the requested time points if requested.
    if plot_annotations:
        annotation_offsets = [(10, 15), (10, 15), (-55, 15)]
        annotations = []
        for annotation_year, annotation_offset in zip(annotation_years, annotation_offsets):
            nearest_index = (Net_record['time'] - annotation_year).abs().idxmin()
            annotation_time = Net_record.at[nearest_index, 'time']
            annotation_value = Net_record.at[nearest_index, result]
            annotation = Net_plot.annotate(
                f'{annotation_year} yrs:\n {annotation_value:.3g}',
                xy=(annotation_time, annotation_value),
                    xytext=annotation_offset,
                    textcoords='offset points',
                    alpha=0.9,
                    color='teal',
                    fontweight='bold',
                    fontsize=8,
                    bbox={'boxstyle': 'round,pad=0.35', 'facecolor': Net_colors[3], 'edgecolor': Net_colors[0], 'alpha': 0.75},
                    arrowprops={'arrowstyle': '->', 'connectionstyle': 'arc3,rad=0.15'},
            )
            annotations.append(annotation)
            Net_plot.plot(annotation_time, annotation_value, 'D', markerfacecolor=Net_colors[3], markeredgecolor=Net_colors[0], markersize=6, alpha=0.9)

    # Show the GHG stacks for the PT and RT, if requested
    if show_ghg_stacks:
        Net_plot.stackplot(PT_df['time'], [PT_df[ghg] for ghg in ghgs], labels=[f'PT {ghg}' for ghg in ghgs], colors=PT_colors, alpha=0.15, hatch='.', edgecolor=PT_colors[0])
        Net_plot.stackplot(RT_df['time'], [RT_df[ghg] for ghg in ghgs], labels=[f'RT {ghg}' for ghg in ghgs], colors=RT_colors, alpha=0.15, hatch='o', edgecolor=RT_colors[0])
  
    
    Net_plot.legend(loc='best', fontsize=10) # show legend
    Net_plot.axhline(0, color='black', linewidth=0.8) # add a horizontal line at y=0
    plt.show()


# Save the DRF records to CSV files:
PT_output_file = "temp/CCLIMB_PT_record_temp.csv"
RT_output_file = "temp/CCLIMB_RT_record_temp.csv"
Net_output_file = "temp/CCLIMB_Net_record_temp.csv"

PT_record.save(PT_output_file)
RT_record.save(RT_output_file)
Net_record.to_csv(Net_output_file, index=False)
