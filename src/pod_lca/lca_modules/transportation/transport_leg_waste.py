__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from . import ElectricTransportMode
from . import TransportMode
from .transport_leg import TransportationLeg
from ..impacts import Impacts
from ..impacts import Emissions
from ..location import Location
from ...units import KILOMETER
from ...utilities import config
from ...utilities import DataImporter
from ...utilities import log


class WasteTransportLeg(TransportationLeg):
    """A leg of waste transportation.

    Attributes
    ----------
    transport_scenario : str
        A discriptor of the tranportation scenario.
    eol_pathway : {'Landfill', 'Recycle', 'Compost', 'Incinerate'}
            End-of-life pathway: \n
            - 'Landfill': transporting waste to a landfill.
            - 'Recycle': transporting waste to a recycler.
            - 'Compost': transporting to a composting facility.
            - 'Incinerate': transporting to an incinerator.
    distance_cut_off: str
        cut-off length for the waste transportation leg.
    """

    def __init__(self):
        super().__init__()
        self.transport_scenario = None
        self.eol_pathway = None
        self.distance_cut_off = None

        self._cache_travel_dist = None
        self._last_params = None

    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_object(cls, material, manager, eol_pathway, transport_scenario="High"):
        """Create.

        Parameters
        ----------
        material : ~pod_lca.eol.WasteProcess
            Material keeping quantity and unit record.
        manager : ~pod_lca.materials_screening.Model or ~pod_lca.buildings.Building
            Manager keeping the end-of-life transport datasets.
        eol_pathway : {'Landfill', 'Recycle', 'Compost', 'Incinerate'}
            End-of-life pathway: \n
            - 'Landfill': transporting waste to a landfill.
            - 'Recycle': transporting waste to a recycler.
            - 'Compost': transporting to a composting facility.
            - 'Incinerate': transporting to an incinerator.
        transport_scenario : {'Min', 'Average', 'High'}
            Transport scenario of the transportation leg. Default is 'High'.
        """
        waste_transportation_leg = cls()

        waste_transportation_leg.set_material(material)
        waste_transportation_leg.set_manager(manager)
        waste_transportation_leg.set_name(material.get_name())

        waste_transportation_leg.impacts = Impacts.from_parent(waste_transportation_leg)
        waste_transportation_leg.emissions = Emissions.from_parent(waste_transportation_leg)

        waste_transportation_leg.set_transport_scenario(transport_scenario)
        waste_transportation_leg.set_eol_pathway(eol_pathway)
        waste_transportation_leg.set_mode()  # TODO: check defaulting values used here
        waste_transportation_leg.set_travel_dist()  # TODO: check defaulting values used here
        waste_transportation_leg.set_shipping_destination(shipping_dest=None)
        waste_transportation_leg.set_shipping_origin(manager.get_location())

        return waste_transportation_leg

    # ================================
    # Setters
    # ================================
    def set_transport_scenario(self, transport_scenario: str):
        """Set the transport scenario of the transportation leg.

        Parameters
        ----------
        transport_scenario : {'Min', 'Average', 'High'}
            Transport scenario of the transportation leg.

        Raises
        ------
        ValueError
            Transportation scenario not recognized.
        TypeError
            Transportation scenario is not None or a string.
        """
        if transport_scenario is None:
            self.transport_scenario = None
        elif isinstance(transport_scenario, str):
            if transport_scenario in ["Min", "Average", "High"]:
                self.transport_scenario = transport_scenario
            else:
                raise ValueError("Transportation scenario not recognized")
        else:
            raise TypeError("Transport scenario must be a string.")

        self._invalidate_cache()
        return self

    def set_eol_pathway(self, eol_pathway):
        """Set the end-of-life pathway corresponding to the waste transportation leg.

        Parameters
        ----------
        eol_pathway : {'Landfill', 'Recycle', 'Compost', 'Incinerate'}
            End-of-life pathway: \n
            - 'Landfill': transporting waste to a landfill.
            - 'Recycle': transporting waste to a recycler.
            - 'Compost': transporting to a composting facility.
            - 'Incinerate': transporting to an incinerator.
        """
        self.eol_pathway = eol_pathway

        return self

    def set_material(self, material):
        """Set the material being transported.

        Parameters
        ----------
        material : ~pod_lca.materials_screening.Product
            Material name of the transportation leg.
        """
        self = super().set_material(material)
        self._invalidate_cache()
        return self

    def set_shipping_destination(self, shipping_dest):
        """Set the shipping destination of the project.

        Parameters
        ----------
        shipping_dest : ~pod_lca.location.Location
            Name of the shipping destination location.
        """
        self = super().set_shipping_destination(shipping_dest)
        self._invalidate_cache()
        return self

    def set_shipping_origin(self, shipping_org):
        """Set the shipping origin of the project.

        Parameters
        ----------
        shipping_org : ~pod_lca.location.Location
            Name of the shipping origin location.
        """
        self = super().set_shipping_origin(shipping_org)
        self._invalidate_cache()
        return self

    def set_mode(self, mode=None, efficiency=None):
        """Set the transportation mode of the transportation leg.

        Note
        ----
        1. Prefix `'E_'` in the mode_name is used as the identifier of an electricity based transportation mode.
        2. Electric vehicles takes electricity based on origin location.

        Parameters
        ----------
        mode : str or ~pod_lca.transportation.TransportMode
            transportation mode of the transportation leg.
        efficiency : {'High', 'Median', 'Low'}
            efficiency of the transportation mode. Default is 'Median'.
        """
        if isinstance(mode, TransportMode):
            self.mode = mode
        else:
            mode_efficiency = "Median" if efficiency is None else efficiency
            mode_name = "Truck" if mode is None else mode

            if mode_name[0:2] == "E_":
                self.mode = ElectricTransportMode.new(mode_name[2:], mode_efficiency)
                self.mode.set_location(self.get_shipping_origin())
            else:
                self.mode = TransportMode.new(mode_name, mode_efficiency)

        self.mode.set_parent(self)
        self.mode.set_inventory_records()

        self._invalidate_cache()
        return self

    def set_cutoff_distance(self):
        """Set the cut-off length for the waste transportation leg."""
        dataset = self.get_dataset()

        conversion_factor = self.get_dist_unit().convert_to(KILOMETER)
        dataset_filtered = dataset.filter_datasets(self.get_shipping_origin(), "Landfill")

        self.distance_cut_off = (
            2 * dataset.get_distance_estimate(dataset_filtered, self.get_transport_scenario()) * conversion_factor
        )

        return self

    def set_travel_dist(self, travel_dist=None, dist_unit=None, return_trip_factor=None):
        """Set the travel distance of the transportation leg.

        Parameters
        ----------
        travel_dist : None
            For DomesticLink objects travel distance are autogenerated from CFS data.
        dist_unit : ~pod_lca.units.Unit
            Unit of the travel distance.
        return_trip_factor : float
            Return trip factor of the transportation leg (default is None).
        """
        self.dist_unit = KILOMETER if dist_unit is None else dist_unit
        self.return_trip_factor = 1.0 if return_trip_factor is None else return_trip_factor
        self._invalidate_cache()
        return self

    # ================================
    # Getters
    # ================================
    def get_transport_scenario(self):
        """Retrieve the transport scenario of the transportation leg.

        Returns
        -------
        str
            The transport scenario of the transportation leg.
        """
        return self.transport_scenario

    def get_travel_dist(self):
        """Set the travel distance of the transportation leg.

        Returns
        -------
        float or str
            travel distance of the transportation leg.

        Raises
        ------
        ValueError
            Transport scenario not recognized.
        """
        current_params = (
            self.get_material(),
            self.get_shipping_destination(),
            self.get_shipping_origin(),
            self.get_mode().get_name(),
            self.get_mode().get_efficiency(),
            self.get_transport_scenario(),
            self.get_dist_unit(),
        )

        if self._last_params == current_params and self._cache_travel_dist is not None:
            log("Returning cached result.", "Info")
            return self._cache_travel_dist
        else:
            transport_scenario = self.get_transport_scenario()
            if transport_scenario in ["Min", "Avg", "High"]:
                travel_dist = self.get_distance_from_dataset(transport_scenario)
            else:
                raise ValueError("Transport scenario not recognized.")

            self._cache_travel_dist = travel_dist
            self._last_params = current_params

            return travel_dist

    def get_return_trip_factor(self):
        """Retrieve the return trip factor of the transportation leg.

        Returns
        -------
        float
            The return trip factor of the transportation leg.
        """
        return self.return_trip_factor

    def get_eol_pathway(self):
        """Get the end-of-life pathway corresponding to the waste transportation leg.

        Returns
        -------
        str
            End-of-life pathway.
        """
        return self.eol_pathway

    def get_cutoff_distance(self):
        """Retrieve the cut-off length for the waste transportation leg.

        Returns
        -------
        float or int
            Cut-off distance
        """
        if self.distance_cut_off is None:
            self.set_cutoff_distance()

        return self.distance_cut_off

    def get_dataset(self):
        """Get the dataset.

        Returns
        -------
        ~pod_lca.transportation.TransportDataset
            Dataset
        """
        return self.get_manager().get_eol_transport_dataset()

    def get_impact_database(self):
        """Get the impact database.

        Returns
        -------
        ~pod_lca.impacts.ImpactsDatabase
            Impacts database
        """
        return self.get_manager().get_transportation_impact_database()

    # ================================
    # CFS Methods
    # ================================
    def get_distance_from_dataset(self, transport_scenario):
        """Get the average distance from the CFS dataset based on the scenario.

        Parameters
        ----------
        scenario : {'Min', 'Average', 'High'}
            The scenario to filter the distances by.

        Returns
        -------
        float
            The distance estimate for the specified scenario.
        """
        dataset = self.get_dataset()

        conversion_factor = self.get_dist_unit().convert_to(KILOMETER)
        dataset_filtered = dataset.filter_datasets(self.get_shipping_origin(), self.get_eol_pathway())
        travel_dist = dataset.get_distance_estimate(dataset_filtered, transport_scenario) * conversion_factor

        return travel_dist

    # ================================
    # Cache Method
    # ================================
    def _invalidate_cache(self):
        self._cache_travel_dist = None
        self._last_params = None


