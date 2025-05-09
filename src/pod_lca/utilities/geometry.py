from math import sqrt
from math import fabs


__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"



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
    return abs(area)


def dot_vectors(u, v):
    return sum(a * b for a, b in zip(u, v))


def distance_point_plane_signed(point, plane):
    base, normal = plane
    vector = subtract_vectors(point, base)
    return dot_vectors(vector, normal)


def distance_point_plane(point, plane):
    return fabs(distance_point_plane_signed(point, plane))


def is_point_on_plane(point, plane, tol=None):
    return distance_point_plane(point, plane) < .001


def distance_point_point(a, b):
    ab = subtract_vectors(b, a)
    return length_vector(ab)


def length_vector_sqrd(vector):
    return vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2


def length_vector(vector):
    return sqrt(length_vector_sqrd(vector))


def normalize_vector(vector):
    length = length_vector(vector)
    if not length:
        return vector
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