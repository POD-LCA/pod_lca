

__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

from pandas import qcut

from . import TransportDataset
from ..location import Location
from ..transportation import TransportMode
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class CFSDataset(TransportDataset):
    """ A class to handle the CFS dataset for transportation legs.

    Attributes
    ----------
    force_location : bool
        If true, when location (origin/destination) not found in the dataset, use closest location.
    force_mode : bool
        If true, when mode not found in the dataset, use forced_mode
    force_mode_value : str
        The mode to use when the specified mode is not found in the dataset.
    cfs_dataset : ~pandas.DataFrame
        Pre-processed dataset from the Comodity Flow Survery (CFS).
    cfs_mode_mapping : dict
        Mapping from mode name to mode code in CFS: {**mode**(:class:`str`) : [**mode code** (:class:`int`)]}
    """

    def __init__(self):
        self.force_location = True
        self.force_mode = True
        self.force_mode_value = "Truck"
        
        self.cfs_dataset = DataImporter.csv_to_pandas(config['file_paths']['transportation']['CFS_DATA_PATH']) 
        self.cfs_modes_mapping = DataImporter.json_to_dict(config['file_paths']['transportation']['CFS_MODE_CODE'])

    def filter_datasets(self, material=None, destination=None, origin=None, mode=None):
        """ Filter the CFS dataset based on the provided parameters.
        
        Parameters
        ----------
        material : ~pod_lca.materials_screening.Product
            The Standard Classification of Transported Goods (SCTG) code to filter by.
        destination : ~pod_lca.location.Location
            The destination location to filter by.
        origin : ~pod_lca.location.Location
            The origin location to filter by.
        mode : ~pod_lca.transportation.TransportMode
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

        # Destination
        if isinstance(destination, Location):
            cfs_filtered = cfs[cfs["DEST_STATE"] == destination.get_cfs_area()]
            if cfs_filtered.empty:
                if self.force_location:
                    closest_state_name, closest_state_code = Location.get_closest_state_CFS(destination, cfs["DEST_STATE"].tolist())
                    cfs_filtered = cfs[cfs["DEST_STATE"] == closest_state_code]
                    log(f"Closest state to {destination.get_location_name()}, {closest_state_name}, is used to estimate travel distance.", "Info")
                else:
                    raise ValueError("Destination not in CFS Dataset.")
            cfs = cfs_filtered

            # Origin
            if isinstance(origin, Location):
                cfs_filtered = cfs[cfs["ORIG_STATE"] == origin.get_cfs_area()]
                if cfs_filtered.empty:
                    if self.force_location:
                        closest_state_name, closest_state_code = Location.get_closest_state_CFS(origin, cfs["ORIG_STATE"].tolist())
                        cfs_filtered = cfs[cfs["ORIG_STATE"] == closest_state_code]
                        log(f"Closest state to {origin.get_location_name()}, {closest_state_name}, is used to estimate travel distance.", "Info")
                    else:
                        raise ValueError("Origin not in CFS Dataset.")    
                cfs = cfs_filtered

        # Mode
        if isinstance(mode,  TransportMode):
            cfs_modes_mapping = self.cfs_modes_mapping
            cfs_filtered = cfs[cfs["MODE"].isin(cfs_modes_mapping[mode.get_name()])]
            if cfs_filtered.empty:
                if self.force_mode:
                    cfs_filtered = cfs[cfs["MODE"].isin(cfs_modes_mapping[self.force_mode_value])]
                    log(f"Forced mode {self.force_mode_value} is used to estimate travel distance.", "Info")
                else:
                    raise ValueError("Transportation mode not in CFS dataset")
            cfs = cfs_filtered  
        
        return cfs
    
    @staticmethod
    def get_data_bins(dataset, target_bins=3):
        """ Compute the qaurtile bins
        
        Parameters
        ----------
        dataset : pandas.DataFrame
            The filtered CFS dataset.
        target_bins : int
            Target number of bins to split the data into.

        Returns
        -------
        :class:`int`
            Number of bins realised.
        :class:`pandas.Series`
            Dataseries tagged with bin number.
        """
        for bins in range(target_bins, 0, -1):
            try:
                groups = qcut(dataset['SHIPMT_DIST_ROUTED'], q=bins, labels=[f"Q{i+1}" for i in range(bins)], duplicates='drop')
                unique_bins = groups.unique().size
                if unique_bins == bins:
                    return bins, groups
            except ValueError:
                continue
    
    @staticmethod
    def get_distance_estimate(dataset, scenario):
        """ Get the average distance from the CFS dataset based on the scenario.
        
        Parameters
        ----------
        dataset : pandas.DataFrame
            The filtered CFS dataset.
        scenario : {'Local', 'Achievable', 'Conservative', 'N/A', 'No scenario'}
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
        if scenario in ['No scenario', 'N/A']:
            return dataset['SHIPMT_DIST_ROUTED'].mean()

        bins, groups = CFSDataset.get_data_bins(dataset, target_bins=3)

        if bins == 3:
            if scenario == 'Local':
                return dataset.loc[groups == 'Q1', 'SHIPMT_DIST_ROUTED'].mean()
            elif scenario == 'Achievable':
                return dataset.loc[groups == 'Q2', 'SHIPMT_DIST_ROUTED'].mean()
            elif scenario == 'Conservative':
                return dataset.loc[groups == 'Q3', 'SHIPMT_DIST_ROUTED'].mean()
        elif bins == 2:
            if scenario == 'Local':
                return dataset.loc[groups == 'Q1', 'SHIPMT_DIST_ROUTED'].mean()
            elif scenario == 'Conservative':
                return dataset.loc[groups == 'Q2', 'SHIPMT_DIST_ROUTED'].mean()
            else:
                raise ValueError('Scenario not achievable within data.')    
        elif bins == 1:
            if scenario == 'Achievable':
                return dataset['SHIPMT_DIST_ROUTED'].mean()  
            else:
                raise ValueError('Scenario not achievable within data.')    


if __name__ == '__main__':
    pass
