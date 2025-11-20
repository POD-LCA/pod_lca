import pandas as pd


date_tag = "17SEPT2025"

file_1 = "save_files\\transportation_dataset_domestic_" + date_tag + ".csv"
file_2 = "save_files\\transportation_dataset_global_" + date_tag + ".csv"
merged_file = "save_files\\transportation_dataset_" + date_tag + ".csv"

df1 = pd.read_csv(file_1)
df2 = pd.read_csv(file_2)

combined = pd.concat([df1, df2], axis=0, ignore_index=True)

first_col = combined.columns[0]  # get first column name
mask = ~combined[first_col].astype(str).str.startswith("Material", na=False)
combined = combined[mask]

combined.to_csv(merged_file, index=False)
