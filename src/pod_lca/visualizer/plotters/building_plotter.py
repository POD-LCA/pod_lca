import plotly
import plotly.graph_objects as go
import plotly.express as px

from pod_lca.utilities.geometry import Mesh


def plot_building(building):
    fks = building.floors
    data = []
    for i, fk in enumerate(fks):
        floor = building.floors[fk]
        add_floor(data, floor, i)

    layout = make_layout()
    fig = go.Figure(data=data, layout=layout)
    fig.show()

def add_floor(data, floor, key):

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
    
    #############################################################################
    # TODO: triangulate faces?
    # This assumes all faces are quads, some floors , cielings will not be
    triangles = []
    for face in faces:
        triangles.append(face[:3])
        if len(face) == 4:
            triangles.append([face[2], face[3], face[0]])
    #############################################################################

    i = [v[0] for v in triangles]
    j = [v[1] for v in triangles]
    k = [v[2] for v in triangles]

    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = [v[2] for v in vertices]


    # colorscales = dir(plotly.colors.sequential)[::2]
    colors = plotly.colors.qualitative.Pastel
    # attrs = ['name', 'surface_type', 'outside_boundary_condition', 'construction']
    text = []
    # intensity = []
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
        text.append(string)
        # intensity.append(key)
        text.append(string)
        # intensity.append(key)

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
                    #    intensitymode='cell',
                    #    intensity=intensity,
                       showscale=False,
                    #    colorscale=colorscales[0],
                    color = colors[key]
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