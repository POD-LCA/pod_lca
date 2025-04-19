import os
import pandas as pd
from lca_modules.transportation.logistics_link import Link
from lca_modules.transportation.scenarios import Scenario
from lca_modules.location.location import Location
from lca_modules.impacts.impacts import Impacts
import gc

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class ProjectLogisticManager:

    def __init__(self, name, shipping_dest, shipping_org):

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

        self.name = name
        self.shipping_dest = None if shipping_dest is None else Location.from_str (shipping_dest)
        self.shipping_org = None if shipping_org is None else Location.from_str (shipping_org)
        self.links = []
        self.impacts = Impacts.from_parent(self)


    def create_link(self, material, qty, travel_dist, return_trip_factor, dist_unit, mode_name, feul_type, mode_dms_name, efficiency, efficiency_dms):
        """
        Create a link of transportation for the project.
        """
        link = Link(self, material, qty, travel_dist, return_trip_factor, dist_unit, mode_name, feul_type, mode_dms_name, efficiency, efficiency_dms)
        self.links.append(link)

        link.compute_impact()
        
    def get_links_impacts(self):

        """
        Retrieve the impacts of the links.
        """

        new_impact = Impacts.from_parent(self)
        for link in self.links:
            new_impact += link.get_impact()
        
        self.impacts.update_impact_qty(new_impact.get_impact_dict())

        del new_impact
        gc.collect()

        return self.impacts 

    def get_name(self):
        """
        Retrieve the name of the project.
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
        """
        Retrieve the links of the project.
        """
        return self.links

    def get_shipping_dest (self):
        """
        Retrieve the shipping destination of the project.
        """
        return self.shipping_dest

    def get_shipping_org (self):
        """
        Retrieve the shipping origin of the project.
        """

        return self.shipping_org







