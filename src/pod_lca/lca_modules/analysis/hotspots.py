__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from ..materials_screening import Model
from ...utilities import ArrayMethods
from ...utilities import config


class HotSpotAnalysis:
    """HotSpotAnalysis object carries out hotspot analysis and stores data.

    Attributes
    ----------
    model : ~pod_lca.materials_screening.Model
        Model on which the hotspot analysis is performed.
    hotspots : dict of list
        {**impact_category** (:class:`str`): :class:`list` of :class:`~pod_lca.materials_screening.Master`}.
    transportation_grouping : {'not_grouped', 'with_material', 'all_transportation'}, optional
        Method for grouping transportation impacts. Default is 'not_grouped'.
    """

    def __init__(self):
        self.model = None
        self.hotspots = {}

        # settings
        self.transportation_grouping = "not_grouped"

    def __str__(self):
        str = "*" * 50 + "\nHOTSPOTS\n" + "*" * 50 + "\n"
        hotspots = self.get_hotspots()
        if hotspots is None:
            str += "No hotspot analysis has been run yet."
        else:
            for impact_category in hotspots:
                for obj in hotspots[impact_category]:
                    str += f"{obj['item'].get_name()}: {impact_category} = {obj['val']:.2f} {config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES'][impact_category]} \n"

        return str

    # ================================
    # Constructors
    # ================================
    @classmethod
    def from_model(cls, model):
        """Create a hotspot analyis from a a model.

        Parameters
        ----------
        model : ~pod_lca.materials_screening.Model
            Model on which the hotspot analysis is performed.
        """
        hotspot_analysis = cls()
        hotspot_analysis.set_model(model)

        model.hotspots = hotspot_analysis.hotspots

        return hotspot_analysis

    # ================================
    # Setters and Getters
    # ================================
    def set_model(self, model):
        """Set a model to the analyser.

        Parameters
        ----------
        model : ~pod_lca.materials_screening.Model
            Model on which the hotspot analysis is performed.
        """
        self.model = model

        return self

    def set_hotspots(self, impact_category):
        """Set attribute in hotspots to identify as hotspots.

        Parameters
        ----------
        hotspots : list of ~pod_lca.materials_screening.Master
            List of hotspot object of the model.
        impact_category : str
            Impact category for which the hotspot analysis was run.
        """
        if impact_category not in self.hotspots:
            self.run(impact_category)

        all_items = self.model.get_all_items()

        ArrayMethods.set_value(all_items, "is_hotspot", False)
        if self.transportation_grouping == 'all_transportation':
            self.model.get_transportation_manager().is_hotspot = False

        ArrayMethods.set_value([hotspot['item'] for hotspot in self.hotspots[impact_category]], "is_hotspot", True)

        return self

    def get_model(self):
        """Get the model for which the analsysis will be run.

        Returns
        ----------
        ~pod_lca.materials_screening.Model
            Model on which the hotspot analysis is performed.
        """
        return self.model

    def get_hotspots(self):
        """Get hotspots of the model.

        Returns
        ----------
        dict
            {**impact_category** (:class:`str`): :class:`list` of :class:`~pod_lca.materials_screening.Master`}
        """
        return self.hotspots

    def get_hotspots_by_impact_category(self, impact_category):
        """Get hotspots of the model, by the impact category.

        Parameters
        ----------
        impact_category : str
            Impact category.

        Returns
        ----------
        list of ~pod_lca.materials_screening.Master
            List of hotspot object of the model.None if hotspots are not set.
        """
        if impact_category not in self.hotspots:
            self.run(impact_category)

        return self.hotspots[impact_category]

    # ================================
    # Methods
    # ================================
    def run(self, impact_category="GWP"):
        """Determines the hotspot of the model.
            The hotspots are the largest group out of \n
            - top 20% contributors to the impact or
            - the smallest group of contributors to the 80% (or more) of the impact category specified.

        Parameters
        ----------
        model : str
            Name of the model considered.
        impact_category : str
            Impact category considered.

        Return
        -------
        list of ~pod_lca.materials_screening.Master
            Hotspot objects.
        """
        if isinstance(self.model, Model):
            impacts = self.model.get_impacts(transportation_grouping=self.transportation_grouping, 
                                             plus_minus_accounting=False)
        else:
            impacts = self.model.get_impacts()

        impacts_lst = []
        for key, list in impacts.items():
            impacts_lst.extend(list)

        if len(impacts_lst) > 0:
            if impact_category == "weighted":
                val_lst = [impact.get_weighted_impact() for impact in impacts_lst]
            else:
                val_lst = [impact.get_record(impact_category) for impact in impacts_lst]
            total_impact = sum(val_lst)
            no_contributors = len(val_lst)

            hot_spots = []

            biggest_contribution = max(val_lst)
            if biggest_contribution == 0.0:
                self.hotspots[impact_category] = []
                return None
            max_index = val_lst.index(biggest_contribution)
            hot_spots.append(
                {
                    "item":impacts_lst[max_index].get_parent(),
                    "val":biggest_contribution
                }
                )
            contributions_in_hotspots = biggest_contribution

            all_found = (
                True
                if len(hot_spots) >= 0.2 * no_contributors and contributions_in_hotspots >= 0.8 * total_impact
                else False
            )

            while not all_found:
                val_lst[max_index] = 0.0

                biggest_contribution = max(val_lst)
                if biggest_contribution == 0.0:
                    break
                max_index = val_lst.index(biggest_contribution)
                hot_spots.append(
                    {
                    "item":impacts_lst[max_index].get_parent(),
                    "val":biggest_contribution
                    }
                    )
                contributions_in_hotspots += biggest_contribution

                all_found = (
                    True
                    if len(hot_spots) >= 0.2 * no_contributors and contributions_in_hotspots > 0.8 * total_impact
                    else False
                )

            self.hotspots[impact_category] = hot_spots
            self.set_hotspots(impact_category)

            return hot_spots
        
        else:
            self.hotspots[impact_category] = []
            return None

if __name__ == "__main__":
    pass
