import pandas as pd
import sys
sys.path.append(r'C:\Users\kiun\ElectricityLCI-development')

from pod_lca.utilities import DataExporter
from pod_lca.utilities import DataImporter
from pod_lca.utilities import log
import electricitylci


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


# Using the ElectricityLCI development branch at commit 2766fa3
# EIA API key (registered to kiun@uw.edu): pFrizy8ltqUZacfG2IR7fCz8KPb1pWpf40C63Vn5

# TODO: add brief of what this do
# olca possibilities not tested

trans_dist_grid_loss = electricitylci.get_distribution_mix_df(subregion='BA')
trading_matrix = electricitylci.get_consumption_mix_df()
generation_mix = electricitylci.get_generation_mix_process_df(regions='BA')

output_file = r'save_files\impacts_uslci_electricity_output'

impact_data_file = r'data\impacts_uslci_electricity.csv'
impact_data_headers = ['GWP (AR5) [kg CO2 eq]','AP [kg SO2 eq]','EP [kg N eq]','ODP [kg CFC-11 eq]','POCP [kg O3 eq]','CO2 [kg]','CH4 [kg]','N2O [kg]']

ferc_regions = ['CAISO', 'ERCOT', 'ISO-NE', 'MISO', 'NW', 'NYISO', 'PJM', 'SE', 'SW', 'SPP']
technologies = ['BIOMASS', 'COAL', 'GAS', 'GEOTHERMAL', 'HYDRO', 'MIXED', 'NUCLEAR', 'OFSL', 'OIL', 'OTHF', 'SOLAR', 'SOLARTHERMAL', 'WIND']

data_all = {}
for ferc_region in ferc_regions:
    data_all[ferc_region] = {}
    for technology in technologies:
        # TODO: consider trade between FERC regions (see if the NETL grid mix explorer considers this)
        tmp_1 = trading_matrix['FERC'][trading_matrix['FERC']['import ferc region abbr']==ferc_region].get(['export_name', 'fraction'])
        tmp_2 = generation_mix[generation_mix['FuelCategory'] == technology].drop(['FuelCategory', 'Electricity'], axis=1, inplace=False)
        tmp_3 = pd.merge(tmp_1, tmp_2, left_on='export_name', right_on='Subregion', how='inner').drop('export_name', axis=1)
        tmp_4 = tmp_3[(tmp_3['fraction']>0.0 ) & (tmp_3['Generation_Ratio']>0.0)]
        tmp_5 = pd.merge(tmp_4, trans_dist_grid_loss, left_on='Subregion', right_on='Balancing Authority Name', how='inner').drop('Subregion', axis=1)

        calc_1 = (tmp_5['fraction'] * tmp_5['Generation_Ratio'])/(sum(tmp_5['fraction'] * tmp_5['Generation_Ratio']))
        calc_2 = calc_1 * (1 + tmp_5['t_d_losses'])
        calc_2.name = 'multiplier'

        tmp_6 = pd.concat([tmp_5['Balancing Authority Name'], calc_2], axis=1)

        electricity_impact = DataImporter.csv_to_pandas(impact_data_file)
        impacts_dict = dict.fromkeys(impact_data_headers, 0)
        for index, row in tmp_6.iterrows():
            USLCI_entry = 'Electricity - ' + technology + ' - ' + row['Balancing Authority Name']
            data_row = electricity_impact[electricity_impact['Name'] == USLCI_entry]
            if data_row.empty:
                log(f"missing BA ({row['Balancing Authority Name']}) for {technology} in {ferc_region}", 1)
                # TODO: investigate this
            else:
                for impact_cat in impact_data_headers:
                    impact_val = electricity_impact[electricity_impact['Name'] == USLCI_entry][impact_cat] * row['multiplier']
                    impacts_dict[impact_cat] +=  impact_val.values[0] * 3600 # TODO: MJ to KWh conversion

        data_all[ferc_region][technology] = impacts_dict

    DataExporter.dict_to_csv(data_all[ferc_region], output_file + f'_{ferc_region}.csv')
    # TODO: write to a single file

# TODO: ERCOT and NYISO need seperate treating
# TODO: Check incompatible names of BAs
# TODO: compare the results ---  how much do they error and why (see trading maps and distribution losses)---trying changing the losses there to reproduce and verify the method4
