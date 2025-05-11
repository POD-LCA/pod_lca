__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"

from pod_lca.utilities.geometry import centroid
from pod_lca.utilities.geometry import normal_polygon
from pod_lca.utilities.geometry import area_polygon

class Mesh(object):

    def __init__(self):
        self.vertices   = {}
        self.faces      = {}
        self.face_attributes = {}
        self.default_face_attributes = {}

    @classmethod
    def from_vertices_and_faces(cls, vertices, faces):
        mesh = cls()
        mesh.vertices = {i: {'x': v[0], 'y': v[1], 'z':v[2]} for i, v in enumerate(vertices)}
        # mesh.faces = {i: v for i, v in enumerate(faces)}
        for face in faces:
            mesh.add_face(face)
        return mesh

    @classmethod
    def from_data(cls, data):
        mesh = cls()
        mesh.data = data
        return mesh

    @property
    def data(self):
        data = {'vertices': self.vertices,
                'faces': self.faces,
                'default_face_attributes': self.default_face_attributes,
                }
        return data

    @data.setter
    def data(self, data):
        self.vertices                   = data.get('vertices') or {}
        self.faces                      = data.get('faces') or {}
        self.default_face_attributes    = data.get('default_face_attributes') or {}

    def edges(self):
        edges = []
        for fk in self.faces:
            vks = self.face_vertices(fk)
            for i in range(len(vks)):
                if i < len(vks) - 1:
                    edge = vks[i], vks[i + 1]
                else:
                    edge = vks[i], vks[0]
                if edge not in edges and (edge[1], edge[0] not in edges):
                    edges.append(edge)
        return edges


    def to_vertices_and_faces(self):
        vertices = [self.vertex_xyz(vk) for vk in sorted(self.vertices.keys())]
        faces = [self.face_vertices(fk) for fk in sorted(self.faces.keys())]
        return vertices, faces

    def add_face(self, face):
        key = self.number_of_faces()
        self.faces[key] = face
        self.face_attributes[key] = {}
        for attr in self.default_face_attributes:
            self.face_attributes[key][attr] =  self.default_face_attributes[attr]

    def set_face_attribute(self, key, attr, value):
        if key in self.face_attributes:
            self.face_attributes[key].update({attr: value})
        else:
            self.face_attributes[key] = {attr: value}

    def get_face_attribute(self, key, attr):
        if attr in self.face_attributes[key]:
            return self.face_attributes[key][attr]
        return None

    def number_of_faces(self):
        return len(self.faces)

    def face_vertices(self, key):
        return self.faces[key]

    def vertex_xyz(self, key):
        return self.vertices[key]['x'], self.vertices[key]['y'], self.vertices[key]['z']

    def face_centroid(self, key):
        points = [self.vertex_xyz(vk) for vk in self.face_vertices(key)]
        return centroid(points)

    def face_normal(self, key, unitized=True):
        return normal_polygon(self.face_coordinates(key), unitized=unitized)

    def face_coordinates(self, key):
        return [self.vertex_xyz(vk) for vk in self.faces[key]]

    def face_area(self, key):
        return area_polygon(self.face_coordinates(key))

    def face_keys(self):
        return self.faces.keys()

if __name__ == '__main__':
    
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

    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    print(mesh.face_vertices(0))
    print(mesh.vertex_xyz(3))
    print(mesh.face_centroid(1))

    