class EOLTransportDataset:
    """A class to handle end-of-life transportation dataset."""

    def __init__(self):
        self.dataset = DataImporter.csv_to_pandas(config["file_paths"]["transportation"]["WASTE_TRANSPORT"])

    def filter_datasets(self, origin=None, eol_pathway=None):
        """Filter the CFS dataset based on the provided parameters.

        Parameters
        ----------
        sctg : int, optional
            The Standard Classification of Transported Goods (SCTG) code to filter by.
        origin : ~pod_lca.location.Location, optional
            The origin location to filter by.
        eol_pathway : ~pod_lca.transportation.TransportMode, optional
            The transportation mode to filter by.

        Returns
        -------
        pandas.DataFrame
            The filtered dataset.
        """
        dataset = self.dataset

        # Origin
        if isinstance(origin, Location):
            dataset_filtered = dataset[dataset["origin_state"] == origin.get_state_abbr()]
            if dataset_filtered.empty:
                raise ValueError("Origin state not in dataset")
            dataset = dataset_filtered

        # EOL_pathway
        if eol_pathway in ["Landfill", "Recycle", "Compost", "Incinerate"]:
            dataset_filtered = dataset[dataset["eol_pathway"] == eol_pathway]
            if dataset_filtered.empty:
                raise ValueError("End-of-life pathway not in dataset")
            dataset = dataset_filtered

        return dataset

    @staticmethod
    def get_distance_estimate(dataset, scenario):
        """Get the average distance from the CFS dataset based on the scenario.

        Parameters
        ----------
        dataset : pandas.DataFrame
            The filtered dataset.
        scenario : {'Min', 'Average', 'High'}
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
        if len(dataset) < 3:
            domestic_dis = dataset["distance (km)"].mean()
        else:
            if scenario == "Min":
                domestic_dis = dataset["distance (km)"].min()
            elif scenario == "Average":
                domestic_dis = dataset["distance (km)"].mean()
            elif scenario == "High":
                domestic_dis = dataset["distance (km)"].max()
            else:
                raise ValueError(f"{scenario} scenario is not recognized")

        return domestic_dis


if __name__ == "__main__":
    pass
