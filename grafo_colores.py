import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from([(1, {"color": "green"}),
                  (2, {"color": "red"}),
                  (3, {"color": "pink"}),
                  (4, {"color": "blue"}),
                  (5, {"color":"yellow"})])

G.add_edges_from([(1, 3, {'weight': 0.76}),
                  (1, 2, {'weight': 0.5}),
                  (2, 3, {'weight': 0.98}),
                  (2, 4, {'weight': 0.22}),
                  (3, 4, {'weight': 0.11}),
                  (3, 5, {'weight': 0.88}),
                  (4, 5, {'weight': 0.77})])

colors = [node[1]['color'] for node in G.nodes(data=True)]

nx.draw(G, with_labels= True, node_color=colors)
plt.show()
