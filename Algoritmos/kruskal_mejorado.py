import networkx as nx

#vamos a mejorar la función find modificando el diccionario para que nos de el padre "inicial", en 
#vez del padre "directo"
def find(i, parent):
    if parent[i] !=i:
        parent[i] = find(parent[i], parent)
    return parent[i]

def union(i,j,parent):
    root1 = find(i,parent)
    root2 = find(j,parent)
    if root1 != root2:
        parent[root2] = root1

def algoritmo_kruskal(graph):
    parent = {node: node for node in graph.nodes()}

    #creamos un grafo que solo tiene los vértices de G
    T = nx.Graph()
    T.add_nodes_from(graph.nodes())
   
    sorted_edges = sorted(graph.edges(data=True), key = lambda x: x[2]['weight'])

    for u,v, data in sorted_edges: 
        #si los vértices u y v están en árboles diferentes,
        #entonces los unimos y agregamos la arista (u,v) a T
        if find(u,parent) != find(v,parent):
            T.add_edge(u,v,weight = data['weight'])
            union(u,v,parent)
    return T

   
