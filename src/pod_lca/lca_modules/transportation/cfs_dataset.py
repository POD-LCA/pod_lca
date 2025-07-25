

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from . import TransportDataset
from ..location import Location
from ..transportation import TransportMode
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class CFSDataset(TransportDataset):
    """ A class to handle the CFS dataset for transportation legs.
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
        destination : ~pod_lca.location.Location, optional
            The destination location to filter by.
        origin : ~pod_lca.location.Location, optional
            The origin location to filter by.
        mode : ~pod_lca.transportation.TransportMode, optional
            The transportation mode to filter by.
        
        Returns
        -------
        pandas.DataFrame
            The filtered CFS dataset.
        
        Raises
        ------
        ValueError
            If no data is found for the provided SCTG code or mode.
        """
        cfs = self.cfs_dataset
        sctg_code = material.get_sctg_code(digits=2)

        # filter SCTG code
        if isinstance(sctg_code, int):
            cfs_filtered = cfs[cfs["SCTG"] == sctg_code]
            if cfs_filtered.empty:
                raise ValueError("Material not found in the CFS dataset")
            cfs = cfs_filtered

        # Mode
        if isinstance(mode,  TransportMode):
            cfs_modes_mapping = self.cfs_modes_mapping
            cfs_filtered = cfs[cfs["MODE"].isin(cfs_modes_mapping[mode.get_name()])]
            if cfs_filtered.empty:
                raise ValueError("Transportation mode not in CFS dataset")
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
      
        return cfs
    
    @staticmethod
    def get_distance_estimate(dataset, scenario):
        """ Get the average distance from the CFS dataset based on the scenario.
        
        Parameters
        ----------
        dataset : pandas.DataFrame
            The filtered CFS dataset.
        scenario : {'Local', 'Regional'. 'Regional_c', 'National', 'Average'}
            The scenario to filter the distances by.
        
        Returns
        -------
        float
            The average distance for the specified scenario.
        
        Raises
        ------
        ValueError
            If the scenario is not recognized.
        """
        if len(dataset) < 4 or scenario == "Average":
            return dataset["SHIPMT_DIST_ROUTED"].mean()
        else:
            if scenario == "Local":
                n = 1
            elif scenario == "Regional":
                n = 2
            elif scenario == "Regional_c":
                n = 3
            elif scenario == "National":
                n = 4
            else:
                raise ValueError(f"{scenario} scenario is not recognized")

            sorted_data = dataset["SHIPMT_DIST_ROUTED"].sort_values(ignore_index=True)
            length = len(sorted_data)
            base_size = length // 4
            extras = length % 4

            group_sizes = [base_size + (1 if i < extras else 0) for i in range(4)]

            start = sum(group_sizes[:n - 1])
            end = start + group_sizes[n - 1]

            group = sorted_data[start:end]

            return group.mean()


if __name__ == '__main__':
    pass
