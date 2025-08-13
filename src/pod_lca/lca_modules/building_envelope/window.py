
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import json

# from pod_lca.utilities.geometry import area_polygon


class Window:

    def __init__(self):
        self.name = None
        self.nodes = None
        self.building_surface = None
        self.construction = None

    def to_json(self, filepath):
        """
        Serialize the data representation of the window to a JSON file

        Parameters
        ----------
        filepath: str
            Path for the JSON file to be created
        
        Returns
        -------
        None

        """
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    @property
    def data(self):
        data = {'name'                  : self.name,
                'nodes'                 : self.nodes,
                'building_surface'      : self.building_surface,
                'construction'          : self.construction,
                }
        return data
    
    @property
    def area(self):
        pts = self.nodes
        return area_polygon(pts)

    @data.setter
    def data(self, data):
        self.name               = data.get('name') or {}
        self.nodes              = data.get('nodes') or {}
        self.building_surface   = data.get('building_surface') or {}
        self.construction       = data.get('construction') or {}

    @classmethod
    def from_data(cls, data):
        """
        Create a new instance of the window datastructure from a data dictionary.

        Parameters
        ----------
        data: dict
            Data dictionary
        
        Returns
        -------
        Window
            The instance of the window datastructure
        
        """
        window = cls()
        window.data = data
        return window

    @classmethod
    def from_json(cls, filepath):
        """
        Create a new instance of the window datastructure from a JSON file

        Parameters
        ----------
        filepath: str
            Path to the JSON file
        
        Returns
        -------
        Window
            The instance of the window datastructure
        
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        window = cls()
        window.data = data
        return window


if __name__ == "__main__":

    for i in range(50): print('')

    w = Window()
    width = 1.
    length = 1.
    w.nodes = [[0,0,0], [width,0,0], [width, length, 0], [0,length, 0]]
    print(w)