import holoviews as hv
from holoviews import dim, opts

hv.extension("matplotlib")
hv.output(fig="svg")

# processors names or UID

nodes = [
    "Tomas concrete",
    "Cement production",
    "Clinker production",
    "Calcareous marl",
    "market for clay",
    "market for lime",
    "market for trasport",
]

nodes = hv.Dataset(enumerate(nodes), "index", "label")

# (processor, to processor, Output)

edges = [(0, 1, 100), (0, 2, 47), (2, 6, 17), (2, 3, 30), (3, 1, 22.5), (3, 4, 3.5), (3, 6, 4.0), (4, 5, 0.45)]

value_dim = hv.Dimension("Percentage", unit="%")
hv.Sankey((edges, nodes), ["From", "To"], vdims=value_dim).opts(
    opts.Sankey(
        cmap="Set1",
        labels="label",
        label_position="right",
        fig_size=300,
        edge_color=dim("To").str(),
        node_color=dim("index").str(),
    )
)


# -------------------------------------------------------------------

import plotly.graph_objects as go

fig = go.Figure(
    data=[
        go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.8),
                label=[
                    "Tomas concrete",
                    "Cement production",
                    "Clinker production",
                    "Calcareous marl",
                    "market for clay",
                    "market for lime",
                    "market for trasport",
                ],
                color="blue",
            ),
            link=dict(
                source=[0, 0, 2, 2, 3, 3, 3, 4],  # indices correspond to labels, eg A1, A2, A1, B1, ...
                target=[1, 2, 6, 3, 1, 4, 6, 5],
                value=[8, 4, 2, 8, 4, 2, 3, 5],
            ),
        )
    ]
)

fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
fig.show()

# -------------------------------------------------------------------

from d3blocks import D3Blocks
import pandas as pd

# Initialize
d3 = D3Blocks(chart="Sankey", frame=True)

# Create a sample dataframe
data = {
    "source": ["A", "A", "B", "C", "D", "D"],
    "target": ["B", "C", "D", "E", "F", "G"],
    "value": [10, 20, 30, 40, 50, 60],
}
df = pd.DataFrame(data)

# Custom color the nodes
html = d3.sankey(
    df,
    filepath=r"c://temp//sankey.html",
    color={
        "A": "#FF0000",
        "B": "#000000",
        "C": "#FF0000",
        "D": "#7FFFD4",
        "E": "#000000",
        "F": "#000000",
        "G": "#FF0000",
    },
)

# Alternatively:
d3 = D3Blocks(chart="Sankey", frame=True)
d3.set_node_properties(
    df,
    color={
        "A": "#FF0000",
        "B": "#000000",
        "C": "#FF0000",
        "D": "#7FFFD4",
        "E": "#000000",
        "F": "#000000",
        "G": "#FF0000",
    },
)
d3.set_edge_properties(df, color="target", opacity="target")
d3.show(filepath=r"c://temp//sankey.html")

# -------------------------------------------------------------------
