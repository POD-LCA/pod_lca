__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"



def plot_building(building):
    import rhinoscriptsyntax as rs

    rs.CurrentLayer('Default')
    layers = ['floor', 'ceiling', 'wall', 'window']
    for layer in layers:
        if not rs.IsLayer(layer):
            rs.LayerCreate(layer
                           )
    rs.DeleteObjects(rs.ObjectsByLayer('Default'))
    rs.DeleteObjects(rs.ObjectsByLayer('floor'))
    rs.DeleteObjects(rs.ObjectsByLayer('ceiling'))
    rs.DeleteObjects(rs.ObjectsByLayer('wall'))
    rs.DeleteObjects(rs.ObjectsByLayer('window'))

    for i in building.building_envelope.envelopes:
        env = building.building_envelope.envelopes[i]

        floor = env.surfaces['floor'].polygon
        floor.append(floor[0])
        rs.CurrentLayer('floor')
        pl = rs.AddPolyline(floor)
        srf = rs.AddPlanarSrf(pl)

        rs.CurrentLayer('ceiling')
        ceiling = env.surfaces['ceiling'].polygon
        ceiling.append(ceiling[0])
        pl = rs.AddPolyline(ceiling)
        srf = rs.AddPlanarSrf(pl)

        rs.CurrentLayer('wall')
        for i in range(6):
            wall_1 = env.surfaces['wall_{}'.format(i)].polygon
            wall_1.append(wall_1[0])
            pl = rs.AddPolyline(wall_1)
            srf = rs.AddPlanarSrf(pl)

        rs.CurrentLayer('window')
        for wk in env.windows:
            win = env.windows[wk]
            sk = list(win.surfaces.keys())[0]
            win = win.surfaces[sk].polygon
            win.append(win[0])
            pl = rs.AddPolyline(win)
            srf = rs.AddPlanarSrf(pl)

    rs.CurrentLayer('Default')