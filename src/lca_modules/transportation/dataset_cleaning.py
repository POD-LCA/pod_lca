import pandas as pd

def cleaning_faf (input_path_faf, output_path_faf):

    faf = pd.read_csv(input_path_faf)

    faf = faf[faf['tons_2017'] != 0]
    faf.dropna(subset=['fr_orig'], inplace=True)

    # Filter rows for import
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

    faf_merged = faf_merged.merge(mot[['dms_mode', 'gwp_mean']].rename(columns={'gwp_mean': 'dom_mot_emi'}), on='dms_mode', how='left')
    faf_merged['min_dom_emi'] = faf_merged['min_dom_dist_km'] * faf_merged['dom_mot_emi']
    faf_merged['max_dom_emi'] = faf_merged['max_dom_dist_km'] * faf_merged['dom_mot_emi']

    # Calculate the average emission and assign to 'ave_dms_emi'
    faf_merged['ave_dom_emi'] = (faf_merged['min_dom_emi'] + faf_merged['max_dom_emi']) / 2

    # Drop rows where 'dms_mot_emi' is NaN, if required
    faf_merged.dropna(subset=['dom_mot_emi'], inplace=True)
    faf_merged = faf_merged[faf_merged['max_dom_emi'].notna()]

    # Drop unrelated columns
    faf_merged.drop(columns=['min_dom_dist', 'max_dom_dist', 'min_dom_dist_km', 'max_dom_dist_km'], inplace=True)

    # Assign faf_merged to faf
    faf = faf_merged
    faf = faf.merge(mot[['fr_inmode', 'gwp_mean']].rename(columns={'gwp_mean': 'fr_mot_emi'}), on='fr_inmode', how='left')
    faf = faf.dropna(subset=['fr_dist'])
    






if __name__ == '__main__':

    input_path_faf = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\temp\transportation_dataset\FAF561.csv"
    output_path_faf = r"C:\Users\mhtaba\Desktop\pod_lca_git\pod_lca\temp\transportation_dataset\FAF561_cleaned.csv"

    cleaning_faf(input_path_faf, output_path_faf)