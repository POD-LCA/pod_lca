from pod_lca.utilities.geometry import centroid
from pod_lca.utilities.geometry import subtract_vectors
from pod_lca.utilities.geometry import scale_vector
from pod_lca.utilities.geometry import add_vectors
from pod_lca.utilities.geometry import normalize_vector
from pod_lca.utilities.geometry import distance_point_point
from pod_lca.utilities.geometry import cross_vectors

from pod_lca.lca_modules.building_envelope.surface import Surface

def window_surfaces_from_wwr(envelope, wall_key, wwr):
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
    return [surface]

def shading_surfaces_from_window(window, top=None, left=None, right=None):
    surface = window.surfaces[0]
    vertices = surface.polygon
    wname = window.name

    v1 = subtract_vectors(vertices[3], vertices[2])
    v2 = subtract_vectors(vertices[3], vertices[0])
    n = normalize_vector(cross_vectors(v2, v1))
    surfaces = []
    if top:
        ntop = scale_vector(n, top)
        a = add_vectors(vertices[0], ntop)
        b = add_vectors(vertices[1], ntop)
        polygon = [vertices[1], vertices[0], a, b]
        shk = '{}_top'.format(wname)
        surfaces.append(Surface.from_polygon(shk, polygon))
    if left:
        nleft = scale_vector(n, left)
        a = add_vectors(vertices[1], nleft)
        b = add_vectors(vertices[2], nleft)
        polygon = [vertices[2], vertices[1], a, b]
        shk = '{}_left'.format(wname)
        surfaces.append(Surface.from_polygon(shk, polygon))
    if right:
        nright = scale_vector(n, right)
        a = add_vectors(vertices[0], nright)
        b = add_vectors(vertices[3], nright)
        polygon = [vertices[3], vertices[0], a, b]
        shk = '{}_right'.format(wname)
        surfaces.append(Surface.from_polygon(shk, polygon))
    return surfaces