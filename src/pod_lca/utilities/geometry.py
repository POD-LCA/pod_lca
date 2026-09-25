from math import sqrt
from math import fabs


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


def intersection_line_line_xy(l1, l2, tol=None):

    a, b = l1
    c, d = l2

    x1, y1 = a[0], a[1]
    x2, y2 = b[0], b[1]
    x3, y3 = c[0], c[1]
    x4, y4 = d[0], d[1]

    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4
    x = (a * (x3 - x4) - (x1 - x2) * b) / d
    y = (a * (y3 - y4) - (y1 - y2) * b) / d

    return [x, y, 0.0]


def midpoint_point_point(a, b):
    return [0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]), 0.5 * (a[2] + b[2])]


def normal_polygon(polygon, unitized=True):
    p = len(polygon)

    if p < 3:
        raise ValueError("At least three points required.")

    nx = 0
    ny = 0
    nz = 0

    o = centroid(polygon)
    a = polygon[-1]
    oa = subtract_vectors(a, o)

    for i in range(p):
        b = polygon[i]
        ob = subtract_vectors(b, o)
        n = cross_vectors(oa, ob)
        oa = ob

        nx += n[0] * 0.5
        ny += n[1] * 0.5
        nz += n[2] * 0.5

    if not unitized:
        return [nx, ny, nz]

    return normalize_vector([nx, ny, nz])


def cross_vectors(u, v):
    return [
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    ]


def area_polygon(polygon):
    from ..units import Quantity

    o = centroid(polygon)
    a = polygon[-1]
    b = polygon[0]
    oa = subtract_vectors(a, o)
    ob = subtract_vectors(b, o)
    n0 = cross_vectors(oa, ob)
    area = 0.5 * length_vector(n0)
    for i in range(0, len(polygon) - 1):
        oa = ob
        b = polygon[i + 1]
        ob = subtract_vectors(b, o)
        n = cross_vectors(oa, ob)
        if dot_vectors(n, n0) > 0:
            area += 0.5 * length_vector(n)
        else:
            area -= 0.5 * length_vector(n)
    area = abs(area)
    x = polygon[0][0]
    if isinstance(x, Quantity):
        return Quantity(area, x.unit * x.unit)
    else:
        return area


def dot_vectors(u, v):
    return sum(a * b for a, b in zip(u, v))


def distance_point_plane_signed(point, plane):
    base, normal = plane
    vector = subtract_vectors(point, base)
    return dot_vectors(vector, normal)


def distance_point_plane(point, plane):
    return fabs(distance_point_plane_signed(point, plane))


def is_point_on_plane(point, plane, tol=None):
    return distance_point_plane(point, plane) < 0.001


def distance_point_point(a, b):
    ab = subtract_vectors(b, a)
    return length_vector(ab)


def length_vector_sqrd(vector):
    return vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2


def length_vector(vector):
    return sqrt(length_vector_sqrd(vector))


def normalize_vector(vector, unitless=False):
    length = length_vector(vector)
    if not length:
        return vector
    if unitless:
        return [(vector[0] / length).value, (vector[1] / length).value, (vector[2] / length).value]
    else:
        return [vector[0] / length, vector[1] / length, vector[2] / length]


def scale_vector(vector, factor):
    return [axis * factor for axis in vector]


def add_vectors(u, v):
    return [a + b for (a, b) in zip(u, v)]


def subtract_vectors(u, v):
    return [a - b for (a, b) in zip(u, v)]


def centroid(points):
    p = len(points)
    x, y, z = zip(*points)
    return [sum(x) / p, sum(y) / p, sum(z) / p]


