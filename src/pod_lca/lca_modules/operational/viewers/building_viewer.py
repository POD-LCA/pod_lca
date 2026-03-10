from __future__ import print_function

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Tomas Mendez Echenagucia - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"

import plotly
import plotly.graph_objects as go

from pod_lca.utilities.geometry import Mesh
from pod_lca.utilities.geometry import centroid


class BuildingViewer(object):
    """
    Viewer object for Building objects. Can show zone geometries, windows,
    shading devicesconstruction layers.

    Parameters
    ----------
    building: object
        The building object to be displayed
    data: list
        Plotly data containing plot objects (i.e. Meshes)
    layout: dict
        PLotly layout data

    """

    def __init__(self, building):
        self.building = building
        self.data = []
        self.layout = None
        self.fig = None

    def make_layout(self):
        """
        Adds the layout data to the viewer object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        name = self.building.name
        title = "{0}".format(name)
        layout = go.Layout(
            title=title,
            scene=dict(
                aspectmode="data",
                xaxis=dict(
                    gridcolor="rgb(255, 255, 255)",
                    zerolinecolor="rgb(255, 255, 255)",
                    showbackground=True,
                    backgroundcolor="rgb(230, 230,230)",
                ),
                yaxis=dict(
                    gridcolor="rgb(255, 255, 255)",
                    zerolinecolor="rgb(255, 255, 255)",
                    showbackground=True,
                    backgroundcolor="rgb(230, 230,230)",
                ),
                zaxis=dict(
                    gridcolor="rgb(255, 255, 255)",
                    zerolinecolor="rgb(255, 255, 255)",
                    showbackground=True,
                    backgroundcolor="rgb(230, 230,230)",
                ),
            ),
            showlegend=True,
        )
        self.layout = layout

    def show(self):
        """
        Displays the buiilding in a browser window.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self.make_layout()
        self.add_envelopes()
        # self.add_windows()
        # self.add_shadings()
        # self.add_north()

        self.fig = go.Figure(data=self.data, layout=self.layout)
        self.fig.show()

    def add_envelopes(self):
        be = self.building.building_envelope
        for ek in be.envelopes:
            env = be.envelopes[ek]
            self.add_envelope_mesh(env, ek)

    def add_windows(self):
        """
        Adds window data to the viewer object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        for wk in self.building.windows:
            self.add_window_mesh(wk)

    def add_shadings(self):
        """
        Adds shading data to the viewer object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        for sk in self.building.shadings:
            self.add_shading_mesh(sk)

    def add_shading_mesh(self, key):
        """
        Adds shading mesh data to the viewer object.

        Parameters
        ----------
        key: int
            The shading key to be added

        Returns
        -------
        None

        """
        mesh = self.building.shadings[key].mesh
        vertices, faces = mesh.to_vertices_and_faces()
        edges = [[mesh.vertex_xyz(u), mesh.vertex_xyz(v)] for u, v in mesh.edges()]
        line_marker = dict(color="rgb(0,0,0)", width=1.5)
        lines = []
        x, y, z = [], [], []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        sname = self.building.shadings[key].name
        lines = [
            go.Scatter3d(
                name=f"{sname}",
                x=x,
                y=y,
                z=z,
                mode="lines",
                line=line_marker,
                legendgroup=f"{sname}",
            )
        ]
        triangles = []
        for face in faces:
            triangles.append(face[:3])
            if len(face) == 4:
                triangles.append([face[2], face[3], face[0]])

        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]

        text = []
        intensity = []

        faces = [
            go.Mesh3d(
                name="Zone",
                x=x,
                y=y,
                z=z,
                i=i,
                j=j,
                k=k,
                color="rgb(255,255,255)",
                opacity=0.8,
                #    colorbar_title='is_rad',
                #    colorbar_thickness=10,
                #    text=text,
                #    hoverinfo='text',
                legendgroup=f"{sname}",
                lighting={"ambient": 1.0},
                #    intensitymode='cell',
                #    intensity=intensity,
                #    showscale=False,
                #    colorscale='gnbu',
            )
        ]
        self.data.extend(lines)
        self.data.extend(faces)

    def add_window_mesh(self, key):
        """
        Adds window mesh data to the viewer object.

        Parameters
        ----------
        key: int
            The window key to be added

        Returns
        -------
        None

        """
        vertices = self.building.windows[key].nodes
        faces = [[0, 1, 2, 3]]
        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        vertices, faces = mesh.to_vertices_and_faces()
        edges = [[mesh.vertex_xyz(u), mesh.vertex_xyz(v)] for u, v in mesh.edges()]
        line_marker = dict(color="rgb(0,0,0)", width=1.5)
        lines = []
        x, y, z = [], [], []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        wname = self.building.windows[key].name
        lines = [
            go.Scatter3d(
                name=f"{wname}",
                x=x,
                y=y,
                z=z,
                mode="lines",
                line=line_marker,
                legendgroup=f"{wname}",
            )
        ]
        triangles = []
        for face in faces:
            triangles.append(face[:3])
            if len(face) == 4:
                triangles.append([face[2], face[3], face[0]])

        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]

        text = []
        intensity = []
        for fk in mesh.faces:
            ck = self.building.windows[key].construction
            if ck in self.building.construction_key_dict:
                con = self.building.constructions[self.building.construction_key_dict[ck]]
                layers = [con.layers[lk]["name"] for lk in con.layers]
                # thick = con.layers[lk]['thickness']
                # layers = ['{} {}mm'.format(lay, round(thick*1000, 1)) for lay in layers]
            else:
                layers = []

            string = "name: {}<br>".format(wname)
            string += "construction: {}<br>".format(ck)
            for lk, layer in enumerate(layers):
                string += "layer {}: {}<br>".format(lk, layer)
            text.append(string)
            intensity.append(float(key))
            if len(mesh.face_vertices(fk)) == 4:
                intensity.append(float(key))
                text.append(string)

        faces = [
            go.Mesh3d(
                name="Zone",
                x=x,
                y=y,
                z=z,
                i=i,
                j=j,
                k=k,
                opacity=0.8,
                colorbar_title="is_rad",
                colorbar_thickness=10,
                text=text,
                hoverinfo="text",
                legendgroup=f"{wname}",
                lighting={"ambient": 1.0},
                intensitymode="cell",
                intensity=intensity,
                showscale=False,
                colorscale="gnbu",
            )
        ]
        self.data.extend(lines)
        self.data.extend(faces)

    def add_envelope_mesh(self, env, key):
        mesh = Mesh.from_surfaces(env.surfaces)
        vertices, faces = mesh.to_vertices_and_faces()
        # vertices = [[v[0].value, v[1].value, v[2].value] for v in vertices]
        edges = [[mesh.vertex_xyz_unitless(u), mesh.vertex_xyz_unitless(v)] for u, v in mesh.edges()]

        line_marker = dict(color="rgb(0,0,0)", width=1.5)
        lines = []
        x, y, z = [], [], []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        zname = 'envelope {}'.format(key)
        lines = [
            go.Scatter3d(
                name=f"{zname}",
                x=x,
                y=y,
                z=z,
                mode="lines",
                line=line_marker,
                legendgroup=f"{zname}",
            )
        ]
        triangles = []
        for face in faces:
            if len(face) == 3:
                triangles.append(face[:3])
            elif len(face) == 4:
                triangles.append(face[:3])
                triangles.append([face[2], face[3], face[0]])
            elif len(face) > 4:
                pts = [vertices[vk] for vk in face]
                cpt = centroid(pts)
                cpti = len(vertices)
                vertices.append(cpt)
                for i in range(len(face)):
                    triangles.append([cpti, face[-i], face[-i-1]])

        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]

        # colorscales = ['sunset', 'viridis', 'amp']

        colorscales = dir(plotly.colors.sequential)[::2]
        attrs = ["name", "surface_type", "outside_boundary_condition", "construction"]
        text = []
        intensity = []
        for fk in mesh.faces:
            # faceatts = mesh.face_attributes[fk]
            ck = mesh.get_face_attribute(fk, "construction")
            if ck:
                con = self.building.constructions[self.building.construction_key_dict[ck]]
                layers = [con.layers[lk]["name"] for lk in con.layers]
                thick = [con.layers[lk]["thickness"] for lk in con.layers]
                layers = ["{} {}mm".format(lay, round(thick[tk] * 1000, 1)) for tk, lay in enumerate(layers)]
            else:
                layers = []
            string = "zone: {}<br>".format(zname)
            # for att in attrs:
            #     string += "{}: {}<br>".format(att, faceatts[att])
            for lk, layer in enumerate(layers):
                string += "layer {}: {}<br>".format(lk, layer)
            text.append(string)
            intensity.append(float(key))
            if len(mesh.face_vertices(fk)) == 4:
                intensity.append(float(key))
                text.append(string)

        faces = [
            go.Mesh3d(
                name="Zone",
                x=x,
                y=y,
                z=z,
                i=i,
                j=j,
                k=k,
                opacity=0.8,
                colorbar_title="is_rad",
                colorbar_thickness=10,
                # text=text,
                # hoverinfo="text",
                legendgroup=f"{zname}",
                lighting={"ambient": 1.0},
                intensitymode="cell",
                intensity=intensity,
                showscale=False,
                colorscale=colorscales[int(key)],
            )
        ]
        self.data.extend(lines)
        self.data.extend(faces)

    def find_npt(self):
        x = []
        y = []
        z = []
        for zk in self.building.zones:
            vs = list(self.building.zones[zk].surfaces.vertices)
            x_ = [self.building.zones[zk].surfaces.vertex_xyz(v)[0] for v in vs]
            y_ = [self.building.zones[zk].surfaces.vertex_xyz(v)[1] for v in vs]
            z_ = [self.building.zones[zk].surfaces.vertex_xyz(v)[2] for v in vs]
            x.extend(x_)
            y.extend(y_)
            z.extend(z_)

        return [min(x) - 2, min(y) - 2, min(z)]

    def add_north(self):

        x, y, z = self.find_npt()

        north = go.Scatter3d(
            x=[x, x - 0.5, x + 0.5, x],
            y=[y + 3, y + 0.5, y + 0.5, y + 3],
            z=[z, z, z, z],
            mode="lines+text",
            text=["North", "", "", "", ""],
            name="North",
            marker={"color": "red"},
        )
        self.data.extend([north])


if __name__ == "__main__":
    import os
    import compas_eplus
    from compas_eplus.building import Building

    for i in range(50):
        print("")

    file = "teresa_example.idf"
    filepath = os.path.join(compas_eplus.DATA, "idf_examples", file)
    path = compas_eplus.TEMP
    wea = compas_eplus.SEATTLE
    b = Building.from_idf(filepath, path, wea)

    v = BuildingViewer(b)
    v.show()
