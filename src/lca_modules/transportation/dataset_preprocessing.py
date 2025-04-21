import pandas as pd

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"


def faf_preprocessing (input_path_faf, output_path_faf):

    """
    This function cleans the FAF dataset by removing unrelated columns, filtering the data, and converting distance units.
    It also merges the cleaned data with the FAF distance band data and calculates average distances.
    """


    PODlLCA_file_path = r"data\transportation_dataset\transportation_pod_lca.xlsx"

    dist_fr = pd.read_excel(PODlLCA_file_path, sheet_name="dist_fr")
    mot = pd.read_excel(PODlLCA_file_path, sheet_name="MOT")
    sensitive_material = pd.read_excel(PODlLCA_file_path, sheet_name="sensitive_material")
    faf_dist_band = pd.read_excel(PODlLCA_file_path, sheet_name="faf_dist_band")

    dist_fr['fr_inmode'] = pd.to_numeric(dist_fr['fr_inmode'], errors='coerce')
    dist_fr['fr_orig'] = pd.to_numeric(dist_fr['fr_orig'], errors='coerce')

    dist_fr['fr_inmode'] = dist_fr['fr_inmode'].astype(float)
    dist_fr['fr_orig'] = dist_fr['fr_orig'].astype(float)

    faf = pd.read_csv(input_path_faf)
    faf = faf[faf['tons_2017'] != 0]
    faf.dropna(subset=['fr_orig'], inplace=True)

    faf_filtered = faf[faf['trade_type'] == 2]

    #Remove unrelated columns
    columns_to_remove = [
        "fr_dest", "fr_outmode", "tons_2018", "tons_2019", "tons_2020", "tons_2021", "tons_2022", 
        "tons_2023", "tons_2025", "tons_2030", "tons_2035", "tons_2040", "tons_2045", "tons_2050",
        "value_2017", "value_2018", "value_2019", "value_2020", "value_2021", "value_2022", 
        "value_2023", "value_2025", "value_2030", "value_2035", "value_2040", "value_2045", "value_2050",
        "current_value_2018", "current_value_2019", "current_value_2020", "current_value_2021", 
        "current_value_2022", "current_value_2023", "tmiles_2017", "tmiles_2018", "tmiles_2019", 
        "tmiles_2020", "tmiles_2021", "tmiles_2022", "tmiles_2023", "tmiles_2025", "tmiles_2030", 
        "tmiles_2035", "tmiles_2040", "tmiles_2045", "tmiles_2050"
    ]

    faf_cleaned = faf.drop(columns=columns_to_remove)
    faf_merged = faf_cleaned.merge(faf_dist_band, on='dist_band', how='left')

    # Convert 'min_dms_dist' and 'max_dms_dist' from miles to kilometers
    faf_merged['min_dom_dist_km'] = faf_merged['min_dom_dist'] * 1.60934
    faf_merged['max_dom_dist_km'] = faf_merged['max_dom_dist'] * 1.60934

    faf_merged['avr_dom_dist_km'] = (faf_merged['min_dom_dist_km'] + faf_merged['max_dom_dist_km']) / 2
    faf_merged.drop(columns=['min_dom_dist', 'max_dom_dist', 'min_dom_dist_km','max_dom_dist_km' ], inplace=True)
    faf = faf_merged.to_csv(output_path_faf, index=False)

    return faf

