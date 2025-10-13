from pod_lca.utilities.geometry import centroid
from pod_lca.utilities.geometry import subtract_vectors
from pod_lca.utilities.geometry import scale_vector
from pod_lca.utilities.geometry import add_vectors
from pod_lca.utilities.geometry import normalize_vector
from pod_lca.utilities.geometry import distance_point_point

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