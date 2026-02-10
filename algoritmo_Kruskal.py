import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from([1,2,3,4,5,6])

edges_with_weights = [(1,2, 20), (1,3,40), (1,5,30), (1,6,30),
                      (2,4,20), (2,6,30),(3,5,20),(3,6,40),
                      (4,6,40)]
G.add_weighted_edges_from(edges_with_weights)


def find(i, parent):
    j = i
    while (parent[j]!=j):
        j = parent[j]
    return j

def union(i,j,parent):
    root1 = find(i,parent)
    root2 = find(j,parent)
    if root1 != root2:
        parent[root2] = root1

def algoritmo_kruskal(graph):

    parent = {node: node for node in graph.nodes()}

    #creamos un grafo que solo tiene los vertices de G
    T = nx.Graph()
    T.add_nodes_from(graph.nodes())
   
    sorted_edges = sorted(graph.edges(data=True), key = lambda x: x[2]['weight'])

    for u,v, data in sorted_edges: 
        #si los vertices u y v están en árboles diferentes,
        #entonces los unimos y agregamos la arista (u,v) a T
        if find(u,parent)!= find(v,parent):
            T.add_edge(u,v,weight = data['weight'])
            union(u,v,parent)
    return T

#Ejecución
mst_kruskal = algoritmo_kruskal(G)

#calculamos el peso total
peso_total = sum(data['weight'] for u,v, data in mst_kruskal.edges(data=True))
print(f"El peso total del Árbol de expansión mínimo es {peso_total}")

#Visualización
plt.figure(figsize=(10,5))

#Grafo original G
plt.subplot(1,2,1)

pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color= 'pink')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G,pos, edge_labels= labels)
plt.title('Grafo G original')

#Grafo de expansión mínimo (Algoritmo de Kruskal)
plt.subplot(1,2,2)
nx.draw(mst_kruskal, pos, with_labels=True, node_color ='green')
labels_mst = nx.get_edge_attributes(mst_kruskal, 'weight')
nx.draw_networkx_edge_labels(mst_kruskal, pos, edge_labels = labels_mst)
plt.title('Grafo MST(Algoritmo de Kruskal)')

plt.tight_layout() # Ajusta automáticamente los márgenes para que nada se monte encima de nada
plt.show()