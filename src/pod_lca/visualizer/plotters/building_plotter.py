import plotly
import plotly.graph_objects as go
import plotly.express as px

from pod_lca.utilities.geometry import Mesh
from pod_lca.utilities.geometry import centroid


def plot_building(building):
    fks = building.floors
    data = []
    for i, fk in enumerate(fks):
        floor = building.floors[fk]
        add_floor(data, building, floor)

    add_ground(building, data)

    layout = make_layout()
    fig = go.Figure(data=data, layout=layout)
    fig.show()


def add_ground(building, data):
    for fk in building.floors:
        if building.floors[fk].is_below_grade:
            pl = building.floors[fk].envelope.surfaces['floor'].polygon
            fz = pl[0][2]
            break

    
    minx = min([pt[0] for pt in pl])
    miny = min([pt[1] for pt in pl])
    maxx = max([pt[0] for pt in pl])
    maxy = max([pt[1] for pt in pl])

    x_ = (maxx - minx) * .4
    y_ = (maxy - miny) * .4
    
    vertices = [[minx - x_, miny - y_, fz],
                [maxx + x_, miny - y_, fz],
                [maxx + x_, maxy + y_, fz],
                [minx - x_, maxy + y_, fz],
                ]
    triangles = [[0,1,2], [2,3,0]]

    i = [v[0] for v in triangles]
    j = [v[1] for v in triangles]
    k = [v[2] for v in triangles]

    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = [v[2] for v in vertices]

    intensity = [None, None]
    text = ['Ground', 'Ground']
    faces = [go.Mesh3d(name='Ground',
                       x=x,
                       y=y,
                       z=z,
                       i=i,
                       j=j,
                       k=k,
                       opacity=.8,
                       text=text,
                       legendgroup='ground',
                       showscale=False,
                       lighting={'ambient':1.0},
                       color = 'black',
                       intensitymode='cell',
                       intensity=intensity,
            )]
    data.extend(faces)


def add_floor(data, building, floor):

    env = floor.envelope
    srfs = env.surfaces
    mesh =  Mesh.from_surfaces(srfs)

    vertices, faces = mesh.to_vertices_and_faces()
    edges = [[mesh.vertex_xyz(u), mesh.vertex_xyz(v)] for u,v in mesh.edges()]
    line_marker = dict(color='rgb(0,0,0)', width=1.5)
    lines = []
    x, y, z = [], [],  []
    for u, v in edges:
        x.extend([u[0], v[0], [None]])
        y.extend([u[1], v[1], [None]])
        z.extend([u[2], v[2], [None]])

    zname = 'floor_{}'.format(floor.floor_no)
    lines = [go.Scatter3d(name=f'{zname}',
                          x=x,
                          y=y,
                          z=z,
                          mode='lines',
                          line=line_marker,
                          legendgroup=f'{zname}',
                          )]
    

    triangles = []
    for face in faces:
        if len(face) == 3:
            triangles.append(face[:3])
        elif len(face) == 4:
            triangles.append(face[:3])
            triangles.append([face[2], face[3], face[0]])
        else:
            pass
            f_xyz = [mesh.vertex_xyz(fk) for fk in face]
            cpt = centroid(f_xyz)
            vertices.append(cpt)
            for fi in range(len(face)):
                triangles.append([len(vertices)-1, face[-fi], face[-fi - 1]])

    i = [v[0] for v in triangles]
    j = [v[1] for v in triangles]
    k = [v[2] for v in triangles]

    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = [v[2] for v in vertices]


    # colors = plotly.colors.qualitative.Pastel
    text = []
    intensity = []
    for sk in srfs:
        con = env.constructions[sk]
        layers = con.layers
        layers = [con.layers[lk].name for lk in con.layers] 
        thick = [con.layers[lk].thickness for lk in con.layers]
        layers = ['{} {}mm'.format(lay, round(thick[tk]*1000, 1)) for tk, lay in enumerate(layers)]
        string = 'Zone: {}<br>'.format(zname)
        string += 'Name: {}<br>'.format(con.name)
        string += 'Surface Type: {}<br>'.format(srfs[sk].name)
        # string += 'Outside Boundary Consition: {}<br>'.format(srfs[sk].outside_boundary_condition)
        string += 'Construction: {}<br>'.format(con.name)
        for lk, layer in enumerate(layers):
            string += 'layer {}: {}<br>'.format(lk, layer)
        if len(srfs[sk].polygon) == 3:
            num_strings = 1
        elif len(srfs[sk].polygon) == 4:
            num_strings = 2
        else:
            num_strings = len(srfs[sk].polygon)
        for _ in range(num_strings):
            text.append(string)
            intensity.append(floor.floor_no)

    faces = [go.Mesh3d(name='Zone',
                       x=x,
                       y=y,
                       z=z,
                       i=i,
                       j=j,
                       k=k,
                       opacity=.8,
                       colorbar_title='is_rad',
                       colorbar_thickness=10,
                       text = text,
                       hoverinfo='text',
                       legendgroup=f'{zname}',
                       lighting={'ambient':1.0},
                       showscale=False,
                    #    color = colors[key],
                       intensitymode='cell',
                       intensity=intensity,
                       cmin=0,
                       cmax=len(building.floors),
            )]
    data.extend(lines)
    data.extend(faces)


def make_layout():
    """
    Adds the layout data to the viewer object.

    Parameters
    ----------
    None

    Returns
    -------
    None
    
    """
    name = 'Building'
    title = '{0}'.format(name)
    layout = go.Layout(title=title,
                        scene=dict(aspectmode='data',
                                xaxis=dict(
                                            gridcolor='rgb(255, 255, 255)',
                                            zerolinecolor='rgb(255, 255, 255)',
                                            showbackground=True,
                                            backgroundcolor='rgb(230, 230,230)'),
                                yaxis=dict(
                                            gridcolor='rgb(255, 255, 255)',
                                            zerolinecolor='rgb(255, 255, 255)',
                                            showbackground=True,
                                            backgroundcolor='rgb(230, 230,230)'),
                                zaxis=dict(
                                            gridcolor='rgb(255, 255, 255)',
                                            zerolinecolor='rgb(255, 255, 255)',
                                            showbackground=True,
                                            backgroundcolor='rgb(230, 230,230)')
                                ),
                        showlegend=True,
                        )
    return layout