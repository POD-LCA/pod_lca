
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.utilities import ArrayMethods
from pod_lca.utilities import config
from pod_lca.utilities import log


class HotSpotAnalysis:
    """ HotSpotAnalysis object carries out hotspot analysis and stores data.

    Attributes
    ----------
    model : Model Obj.
        Model on which the hotspot analysis is performed.
    hotspots : dict of list
        {impact_category (str): list (Master Obj)} .
    """

    def __init__(self):
        self.model = None
        self.hotspots = {}

    def __str__(self):
        str = "*"*50 + "\nHOTSPOTS\n" + "*"*50 + "\n"
        hotspots = self.get_hotspots()
        if hotspots is None:
            str += "No hotspot analysis has been run yet."
        else:
            for impact_category in hotspots:
                for obj in hotspots[impact_category]:
                    if impact_category == 'weighted':
                        impact_val = obj.get_impacts().get_weighted_impact()
                    else:
                        impact_val = obj.get_impacts().get_record(impact_category)
                    str += f"{obj.get_name()}: {impact_category} = {impact_val:.2f} {config['setup']['INVENTORY_ITEMS']['IMPACT_CATEGORIES'][impact_category]} \n"
        
        return str

    # ================================
    # Constructors
    # ================================  
    @classmethod
    def from_model(cls, model):
        """ Create a hotspot analyis from a a model.
        
        Attributes
        ----------
        model : Model Obj.
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
        """ Set a model to the analyser.
        
        Attributes
        ----------
        model : Model Obj.
            Model on which the hotspot analysis is performed.        
        """
        self.model = model

    def set_hotspots(self, hotspots, impact_category):
        """ Set attribute in hotspots to identify as hotspots.

        Parameters
        ----------
        hotspots : list of Master Objs.
            List of hotspot object of the model.
        impact_category : str
            Impact category for which the hotspot analysis was run.
        """
        self.hotspots[impact_category] = hotspots

        all_items = self.model.get_all_items()

        ArrayMethods.set_value(all_items, 'is_hotspot', False)
        ArrayMethods.set_value(hotspots, 'is_hotspot', True)

    def get_model(self):
        """ Get the model for which the analsysis will be run.
    
        Returns
        ----------
        Model Obj.
            Model on which the hotspot analysis is performed.        
        """
        return self.model
    
    def get_hotspots(self):
        """ Get hotspots of the model.

        Returns
        ----------
        dict.
            {impact_category (str): list (Master Obj)} .
        """

        return self.hotspots

    def get_hotspots_by_impact_category(self, impact_category):
        """ Get hotspots of the model, by the impact category.

        Parameters
        ----------
        impact_category : str
            Impact category.

        Returns
        ----------
        list of Master Objs.
            List of hotspot object of the model.
            None if hotspots are not set.
        """
        if impact_category in self.hotspots:
            return self.hotspots[impact_category]
        else:
            log("No hotspots set yet. Run hotspot analysis first.", "Warn")

    # ================================
    # Methods
    # ================================
    def run(self, impact_category= "GWP"):
        """ Determines the hotspot of the model.
            The hotspots are the largest group out of (a) top 20% contributors to the impact or 
            (b) the smallest group of contributors to the 80% (or more) of the impact category specified.

        Parameters
        ----------
        model : str
            Name of the model considered.
        impact_category : str
            Impact category considered.
        
        Retrurn
        -------
        List of Master Obj.
            Hotspot objects.
        """
        for item in self.model.get_all_items():
            item.update_inventory_records()
            
        impacts = self.model.get_impacts()

        impacts_lst = []
        for key, list in impacts.items():
            impacts_lst.extend(list)

        if len(impacts_lst) > 0:
            if impact_category == 'weighted':
                val_lst = [impact.get_weighted_impact() for impact in impacts_lst]
            else:
                val_lst = [impact.get_record(impact_category) for impact in impacts_lst]
            total_impact = sum(val_lst)
            no_contributors = len(val_lst)

            hot_spots =[]
            
            biggest_contribution = max(val_lst)
            if biggest_contribution == 0.0:
                return None
            max_index = val_lst.index(biggest_contribution)
            hot_spots.append(impacts_lst[max_index].get_parent())
            contributions_in_hotspots = biggest_contribution

            all_found = True if len(hot_spots) >= 0.2 * no_contributors and contributions_in_hotspots >= 0.8 * total_impact else False
            
            while not all_found:
                val_lst[max_index] = 0.0

                biggest_contribution = max(val_lst)
                if biggest_contribution == 0.0:
                    break
                max_index = val_lst.index(biggest_contribution)
                hot_spots.append(impacts_lst[max_index].get_parent())
                contributions_in_hotspots += biggest_contribution

                all_found = True if len(hot_spots) >= 0.2 * no_contributors and contributions_in_hotspots > 0.8 * total_impact else False
            
            self.set_hotspots(hot_spots, impact_category)

            return hot_spots
        

if __name__ == '__main__':
    pass
