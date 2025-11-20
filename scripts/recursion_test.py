import networkx as nx

# # from pyvis.network import Network
# # TODO: Test the recursion with a known (and small) network.

for i in range(50):
    print("")

data = {
    "a": ["b", "c", "d"],
    "b": ["i", "j", "k"],
    "c": ["h"],
    "d": ["e", "f", "g"],
    "e": [],
    "f": [],
    "g": [],
    "h": [],
    "i": [],
    "j": [],
    "k": ["l", "m", "n"],
    "l": [],
    "m": ["o"],
    "n": [],
    "o": [],
}

G = nx.Graph()
root = "a"
q = data[root]
for c in data[root]:
    G.add_edge(root, c)
while q:
    print(q)
    parent = q.pop(0)
    # G.add_edge(root, parent)
    # print(root, parent)
    if data[parent]:
        for child in data[parent]:
            # print(parent, child)
            G.add_edge(parent, child)
            print(parent, child)

            q.append(child)
    # root = parent


from pyvis.network import Network

nt = Network("1000px", "1700px", notebook=True)
nt.from_nx(G)
nt.show("nx.html")


##################################
# using a dict, a while loop + a for loop
##################################


# for i in range(50): print('')

# graph_data = {"root": {"level-0.A":1,
#                        "level-0.B":{"level-1.B.1":2,
#                                     "level-1.B.2": {"level-2.B.2.1":3, "level-2.B.2.2":1},
#                                     "tomas": {'maura':4, 'daniel':5, 'nora': 6, 'agustin':7}
#                                     },
#                         'ok':{'nor':1, 'tor':3, 'bor':44, 'som':{'cor':3,'rot':11}}}}
# # Empty directed graph
# G = nx.Graph()

# # Iterate through the layers
# q = list(graph_data.items())
# while q:
#     v, d = q.pop()
#     for nv, nd in d.items():
#         G.add_edge(v, nv)
#         if isinstance(nd, dict):
#             q.append((nv, nd))

# from pyvis.network import Network
# nt = Network('1000px', '1700px', notebook=True)
# nt.from_nx(G)
# nt.show('nx.html')
