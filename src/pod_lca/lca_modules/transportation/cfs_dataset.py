

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from time import time

from ..location import Location
from ..transportation import TransportMode
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class CFSDataset:
    """ A class to handle the CFS dataset for transportation links.
    """

    def __init__(self):
        self.cfs_dataset = DataImporter.csv_to_pandas(config['file_paths']['transportation']['CFS_DATA_PATH']) 
        self.cfs_modes_mapping = DataImporter.json_to_dict(config['file_paths']['transportation']['CFS_MODE_CODE'])
        self.sctg_codes = DataImporter.csv_to_pandas(config['file_paths']['transportation']['CFS_SCTG_CODE'])

    def get_sctg_code(self, material ,digit=2):
        """ Get the SCTG code based on the material category.

        Parameters
        ----------
        material : str
            The material category for which to retrieve the SCTG code.
        digit: int
            the digit of the SCTG code to retrieve.

        Returns
        -------
        int
            The SCTG code of the material.

        Raises
        ------
        ValueError
            If the material is not found in the dataset.
        """
        data_material = self.sctg_codes
        if material not in data_material["material"].values:
            raise ValueError("material not found in the dataset")
        
        sctg = data_material[data_material["material"] == material].iloc[0, 1]
        sctg = int(str(sctg)[:digit])

        return sctg

    def filter_datasets(self, sctg=None, destination=None, origin=None, mode=None):
        """ Filter the CFS dataset based on the provided parameters.
        
        Parameters
        ----------
        sctg : int, optional
            The Standard Classification of Transported Goods (SCTG) code to filter by.
        destination : Location, optional
            The destination location to filter by.
        origin : Location, optional
            The origin location to filter by.
        mode : TransportMode, optional
            The transportation mode to filter by.
        
        Returns
        -------
        pandas.DataFrame
            The filtered CFS dataset.
        
        Raises
        ------
        ValueError
            If no data is found for the provided SCTG code, destination, or mode.
        """
        cfs = self.cfs_dataset

        # filter SCTG code
        if isinstance(sctg, int):
            cfs_filtered = cfs[cfs["SCTG"] == sctg]
            if cfs_filtered.empty:
                raise ValueError("Material not found in the CFS dataset")
            cfs = cfs_filtered

        # Destination
        if isinstance(destination, Location):
            cfs_filtered = cfs[cfs["DEST_STATE"] == destination.get_cfs_area()]
            if cfs_filtered.empty:
                closest_state_name, closest_state_code = Location.get_closest_state_CFS(destination, cfs["DEST_STATE"].tolist())
                cfs_filtered = cfs[cfs["DEST_STATE"] == closest_state_code]
                log(f"Closest state to {destination.get_location_name()}, {closest_state_name}, is used to estimate travel distance.", "Info")
            cfs = cfs_filtered

        # Origin
        if isinstance(origin, Location):
            cfs_filtered = cfs[cfs["ORIG_STATE"] == origin.get_cfs_area()]
            if cfs_filtered.empty:
                closest_state_name, closest_state_code = Location.get_closest_state_CFS(origin, cfs["ORIG_STATE"].tolist())
                cfs_filtered = cfs[cfs["ORIG_STATE"] == closest_state_code]
                log(f"Closest state to {origin.get_location_name()}, {closest_state_name}, is used to estimate travel distance.", "Info")
            cfs = cfs_filtered

        # Mode
        if isinstance(mode,  TransportMode):
            cfs_modes_mapping = self.cfs_modes_mapping
            cfs_filtered = cfs[cfs["MODE"].isin(cfs_modes_mapping[mode.get_name()])]
            if cfs_filtered.empty:
                raise ValueError("Transportation mode not in CFS dataset")
            cfs = cfs_filtered  
      
        return cfs
    
    @staticmethod
    def get_distance_estimate(dataset, scenario):
        """ Get the average distance from the CFS dataset based on the scenario.
        
        Parameters
        ----------
        dataset : pandas.DataFrame
            The filtered CFS dataset.
        scenario : str
            The scenario to filter the distances by.
        
        Returns
        -------
        float
            The average distance for the specified scenario.
        
        Raises
        ------
        ValueError
            If the scenario is not recognized or if no data is found for the scenario.
        """
        quartiles = dataset["SHIPMT_DIST_ROUTED"].quantile([0.25, 0.5, 0.75]).values
        def assign_quartile(x, q1, q2, q3):
            if x <= q1:
                return 'Q1'
            elif x <= q2:
                return 'Q2'
            elif x <= q3:
                return 'Q3'
            else:
                return 'Q4'
        dataset['quartile'] = dataset["SHIPMT_DIST_ROUTED"].apply(assign_quartile, args=(quartiles[0], quartiles[1], quartiles[2]))
        # TODO: dealing with when the number of entries are less than 4
        if scenario == "Local":
            domestic_dis = dataset[dataset["quartile"] == "Q1"]["SHIPMT_DIST_ROUTED"].mean()
        elif scenario == "Regional":
            domestic_dis = dataset[dataset["quartile"] == "Q2"]["SHIPMT_DIST_ROUTED"].mean()
        elif scenario == "Regional_c":
            domestic_dis = dataset[dataset["quartile"] == "Q3"]["SHIPMT_DIST_ROUTED"].mean()
        elif scenario == "National":
            domestic_dis = dataset[dataset["quartile"] == "Q4"]["SHIPMT_DIST_ROUTED"].mean()
        else: # TODO: Verify this for consistency
            domestic_dis = dataset["SHIPMT_DIST_ROUTED"].mean()

        return domestic_dis


if __name__ == '__main__':
    pass
