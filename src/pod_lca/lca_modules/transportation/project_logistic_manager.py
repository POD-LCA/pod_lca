
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "mhtaba@uw.edu"
__version__ = "0.1.0"

import gc
import pickle

from ..impacts import Emissions
from ..impacts import Impacts
from ..transportation import LogisticLink, ForeignLink, DomesticLink


class ProjectLogisticManager:
    """ ProjectLogisticManager class which maintains the links of transportation.

    Attributes
    ----------
    name : str
        name of the project.
    links : list. # TODO: consider changing to a dictionary of goods and their links
        list of links.
    """

    def __init__(self):
        self.name = None
        self.goods_links_map = {}

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

    def set_project_origin(self, origin:(str)):
        """ Set the origin location of the project.

        Parameters
        ----------
        origin : str
            Origin location of the project.
        """
        for link in self.get_links():
            link.set_shipping_org(origin)
        # TODO consider having a project level variable for origin

    def set_project_destination(self, destination:(str)):
        """ Set the destination location of the project.

        Parameters
        ----------
        destination : str
            Destination location of the project.
        """
        for link in self.get_links():
            link.set_shipping_dest(destination)
        # TODO consider having a project level variable for origin

    def get_name(self):
        """ Retrieve the name of the project.

        Returns
        -------
        str
            Name of the project.
        """
        return self.name

    def get_links(self):
        """ Retrieve the links of the project.

        Returns
        -------
        list
            List of links.
        """
        return list(*self.goods_links_map.values())
    
    def get_link(self, product):
        """ Retrieve the links corresponding to a product.
        
        Parameters
        ----------
        product : Master Obj.
            Object for which the transportation links correspond to.
        """
        if product in self.goods_links_map:
            return self.goods_links_map[product]

    def get_goods(self):
        """ Retrieve the goods of the project.

        Returns
        -------
        list
            List of goods.
        """
        return list(self.goods_links_map.keys())

    def get_impacts(self, product=None):
        """ Retrieve the impacts of the project.

        Returns
        -------
        Impacts Obj.
            Impacts of the project.
        """
        
        if product is None:
            impact = Impacts.from_parent(self)
            for link in self.get_links():
                # link.update_inventory_records() # TODO: rename the compute_impact method to update_inventory_records
                impact += link.get_impact()

            return impact
        
        else:
            if product not in self.goods_links_map:
                raise ValueError(f"Product '{product}' not found in the project.")
            
            impact = Impacts.from_parent(self)
            for link in self.goods_links_map[product]:
                # link.update_inventory_records() # TODO: rename the compute_impact method to update_inventory_records
                impact += link.get_impact()

            return impact

    def get_emissions(self):
        """ Retrieve the emissions of the product/process.

        Returns
        -------
        Emissions Obj.
            Emissions of the product/process.
        """
        emission = Emissions.from_parent(self)
        for link in self.get_links():
            # link.update_inventory_records() # TODO: rename the compute_impact method to update_inventory_records
            impact += link.get_emission()

        return impact
    
    # ================================
    # Model Methods
    # ================================
    def add_goods(self, goods, 
                  shipping_dest, shipping_org,
                  transport_scenario:(str) = None,
                  travel_dist = None,
                  travel_dist_unit:(str) = "km", 
                  return_trip_factor:(float) = None, 
                  mode:(str) = None,
                  mode_fuel_type:(str) = "Regular", 
                  mode_efficiency:(str) = "Median"):
        """ Add goods to the project.

        Parameters
        ----------
        """
        for good in goods:
            self.goods_links_map[good] = []

            if travel_dist is None:
                if isinstance(transport_scenario, str):
                    if transport_scenario in ["North_america", "Global", "Known"]:
                        LinkClass = ForeignLink
                    elif transport_scenario in ["National", "Regional_c", "Regional", "Local", "Known_us"]:
                        LinkClass = DomesticLink
                    else:
                        raise ValueError("Transport scenario not recognized.")
                elif transport_scenario is None:
                    LinkClass = DomesticLink
                else:
                    raise TypeError("Transport scenario not recognized.")
            elif isinstance(travel_dist, (int, float)):
                LinkClass = LogisticLink
            else:
                raise ValueError("travel_dist must be a number or None.")

            link = LinkClass.in_project (self, 'transport_' + good.get_name())
            if isinstance(link, ForeignLink):
                link_domestic = DomesticLink.in_project(self, 'transport_' + good.get_name() + '_domestic')
                link.set_next(link_domestic)
            link.set_transport_scenario(transport_scenario)
            link.set_shipping_dest(shipping_dest)
            link.set_shipping_org(shipping_org)
            link.set_material(good)
            link.set_mode(mode, mode_fuel_type, mode_efficiency)
            link.set_travel_dist(travel_dist, travel_dist_unit, return_trip_factor)
            
            self.goods_links_map[good].append(link)
            if isinstance(link, ForeignLink):
                self.goods_links_map[good].append(link_domestic)

        return self

    # ================================
    # Project Methods
    # ================================
    def clear_project(self, links=True, impacts=True):  
        """ Clear the project by removing all links and impacts.
        """
        self.goods_links_map = {}

        return self

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


if __name__ == '__main__':
    pass
