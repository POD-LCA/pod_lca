from utilities.data_imports.csv import CSV_Importer

from pandas import DataFrame, concat
import bisect
import gc

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class CambiumData:
    """ A class to operate on cambium data.
    
        Attributes
        ----------
        NATIONAL_DATA : str
            File path to national level cambium data.
        REGIONAL_DATA : str
            File path to regional level cambium data.
        LOCAL_DATA : str
            File path to local level cambium data.
        DATA_YEARS : list
            List of years for which cambium data is available.
        HEADER_MAP : str
            File path to mapping of cambium data headers with electricity generation technology.
        TECHNOLOGY_MAP : str
            File path to mapping of cambium technology names with that of impact data source.
        data : DataFrame (Pandas)
            Pandas dataframe of cambium data loaded.
    """

    NATIONAL_DATA = "data\\cambium_data_national.csv"
    REGIONAL_DATA = "data\\cambium_data_regional.csv"
    LOCAL_DATA = "data\\cambium_data_local.csv"
    DATA_YEARS = [2025, 2030, 2035, 2040, 2045, 2050]
    HEADER_MAP = "data\\cambium_headers.json"
    TECHNOLOGY_MAP = "data\\cambium_technology_map.json"

    def __init__(self):
        self.data = None

    @classmethod
    def from_regional_resolution(cls, regional_resolution, location):
        """ Create cambium data object from regionalised data.
        
            Parameters
            ----------
            regional_resolution : str
                Level of regionality of data: e.g., 'National', 'Regional', 'Local'.
            location : Location Obj.
                Location of electricity supply.
        """

        cambium_data = cls()
        
        if location is None:
            raise ValueError('No region name set.')
        else:
            if regional_resolution== 'National':
                country_code = location.get_country_code()
                df = CSV_Importer.import_as_pandas(CambiumData.NATIONAL_DATA)
                cambium_data.data = df[df['country code'] == country_code]
            elif regional_resolution == 'Regional':
                if location.get_cambium_gea_region() is None:
                    location.set_cambium_gea_region()
                region = location.get_cambium_gea_region()
                df = CSV_Importer.import_as_pandas(CambiumData.REGIONAL_DATA)
                cambium_data.data = df[df['gea'] == region]
            elif regional_resolution == 'Local':
                if location.get_reeds_balancing_authority() is None:
                    location.set_reeds_balancing_authority()
                region = location.get_reeds_balancing_authority()
                df = CSV_Importer.import_as_pandas(CambiumData.LOCAL_DATA)
                cambium_data.data = df[df['r'] == region]
            else:
                raise KeyError("Regional resolution not recognized. Should be 'National', 'Regional', or 'Local'")

            return cambium_data

    def get_mix(self, year, technologies, scenario="MidCase"):
        """ Get technology mix of the electricity consumption by year.

            Notes
            -----
            Cambium data are available for 5 year increments from 2025 to 2050. The data are linearly interpolated for the years in between.
         
            Parameters
            ----------
            year : int
                Year of electricity consumption.
            technologies : list
                List of electricity generation technoclogies to be classified by.
            scenario : str
                Electricity consmuption scenario considered: e.g., 'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'.

            Returns
            -------
            dict
                Dictionary of electricity generation technology in percentages.
        """

        # match year with years available in dataset.
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
            data_set_tmp = self.data[self.data['scenario']==scenario]
            data_set_tmp = data_set_tmp[data_set_tmp['t']==yr]
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
        mix_dict = dict.fromkeys(technologies, 0.0)
        for technology, header in CSV_Importer.json_to_dict(CambiumData.HEADER_MAP).items():
            technology_mapped = technology_map[technology]
            value = mix[header]

            mix_dict[technology_mapped] += value

        total = sum(mix_dict.values())

        return  {k: (v / total) for k, v in mix_dict.items()}

    def delete_data(self):
        """ Delete the cambium data object"""

        del self.data
        
        gc.collect


if __name__ == '__main__':
    pass