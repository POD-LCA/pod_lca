__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"


class TransportDataset:
    """An abstract class to handle the dataset for transportation legs."""

    def filter_datasets(self, material=None, destination=None, origin=None, mode=None, **kwargs):
        """Filter the CFS dataset based on the provided parameters.

        Parameters
        ----------
        material : ~pod_lca.materials_screening.Product
            Material considered.
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
        """
        pass

    @staticmethod
    def get_distance_estimate(dataset, **kwargs):
        """Get the average distance from the CFS dataset based on the scenario.

        Parameters
        ----------
        dataset : pandas.DataFrame
            The filtered dataset.

        Returns
        -------
        float
            The average distance for the specified scenario.
        """
        pass


if __name__ == "__main__":
    pass