def geometric_key(xyz, precision=3, sanitize=True):
    x, y, z = xyz
    if precision == 0:
        raise ValueError("Precision cannot be zero.")

    if precision == -1:
        return "{:d},{:d},{:d}".format(int(x), int(y), int(z))

    if precision < -1:
        precision = -precision - 1
        factor = 10**precision
        return "{:d},{:d},{:d}".format(
            int(round(x / factor) * factor),
            int(round(y / factor) * factor),
            int(round(z / factor) * factor),
        )

    if sanitize:
        minzero = "-{0:.{1}f}".format(0.0, precision)
        if "{0:.{1}f}".format(x, precision) == minzero:
            x = 0.0
        if "{0:.{1}f}".format(y, precision) == minzero:
            y = 0.0
        if "{0:.{1}f}".format(z, precision) == minzero:
            z = 0.0

    return "{0:.{3}f},{1:.{3}f},{2:.{3}f}".format(x, y, z, precision)


def make_box(w, l, h, spt=[0, 0, 0]):
    p0 = [spt[0], spt[1], spt[2]]
    p1 = [spt[0] + w, spt[1], spt[2]]
    p2 = [spt[0] + w, spt[1] + l, spt[2]]
    p3 = [spt[0], spt[1] + l, spt[2]]
    p4 = [spt[0], spt[1], spt[2] + h]
    p5 = [spt[0] + w, spt[1], spt[2] + h]
    p6 = [spt[0] + w, spt[1] + l, spt[2] + h]
    p7 = [spt[0], spt[1] + l, spt[2] + h]

    f0 = [0, 3, 2, 1]
    f1 = [4, 5, 6, 7]
    f2 = [0, 1, 5, 4]
    f3 = [1, 2, 6, 5]
    f4 = [2, 3, 7, 6]
    f5 = [3, 0, 4, 7]

    vertices = [p0, p1, p2, p3, p4, p5, p6, p7]
    faces = [f0, f1, f2, f3, f4, f5]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    return mesh


def make_box_from_quad(quad, height):

    f0 = [0, 3, 2, 1]
    f1 = [4, 5, 6, 7]
    f2 = [0, 1, 5, 4]
    f3 = [1, 2, 6, 5]
    f4 = [2, 3, 7, 6]
    f5 = [3, 0, 4, 7]

    quad_ = [[p[0], p[1], p[2] + height] for p in quad]
    quad.extend(quad_)
    faces = [f0, f1, f2, f3, f4, f5]

    mesh = Mesh.from_vertices_and_faces(quad, faces)
    return mesh


class Mesh(object):

    def __init__(self):
        self.vertices = {}
        self.faces = {}
        self.face_attributes = {}
        self.default_face_attributes = {}

    @classmethod
    def from_surfaces(cls, surfaces):
        all_vertices = []
        for sk in surfaces:
            all_vertices.extend(surfaces[sk].polygon)
        gk_dict = {geometric_key(v): v for v in all_vertices}
        vertices = [gk_dict[k] for k in gk_dict]
        gk_dict = {geometric_key(v): i for i, v in enumerate(vertices)}
        faces = []
        for srf in surfaces:
            face = [gk_dict[geometric_key(v)] for v in surfaces[srf].polygon]
            faces.append(face)
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    @classmethod
    def from_vertices_and_faces(cls, vertices, faces):
        mesh = cls()
        mesh.vertices = {i: {"x": v[0], "y": v[1], "z": v[2]} for i, v in enumerate(vertices)}
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
        data = {
            "vertices": self.vertices,
            "faces": self.faces,
            "default_face_attributes": self.default_face_attributes,
        }
        return data

    @data.setter
    def data(self, data):
        self.vertices = data.get("vertices") or {}
        self.faces = data.get("faces") or {}
        self.default_face_attributes = data.get("default_face_attributes") or {}

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
            self.face_attributes[key][attr] = self.default_face_attributes[attr]

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
        return self.vertices[key]["x"], self.vertices[key]["y"], self.vertices[key]["z"]

    def vertex_xyz_unitless(self, key):
        from ..units import Quantity
        if isinstance(self.vertices[key]['x'], Quantity):
            return self.vertices[key]["x"].value, self.vertices[key]["y"].value, self.vertices[key]["z"].value
        else:
            return self.vertex_xyz(key)


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

