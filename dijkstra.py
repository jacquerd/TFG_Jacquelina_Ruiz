import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from(['A','B','C','D','E','F'])

edges_with_weights = [('A','B',3),('A','D',4),('A','E',6),
                      ('B','C',1),('B','F',5),('B','E',1),
                      ('C','F',5),('C','E',2),('C','D',3),
                      ('D','F',4),('D','E',4)]

G.add_weighted_edges_from(edges_with_weights)

def estimado_minimo(T,d):
    nodo_sol = None
    valor_min = float('inf')
    for u in T:
        if d[u] < valor_min:
            valor_min = d[u]
            nodo_sol = u
    return nodo_sol


def dijkstra(graph):
    root = sorted(list(graph.nodes()))[0]
    d = {}
    d[root] = 0
    parent = {}
    parent[root] = -1
    resto = sorted(list(graph.nodes()))
    for node in resto: 
        if node != root:
            parent[node] = -1
            d[node] = float('inf')
    
    #T es la lista de vértices no procesados
    T = sorted(list(graph.nodes()))
    u = root
    
    while T!=[]:
        #para asegurarnos de que los nodos que quedan son alcanzables
        #(esto es por si el grafo es desconectado)
        if u is None:
            break

        T.remove(u) #hemos procesado el vértice u
        N_u = sorted(list(graph.neighbors(u)))
        for v in N_u:
            if (v in T) and (d[v]>d[u]+ graph[u][v]['weight']):
                d[v] = d[u]+ graph[u][v]['weight']
                parent[v] = u
        
        #ahora u es el vértice de T con el estimado más pequeño
        u = estimado_minimo(T,d)
    return parent

#Ejecución
resultado = dijkstra(G)
print(resultado)