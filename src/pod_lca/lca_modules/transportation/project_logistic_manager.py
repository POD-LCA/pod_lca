
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

import gc

from ..impacts import Impacts
from ..location import Location
from ..transportation import Link


class ProjectLogisticManager:
    """
    ProjectLogisticManager class which maintains the links of transportation.

    Attributes
    ----------
    name : int.
        name of the project.
    shipping_dest : str.
        neme of the shipping destination location.
    shipping_org : str.
        name of the shipping origin location.
    links : list.
        list of links.
    impact : obj.
        impact object.
    subdataset : dict.
        dictionary of subdatasets.
    """
    def __init__(self, name, shipping_dest, shipping_org):
        self.name = name
        self.shipping_dest = None if shipping_dest is None else Location.from_str (shipping_dest)
        self.shipping_org = None if shipping_org is None else Location.from_str (shipping_org)
        self.links = []
        self.impacts = Impacts.from_parent(self)

        # TODO: create constructor method
        # TODO: create setters
        # TODO: create __str__ method
    
    #TODO: this to move as a constructor method in Link class
    def create_link(self, material, qty, travel_dist, return_trip_factor, dist_unit, mode_name, feul_type, mode_dms_name, efficiency, efficiency_dms):
        """
        Create a link of transportation for the project.
        """
        link = Link(self, material, qty, travel_dist, return_trip_factor, dist_unit, mode_name, feul_type, mode_dms_name, efficiency, efficiency_dms)
        self.links.append(link)

        link.compute_impact()
        
    # TODO: Is get_total_impacts() a more appropriate method name?
    def get_links_impacts(self):
        """
        Retrieve the impacts of the links.
        """

        new_impact = Impacts.from_parent(self)
        for link in self.links:
            new_impact += link.get_impact()
        
        self.impacts.update_qty(new_impact.get_record_dict())

        del new_impact
        gc.collect()

        return self.impacts 

    # ========================
    # Getters
    # ========================
    def get_name(self):
        """ Retrieve the name of the project.

            Returns
            -------
            str
                Name of the project.
        """
        return self.name


    def get_impacts(self):
        """ Retrieve the impacts of the Transportation.

            Returns
            -------
            Impacts Obj.
                Impacts of the Transportation.

        """
        return self.impacts

    def get_links (self):
        """ Retrieve the links of the project.

            Returns
            -------
            list
                List of transportation links of the project
        """
        return self.links

    def get_shipping_dest (self):
        """ Retrieve the shipping destination of the project.
        """
        return self.shipping_dest

    def get_shipping_org (self):
        """ Retrieve the shipping origin of the project.
        """
        return self.shipping_org


if __name__ == '__main__':
    pass
