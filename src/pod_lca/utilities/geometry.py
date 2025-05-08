__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


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