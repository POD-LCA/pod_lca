
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

import bisect
import gc

from pandas import concat
from pandas import DataFrame

from ..location import Location
from ...utilities import config
from ...utilities import DataImporter


class CambiumData:
    """ A class to operate on cambium data.
    
    Attributes
    ----------
    data : DataFrame (Pandas)
        Pandas dataframe of cambium data loaded.
    """

    def __init__(self):
        self.data = None

    @classmethod
    def from_geographical_scope(cls, geographical_scope, location):
        """ Create cambium data object from regionalised data.
        
        Parameters
        ----------
        geographical_scope : str
            Geographical scope of data: e.g., 'National', 'Regional', 'Local'.
        location : Location Obj. or str
            Location of electricity supply.
            If a string is provided, it should be the country code for national level data,
            region name for regional level data, or REEDS balancing authority for local level data.
        """
        cambium_data = cls()
        
        # get country/region name
        if location is None:
            if geographical_scope== 'National':
                country_code = config['setup']['electricity']['DEFAULT_COUNTRY_CODE']
            else:
                raise KeyError(f"No default location for geographical scope {geographical_scope}.")
        elif isinstance(location, str):
            if geographical_scope== 'National':
                country_code = location
            elif geographical_scope == 'Regional':
                region = location
            elif geographical_scope == 'Local':
                region = location
        elif isinstance(location, Location):
            if geographical_scope== 'National':
                country_code = location.get_country_code()
            elif geographical_scope == 'Regional':
                if location.get_cambium_gea_region() is None:
                    location.set_cambium_gea_region()
                region = location.get_cambium_gea_region()
            elif geographical_scope == 'Local':
                if location.get_reeds_balancing_area() is None:
                    location.set_reeds_balancing_area()
                region = location.get_reeds_balancing_area()
        else:
            raise TypeError("Location should be a string or Location object.")
        
        # get cambium data
        if geographical_scope== 'National':
            df = DataImporter.csv_to_pandas(config['file_paths']['electricity']['CAMBIUM_NATIONAL_DATA'])
            cambium_data.data = df[df['country_code'] == country_code]
        elif geographical_scope == 'Regional':
            df = DataImporter.csv_to_pandas(config['file_paths']['electricity']['CAMBIUM_REGIONAL_DATA'])
            cambium_data.data = df[df['gea'] == region]
        elif geographical_scope == 'Local':
            df = DataImporter.csv_to_pandas(config['file_paths']['electricity']['CAMBIUM_LOCAL_DATA'])
            cambium_data.data = df[df['r'] == region]
        else:
            raise KeyError(f"Geographical scope {geographical_scope} not recognized. Should be 'National', 'Regional', or 'Local'")

        return cambium_data

    def get_mix(self, year, technologies, scenario="MidCase", interpolate="values"):
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
        interpolate : str
            Linear interpolation of electricity consumption between two years by 'values' or 'percentages'.

        Returns
        -------
        dict
            Dictionary of electricity generation technology in percentages.
        """
        # match year with years available in dataset.
        cambium_yrs = config['setup']['electricity']['CAMBIUM_DATA_YEARS']
        idx = bisect.bisect_left(cambium_yrs, year)
        if idx == 0:
            years = [cambium_yrs[0]]
        elif idx == len(cambium_yrs):
            years = [cambium_yrs[-1]]
        else:
            years = [cambium_yrs[idx - 1], cambium_yrs[idx]]

        mix_names = list(DataImporter.json_to_dict(config['file_paths']['electricity']['CAMBIUM_HEADER_MAP']).values())
        mix_set = DataFrame()
        for yr in years:
            data_set_tmp = self.data[self.data['scenario']==scenario]
            data_set_tmp = data_set_tmp[data_set_tmp['t']==yr]
            mix_set = concat([mix_set, data_set_tmp[['t'] + mix_names]], ignore_index=True)

        if len(years) == 2: # interpolate data
            weight = (year - mix_set.iloc[0]['t']) / (mix_set.iloc[1]['t'] - mix_set.iloc[0]['t'])

            if interpolate == "percentages":
                percentages_0 = mix_set.iloc[0].div(mix_set.iloc[0].drop('t', axis=0).sum())
                percentages_1 = mix_set.iloc[1].div(mix_set.iloc[1].drop('t', axis=0).sum())
                new_row = percentages_0 + weight * (percentages_1 - percentages_0)
            elif interpolate == "values":
                new_row = mix_set.iloc[0] + weight * (mix_set.iloc[1] - mix_set.iloc[0])
            else:
                raise KeyError(f"Interpolation method {interpolate} not recognized. Should be 'values' or 'percentages'.")
            
            new_row['t'] = year
            mix =  new_row
        else:
            if interpolate == "percentages":
                mix = mix_set.iloc[0].div(mix_set.iloc[0].drop('t', axis=0).sum()).squeeze()
            elif interpolate == "values":
                mix = mix_set.squeeze()
            else:
                raise KeyError(f"Interpolation method {interpolate} not recognized. Should be 'values' or 'percentages'.")

        # map
        technology_map = DataImporter.json_to_dict(config['file_paths']['electricity']['CAMBIUM_TECHNOLOGY_MAP'])
        mix_dict = dict.fromkeys(technologies, 0.0)
        for technology, header in DataImporter.json_to_dict(config['file_paths']['electricity']['CAMBIUM_HEADER_MAP']).items():
            technology_mapped = technology_map[technology]
            value = mix[header]

            mix_dict[technology_mapped] += value

        if interpolate == "percentages":
            return mix_dict
        elif interpolate == "values":
            total = sum(mix_dict.values())
            return  {k: (v / total) for k, v in mix_dict.items()}
        else:
            raise KeyError(f"Interpolation method {interpolate} not recognized. Should be 'values' or 'percentages'.")
    
    def get_load(self, year, scenario="MidCase"):
        """ Get electricity load of the electricity consumption by year.
        
        Parameters
        ----------
        year : int
            Year of electricity consumption.
        scenario : str
            Electricity consmuption scenario considered: e.g., 'MidCase', 'LowRECost', 'HighRECost', 'HighDemandGrowth', 'LowNGPrice', 'HighNGPrice', 'Decarb95by2050', 'Decarb100by2035'.

        Returns
        -------
        float
            Electricity load in GWh.
        """
        # match year with years available in dataset.
        cambium_yrs = config['setup']['electricity']['CAMBIUM_DATA_YEARS']
        idx = bisect.bisect_left(cambium_yrs, year)
        if idx == 0:
            years = [cambium_yrs[0]]
        elif idx == len(cambium_yrs):
            years = [cambium_yrs[-1]]
        else:
            years = [cambium_yrs[idx - 1], cambium_yrs[idx]]

        load = DataFrame()
        for yr in years:
            data_set_tmp = self.data[self.data['scenario']==scenario]
            data_set_tmp = data_set_tmp[data_set_tmp['t']==yr]
            load = concat([load, data_set_tmp[['t'] + ['busbar_load']]], ignore_index=True)

        if len(years) == 2: # interpolate data
            weight = (year - load.iloc[0]['t']) / (load.iloc[1]['t'] - load.iloc[0]['t'])
            new_row = load.iloc[0] + weight * (load.iloc[1] - load.iloc[0])
            new_row['t'] = year
            load =  new_row
        else:
            load = load.squeeze()

        return  load['busbar_load']

    def delete_data(self):
        """ Delete the cambium data object.
        """
        del self.data
        
        gc.collect


if __name__ == '__main__':
    pass