def cfaf_preprocessing (input_path_cfaf , output_path_cfaf):

    """
    This function cleans the CFaf dataset by filtering the data for specific conditions, dropping unrelated columns,
    and creating a mapping for SCTG groups to their corresponding numbers. It also calculates the average distance per shipment.
    """

    cfaf = pd.read_excel(input_path_cfaf)

    cfaf_filtered = cfaf[(cfaf['Year'] == 2017) & 
                         (cfaf['DestCtry'].isin(['UM'])) & 
                         (cfaf['OrigCtry'] == 'CA')]

    # Drop the specified columns
    columns_to_drop = ['Weight', 'Revenue', 'TonneKm', 'Value', 'DestProv', 'DestCMA', 'OrigCMA', 'OrigProv']
    cfaf_filtered = cfaf_filtered.drop(columns=columns_to_drop)

    # Create a mapping dictionary from SCTGGroup to their corresponding numbers
    sctg_mapping = {
        'AGRI': [1, 2, 3, 4],
        'FOOD': [5, 6, 7, 8, 9],
        'MNRLS': [10, 11, 12, 13, 14],
        'COAL': [15],
        'FUELS': [16, 17, 18, 19],
        'PLCHM': [20, 21, 22, 23, 24],
        'FRPAP': [25, 26, 27, 28, 29],
        'BMETL': [31, 32, 33],
        'TRANS': [36, 37],
        'OTHMF': [30, 34, 35, 38, 39, 40],
        'WASTE': [41],
        'MISC': [42]
    }

    # Create a list to store the new rows
    new_rows = []

    # Iterate over each row in the cfaf dataframe
    for _, row in cfaf_filtered.iterrows():
        sctg_group = row['SCTGGroup']
        
        # Check if the SCTGGroup exists in the mapping
        if sctg_group in sctg_mapping:
            # For each number in the corresponding list, create a new row
            for sctg_num in sctg_mapping[sctg_group]:
                new_row = row.copy()  # Copy the original row
                new_row['SCTG_2digits'] = sctg_num  # Replace with one SCTG number
                new_rows.append(new_row)  # Append the new row to the list
        else:
            # If no mapping exists, just keep the original row
            new_row = row.copy()
            new_row['SCTG_2digits'] = sctg_group  # Keep the original SCTG group
            new_rows.append(new_row)

    # Create a new dataframe from the list of new rows
    cfaf = pd.DataFrame(new_rows)
    cfaf['Distance_per_Shipment'] = cfaf['Distance'] / cfaf['Shipments']
    cfaf = cfaf.dropna(subset=['Distance_per_Shipment'])
    
    # Group by 'SCTG_2digits' and calculate the average 'Distance_per_Shipment'
    cfaf2017 = cfaf.groupby('SCTG_2digits', as_index=False)['Distance_per_Shipment'].mean()

    # Rename the resulting column for clarity
    cfaf2017.rename(columns={'Distance_per_Shipment': 'Average_Distance_per_Shipment'}, inplace=True)

    cfaf2017.to_csv(output_path_cfaf, index=False)

    return cfaf2017

def cfs_preprocessing (input_path, output_path):

    """
    This function cleans the CFS dataset by filtering the data for specific conditions, dropping unrelated columns,
    and renaming the columns for clarity. It also filters the data based on specific modes of transportation.
    """

    cfs = pd.read_csv (input_path)
    cfs = cfs.drop(columns=["SHIPMT_ID", "QUARTER", "SHIPMT_VALUE", "TEMP_CNTL_YN", "EXPORT_CNTRY",
                            "HAZMAT", "WGT_FACTOR", "ORIG_MA", "ORIG_CFS_AREA", "DEST_MA", "DEST_CFS_AREA"])
    
    cfs = cfs[cfs["EXPORT_YN"] == "N"]
    cfs = cfs[cfs["MODE"].isin([3, 4, 5, 6, 7, 8, 9, 10, 101, 11])]

    cfs.to_csv(output_path, index=False)
    return cfs



if __name__ == "__main__":

    """"
    Original data sources:

    FAF (Freight Analysis Framework) dataset: https://ops.fhwa.dot.gov/freight/freight_analysis/faf/
    CFaf (Canadian Freight Analysis Framework) dataset: https://www150.statcan.gc.ca/n1/pub/50-503-x/50-503-x2018001-eng.htm
    CFS (Commodity Flow Survey) dataset: https://www.census.gov/programs-surveys/cfs.html

    """

    faf_preprocessing (input_path_faf, output_path_faf)
    cfaf_preprocessing (input_path_cfaf, output_path_cfaf)
    cfs_preprocessing (input_path_cfs, output_path_cfs)