from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import json
from pod_lca.utilities import Mesh



class Zone(object):
    """
    Zone datastructure for energy+ analysis. 

    Parameters
    ----------
    name: str, optional
        Name for the zone
    surfaces: object
        A compas mesh representing the surfaces of the zone
    
    """
    def __init__(self):
        self.name =  ''
        self.surfaces = None
        self.volume = 0.
        self.origin = [0., 0., 0.]
        self.height = 0

    def to_json(self, filepath):
        """
        Serialize the data representation of the zone to a JSON file

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
    def area(self):
        for fk in self.surfaces.faces():
            st = self.surfaces.face_attribute(fk, 'surface_type')
            if st == 'Floor':
                return self.surfaces.face_area(fk)

    @property
    def centroid_xy(self):
        for fk in self.surfaces.faces():
            st = self.surfaces.face_attribute(fk, 'surface_type')
            if st == 'Floor':
                return self.surfaces.face_centroid(fk)

    @property
    def data(self):
        data = {'name'                  : self.name,
                'surfaces'              : self.surfaces.to_data(),
                }
        return data
    
    @data.setter
    def data(self, data):
        surfaces = data.get('surfaces') or {}
        self.name               = data.get('name') or {}
        self.surfaces      = ZoneSurfaces.from_data(surfaces)
        self.surfaces.name = self.name

    def add_surfaces(self, mesh):
        """
        Adds surfaces to the zone from a compas mesh

        Parameters
        ----------
        mesh: object
            Compas mesh to add to the zone
        Returns
        -------
        None

        """
        self.surfaces = ZoneSurfaces.from_data(mesh.data)
        self.surfaces.assign_zone_surface_attributes(self.name)

    @classmethod
    def from_data(cls, data):
        """
        Create a new instance of the zone datastructure from a data dictionary.

        Parameters
        ----------
        data: dict
            Data dictionary
        
        Returns
        -------
        Zone
            The instance of the zone datastructure
        
        """
        zone = cls()
        zone.data = data
        return zone

    @classmethod
    def from_json(cls, filepath):
        """
        Create a new instance of the zone datastructure from a JSON file

        Parameters
        ----------
        filepath: str
            Path to the JSON file
        
        Returns
        -------
        Zone
            The instance of the zone datastructure
        
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        zone = cls()
        zone.data = data
        return zone

    @classmethod
    def from_mesh(cls, mesh, name):
        """
        Create a new instance of the zone datastructure from a compas mesh.
        Mesh faces must be provided in the following order: 1 - Floor face, 
        2 - Ceiling face, 3 to n - Wall faces.

        Parameters
        ----------
        mesh: object
            Mesh to create the zone
        name: str, optional
            The name of the zone
        
        Returns
        -------
        Zone
            The instance of the zone datastructure
        
        """
        zone = cls()
        zone.name = name
        zone.add_surfaces(mesh)
        return zone




class ZoneSurfaces(Mesh):
    def __init__(self):
        """
        Custom mesh object for the zone surfaces. Assigns face attributes
        representing surface constructions, and boundary conditions. 

        """
        super().__init__()
        self.default_face_attributes.update({'name': None,
                                             'construction':None,
                                             'surface_type': None,
                                             'outside_boundary_condition': None,
                                             'outside_boundary_condition_object': None,
                                             })
    
    def __str__(self):
        return 'pod_lca Zone Surfaces - {}'.format(self.name)

    def assign_zone_surface_attributes(self, zname):
    #     """
    #     Assigns basic and pre-defined surface attributes based on mesh face order. 

    #     Parameters
    #     ----------
    #     None

    #     Returns
    #     -------
    #     None
        
    #     """

        self.set_face_attribute(0, 'name', '{}_floor'.format(zname))
        self.set_face_attribute(0, 'surface_type', 'Floor')

        self.set_face_attribute(1, 'name', '{}_ceiling'.format(zname))
        self.set_face_attribute(1, 'surface_type', 'Roof')

        for i in range(2, self.number_of_faces()):
            self.set_face_attribute(i, 'name', '{}_wall_{}'.format(zname, i))
            self.set_face_attribute(i, 'surface_type', 'Wall')


if __name__ == '__main__':
    for i in range(50): print('')
    for i in range(50): print('')

    w = 10
    l = 20
    h = 10

    v0 = [0, 0, 0]
    v1 = [w, 0, 0]
    v2 = [w, l, 0]
    v3 = [0 ,l, 0]
    v4 = [0, 0, h]
    v5 = [w, 0, h]
    v6 = [w, l, h]
    v7 = [0 ,l, h]

    f0 = [0, 3, 2, 1]
    f1 = [4, 5, 6, 7]
    f2 = [0, 1, 5, 4]
    f3 = [1, 2, 6, 5]
    f4 = [2, 3, 7, 6]
    f5 = [0, 4, 7, 3]

    vertices = [v0, v1, v2, v3, v4, v5, v6, v7]
    faces = [f0, f1, f2, f3, f4, f5]

    mesh = ZoneSurfaces.from_vertices_and_faces(vertices, faces)
    print(mesh.face_attributes[0])
