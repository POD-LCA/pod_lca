from utilities.data_imports.csv import CSV_Importer

from pandas import DataFrame, concat
import bisect
import gc


class CambiumData:

    NATIONAL_DATA = "data\\cambium_data_national.csv"
    REGIONAL_DATA = "data\\cambium_data_regional.csv"
    LOCAL_DATA = "data\\cambium_data_local.csv"
    HEADER_MAP = "data\\cambium_headers.json"
    DATA_YEARS = [2025, 2030, 2035, 2040, 2045, 2050]
    TECHNOLOGY_MAP = "data\\cambium_technology_map.json"

    def __init__(self):
        self.data = None

    @classmethod
    def from_regional_resolution(cls, regional_resolution):

        cambium_data = cls()
        
        if regional_resolution== 'National':
            df = CSV_Importer.import_as_pandas(CambiumData.NATIONAL_DATA)
        elif regional_resolution == 'Regional':
            df = CSV_Importer.import_as_pandas(CambiumData.REGIONAL_DATA)
        elif regional_resolution == 'Local':
            df = CSV_Importer.import_as_pandas(CambiumData.LOCAL_DATA)

        cambium_data.data = df

        return cambium_data

    def get_mix(self, year, electricity_technologies, scenario="MidCase"):


        idx = bisect.bisect_left(CambiumData.DATA_YEARS, year)
        if idx == 0:
            years = [CambiumData.DATA_YEARS[0]]
        elif idx == len(CambiumData.DATA_YEARS):
            years = [CambiumData.DATA_YEARS[0][-1]]
        else:
            years = [CambiumData.DATA_YEARS[idx - 1], CambiumData.DATA_YEARS[idx]]

        mix_names = list(CSV_Importer.json_to_dict(CambiumData.HEADER_MAP).values())
        mix_set = DataFrame()
        for yr in years:
            data_set_tmp = self.data[self.data['scenario']==scenario][self.data['t']==yr]
            mix_set = concat([mix_set, data_set_tmp[['t'] + mix_names]], ignore_index=True)

        if len(years) == 2: # interpolate data
            weight = (year - mix_set.iloc[0]['t']) / (mix_set.iloc[1]['t'] - mix_set.iloc[0]['t'])
            new_row = mix_set.iloc[0] + weight * (mix_set.iloc[1] - mix_set.iloc[0])
            new_row['t'] = year
            mix =  new_row
        else:
            mix = mix_set.squeeze()

        # map
        technology_map = CSV_Importer.json_to_dict(CambiumData.TECHNOLOGY_MAP)
        mix_dict = dict.fromkeys(electricity_technologies, 0.0)
        for technology, header in CSV_Importer.json_to_dict(CambiumData.HEADER_MAP).items():
            technology_mapped = technology_map[technology]
            value = mix[header]

            mix_dict[technology_mapped] += value

        total = sum(mix_dict.values())

        return  {k: (v / total) * 100 for k, v in mix_dict.items()}

    def delete_data(self):

        del self.data
        
        gc.collect

if __name__ == '__main__':
    pass