from lca_modules.transportation.logistics_link import Link
from lca_modules.transportation.scenarios import Scenario

from lca_modules.impacts.impacts import Impacts
import gc

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"



class ProjectLogisticManager:
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

    def __init__(self):

        self.name = None
        self.links = {}
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

    def get_link(self, link_name:(str)):
        """
        Retrieve a link from the project.

        Parameters
        ----------
        link_name : str
            Name of the link to be retrieved.

        Returns
        -------
        Link Obj.
            The link object if found, else None.
        """

        if link_name in self.links:
            return self.links[link_name]
        else:
            raise ValueError(f"Link '{link_name}' not found in the project.")

    def get_link_names(self):
        """
        Retrieve the names of all the links in the project.

        Returns
        -------
        list
            List of link names.
        """

        return list(self.links.keys())
    
    # ================================
    # Model Methods
    # ================================

    def add_link(self, link_name:(str), shipping_dest:(str) = None, shipping_org:(str) = None,
                material:(str) = None, qty:(float) = None, qty_unit:(str) = "tonne", travel_dist = None,
                travel_dist_unit:(str) = "km", return_trip_factor:(float) = None, mode_domestic:(str) = None,
                mode_domestic_fuel_type:(str) = "Regular", mode_domestic_efficiency:(str) = "Median",
                mode_foreign:(str) = None, mode_foreign_fuel_type:(str) = "Regular", mode_foreign_efficiency:(str) = "Median"):

        """
        Add a link to the project.

        Parameters
        ----------
        link_name : str
            Name of the link to be added.
        """

        link = Link.in_project (self, link_name)
        link.set_name(link_name)
        link.set_shipping_dest(shipping_dest)
        link.set_shipping_org(shipping_org)
        link.set_material(material, qty, qty_unit)
        link.set_travel_dist(travel_dist, travel_dist_unit, return_trip_factor)
        link.set_mode_domestic(mode_domestic, mode_domestic_fuel_type, mode_domestic_efficiency)
        link.set_mode_foreign(mode_foreign, mode_foreign_fuel_type, mode_foreign_efficiency)


        self.links[link_name] = link

        return link


    # ================================
    # Project Methods
    # ================================


    def clear_project(self, links=True, impacts=True):  
        """
        Clear the project by removing all links and impacts.

        Parameters
        ----------
        links : bool, optional
            If True, clear all links. Default is True.
        impacts : bool, optional
            If True, clear all impacts. Default is True.
        """

        if links:
            self.links = {}

        if impacts:
            self.impacts = None


    def save(self, file_path:(str)):
        """ Save as a *.pkl file.

        Parameters
        ----------
        file_path : str
            Location (including the name) where the data be saved.
        """
        
        with open(file_path, "wb") as file:
            pickle.dump(self, file)


    @staticmethod
    def load(file_path:(str)):
        """ Load a project from a pickled file.

        Parameters
        ----------
        file_path : str
            Location (including the name) where the data be loaded from.

        Raises
        ------
        FileNotFoundError
            File not found.
        PermissionError
            Permission denied to access file.
        """

        try:
            with open(file_path, 'rb') as file:
                project = pickle.load(file)
            return project
        except FileNotFoundError:
            print("File not found.")
        except PermissionError:
            print("Permission denied.")
        except Exception as e:
            print("An error occurred:", e)


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





