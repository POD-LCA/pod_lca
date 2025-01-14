from utilities.objects import array_methods


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class HotSpotAnalysis:
    """
    HotSpotAnalysis object carries out hotspot analysis and stores data.

    Attributes
    ----------
    project : Project Obj.
        Project on which the calculator operates.
    hotspots : dict of dict of list
        {model_name (str): {impact_category (str): list (Master Obj)} .
    """

    def __init__(self, project):
        self.project = project
        self.hotspots = dict.fromkeys(project.get_model_names(), None)

        project.HotSpotAnalysis = self

    def run(self, model_name='Model_0', impact_category= "GWP", printout=False):
        """ Determines the hotspot of the model.
            The hotspots are the largest group out of (a) top 20% contributors to the impact or (b) the smallest group of contributors to the 80% (or more) of GWP.

            Parameters
            ----------
            model : str
                Name of the model considered.
            impact_category : str
                Impact category considered.
            printout : bool
                Printout the results if true.
            
            Retrurn
            -------
            List of Master Obj.
                Hotspot objects.
        """

        impacts = self.project.get_model(model_name).get_impacts()

        impacts_lst = []
        for key, list in impacts.items():
            impacts_lst.extend(list)

        if len(impacts_lst) > 0:
            if impact_category == 'weighted':
                val_lst = [impact.get_weighted_impact() for impact in impacts_lst]
            else:
                val_lst = [impact.get_impact(impact_category) for impact in impacts_lst]
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

            if printout:
                print("*"*50 + "\nHOTSPOTS\n" + "*"*50)
                for obj in hot_spots:
                    
                    if impact_category == 'weighted':
                        impact_val = obj.get_impacts().get_weighted_impact()
                    else:
                        impact_val = obj.get_impacts().get_impact(impact_category)
                    print(obj, "Impact ({}):".format(impact_category), impact_val)
            
            self.set_hotspots(hot_spots, model_name)
            hot_spots_dict = self.hotspots[model_name]
            if hot_spots_dict == None:
                hot_spots_dict = {impact_category: hot_spots}
            else:
                hot_spots_dict[impact_category] = hot_spots
            self.hotspots[model_name] = hot_spots_dict

            return hot_spots
    
    def set_hotspots(self, hotspots, model_name):
        """ Set attribute in hotspots to identify as hotspots.

            Parameters
            ----------
            hotspots : list of Master Objs.
                List of hotspot object of the model.
            model_name : str.
                Name of the model

        """
        
        model = self.project.get_model(model_name)
        all_items = model.get_products() + model.get_processes()

        array_methods.set_value(all_items, 'is_hotspot', False)
        array_methods.set_value(hotspots, 'is_hotspot', True)


    def get_hotspots(self, model_name='Model_0', impact_category='GWP'):
        """ Get hotspots of the model.

            Parameters
            ----------
            model_name : str
                Name of the model.
            impact_category : str
                Impact category.

            Returns
            ----------
            list of Master Objs.
                List of hotspot object of the model.
                None if hotspots are not set.

        """

        if self.hotspots[model_name][impact_category] == None:
            print("No hotspots set yet. Run hotspot analysis first.")
        else:
            return self.hotspots[model_name][impact_category]
