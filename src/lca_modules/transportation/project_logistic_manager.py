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

    def __init__(self):

        """
        ProjectLogisticManager class which maintains the links of transportation.

        Attributes
        ----------
        name : str
            name of the project.
        shipping_dest : str.
            neme of the shipping destination location.
        shipping_org : str.
            name of the shipping origin location.
        links : list.
            list of links.
        impact : obj.
            impact object.
        """

        self.name = None
        self.shipping_dest = None 
        self.shipping_org = None 
        self.links = []
        self.impacts = Impacts.from_parent(self)


    def __str__(self):

        str = "="*75 + "\n" + f"Project: {self.get_name()}\n" + "="*75 + "\n"

        for link in self.get_links():
            str += f"{link} \n"

        return str

    # ================================
    # Constructors
    # ================================


    @classmethod
    def new(cls, name=None):

        """ Create a new project.

        Parameters
        ----------
        name : str
            Name of the project.

        Returns
        -------
        Project Obj.
            Project created.
        """

        new_project = cls()
        new_project.set_name(name)

        return new_project  


    # ================================
    # Setters and Getters
    # ================================

    def set_name(self, name:(str)):
        """ Set the name of the project.

        Parameters
        ----------
        name : str
            Name of the project.
        """

        self.name = name

        return self


    def set_shipping_dest(self, shipping_dest:(str)):
        """ Set the shipping destination of the project.

        Parameters
        ----------
        shipping_dest : str
            Name of the shipping destination location.
        """

        self.shipping_dest = Location.from_str (shipping_dest)

        return self


    def set_shipping_org(self, shipping_org:(str)):
        """ Set the shipping origin of the project.

        Parameters
        ----------
        shipping_org : str
            Name of the shipping origin location.
        """

        self.shipping_org = Location.from_str (shipping_org)

        return self

    #TO DO: Add the method to update the destination and origin location in the links.

    def get_name(self):
        """
        Retrieve the name of the project.

        Returns
        -------
        str
            Name of the project.
        """
        return self.name

    def get_shipping_dest(self):
        """
        Retrieve the shipping destination of the project.

        Returns
        -------
        str
            Name of the shipping destination location.
        """
        return self.shipping_dest

    def get_shipping_org(self):
        """
        Retrieve the shipping origin of the project.

        Returns
        -------
        str
            Name of the shipping origin location.
        """
        return self.shipping_org

    def get_links(self):
        """
        Retrieve the links of the project.

        Returns
        -------
        list
            List of links.
        """
        return self.links

    def get_impacts(self):
        """
        Retrieve the impacts of the project.

        Returns
        -------
        Impacts Obj.
            Impacts of the project.
        """
        return self.impacts
    
    # ================================
    # Model Methods
    # ================================


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



if __name__ == '__main__':
    pass





