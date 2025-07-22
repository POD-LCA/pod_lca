

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

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

    def filter_datasets(self, material=None, destination=None, origin=None, mode=None):
        """ Filter the CFS dataset based on the provided parameters.
        
        Parameters
        ----------
        material : ~pod_lca.materials_screening.Master
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
        sctg_code = material.get_sctg_code(digits=2)

        # filter SCTG code
        if isinstance(sctg_code, int):
            cfs_filtered = cfs[cfs["SCTG"] == sctg_code]
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
        
        if len(dataset) < 4:
            domestic_dis = dataset["SHIPMT_DIST_ROUTED"].mean()
        else:
            if scenario == "Local":
                domestic_dis = dataset[dataset["quartile"] == "Q1"]["SHIPMT_DIST_ROUTED"].mean()
            elif scenario == "Regional":
                domestic_dis = dataset[dataset["quartile"] == "Q2"]["SHIPMT_DIST_ROUTED"].mean()
            elif scenario == "Regional_c":
                domestic_dis = dataset[dataset["quartile"] == "Q3"]["SHIPMT_DIST_ROUTED"].mean()
            elif scenario == "National":
                domestic_dis = dataset[dataset["quartile"] == "Q4"]["SHIPMT_DIST_ROUTED"].mean()
            elif scenario == "Average":
                domestic_dis = dataset["SHIPMT_DIST_ROUTED"].mean()
            else:
                raise ValueError(f"{scenario} scenario is not recognized")

        return domestic_dis


if __name__ == '__main__':
    pass
