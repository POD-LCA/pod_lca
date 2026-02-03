__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


from pod_lca.lca_modules.building_envelope.construction import Construction


class Window(Construction):
    def __init__(self):
        super().__init__()
        self.__type__ = 'Window'
        self.wall_key = None # the wall this window is related to

    def update_wall(self, envelope):
        # TODO: Create a function that updates the wall area / quantities the window is attached to. 
        pass

    @classmethod
    def from_wall_wwr_and_idf(cls):
        pass
        if wwr > .95:
            wwr = .95
        pts = envelope.surfaces[wall_key].polygon
        cpt = centroid(pts)
        area = envelope.surfaces[wall_key].area * wwr
        lx = distance_point_point(pts[0], pts[1]) - .1
        ly = area / lx
        vx = scale_vector(normalize_vector(subtract_vectors(pts[0], pts[1])), lx / 2.)
        vy = scale_vector(normalize_vector(subtract_vectors(pts[0], pts[-1])), ly / 2.)
        vx_ = scale_vector(normalize_vector(subtract_vectors(pts[0], pts[1])), -lx / 2.)
        vy_ = scale_vector(normalize_vector(subtract_vectors(pts[0], pts[-1])), -ly / 2.)

        p0 = add_vectors(cpt, add_vectors(vx_, vy_))
        p1 = add_vectors(cpt, add_vectors(vx, vy_))
        p2 = add_vectors(cpt, add_vectors(vx, vy))
        p3 = add_vectors(cpt, add_vectors(vx_, vy))

        sk = 'window_{}'.format(wall_key)
        surface = Surface.from_polygon(sk, [p0, p1, p2, p3])
        envelope.surfaces[sk] = surface
        envelope.window_surface_keys.append(sk)
        construction = Construction.from_idf(construction_name, path, building, envelope, 'window', window_service_life)


        window = cls()
        window.name = f'win_{envelope.name}_{wall_key}'
        window.building_surface = f'{envelope.name}_wall_{wall_key}' 
        window.construction = construction
        return window
    
    # def to_json(self, filepath):
    #     """
    #     Serialize the data representation of the window to a JSON file

    #     Parameters
    #     ----------
    #     filepath: str
    #         Path for the JSON file to be created
        
    #     Returns
    #     -------
    #     None

    #     """
    #     with open(filepath, 'w+') as fp:
    #         json.dump(self.data, fp)

    # @property
    # def data(self):
    #     data = {'name'                  : self.name,
    #             'nodes'                 : self.nodes,
    #             'building_surface'      : self.building_surface,
    #             'construction'          : self.construction,
    #             }
    #     return data
    

    # @data.setter
    # def data(self, data):
    #     self.name               = data.get('name') or {}
    #     self.nodes              = data.get('nodes') or {}
    #     self.building_surface   = data.get('building_surface') or {}
    #     self.construction       = data.get('construction') or {}

    # @classmethod
    # def from_data(cls, data):
    #     """
    #     Create a new instance of the window datastructure from a data dictionary.

    #     Parameters
    #     ----------
    #     data: dict
    #         Data dictionary
        
    #     Returns
    #     -------
    #     Window
    #         The instance of the window datastructure
        
    #     """
    #     window = cls()
    #     window.data = data
    #     return window


    # @classmethod
    # def from_json(cls, filepath):
    #     """
    #     Create a new instance of the window datastructure from a JSON file

    #     Parameters
    #     ----------
    #     filepath: str
    #         Path to the JSON file
        
    #     Returns
    #     -------
    #     Window
    #         The instance of the window datastructure
        
    #     """
    #     with open(filepath, 'r') as fp:
    #         data = json.load(fp)
    #     window = cls()
    #     window.data = data
    #     return window

    # @classmethod
    # def from_points_and_zone(cls, points, zone):
    #     cpt = centroid(points)
    #     mesh = zone.surfaces
    #     for fk in mesh.faces:
    #         # pl = [mesh.vertex_coordinates(vk) for vk in mesh.face_vertices(fk)]
    #         normal = mesh.face_normal(fk)
    #         fcpt = mesh.face_centroid(fk)
    #         check = is_point_on_plane(cpt, [fcpt, normal])
    #         if check:
    #             wall_key = fk
    #             break

        
    #     window = cls()
    #     window.name = 'win_{}_{}'.format(zone.name, wall_key)
    #     window.nodes = points
    #     window.building_surface = '{}_wall_{}'.format(zone.name, wall_key) 
    #     window.construction = None
    #     return window

if __name__ == '__main__':
    pass