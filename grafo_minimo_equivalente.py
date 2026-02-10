import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_nodes_from([1,2,3,4,5])

edges_with_weights = [(1,3,9),(1,4,6),(2,1,8),
                      (3,2,3),(3,5,4),(4,3,1),
                      (4,2,2),(5,1,5),(5,2,10),(5,4,7)]

G.add_weighted_edges_from(edges_with_weights)


G2 = nx.DiGraph()

G2.add_nodes_from([1,2,3,4])

edges_with_weights2 = [(1,2,1),(1,4,2),(2,3,3),
                       (2,4,4),(3,2,5),(4,1,6), (4,2,7)]

G2.add_weighted_edges_from(edges_with_weights2)

def ruta_alternativa(S,i,j):
    #creamos un grafo con los mismos nodos que el grafo original pero solo con 
    #las aristas de S
    grafo = nx.DiGraph()
    grafo.add_nodes_from(G.nodes())
    grafo.add_edges_from(S)
    #quitamos de este grafo la arista (i,j) para comprobar si hay otra ruta
    #diferente que nos lleve de i a j
    if grafo.has_edge(i,j):
        grafo.remove_edge(i,j)
    return nx.has_path(grafo,i,j)

def grafo_minimo_equivalente(graph):
    n = graph.number_of_nodes()

    #ordenamos las aristas por el peso
    aristas_ordenadas = sorted(graph.edges(data=True), key = lambda x : x[2]['weight'])

    #creamos la lista S de aristas (sin los pesos)
    S = [(u,v) for u,v,data in aristas_ordenadas]

    F = []

    #FASE 1
    for i,j,k in aristas_ordenadas:
        if ruta_alternativa(S,i,j):
            S.remove((i,j))
            F.append((i,j))

    if len(S) == n:
        return S
    
    #FASE 2
    while F != [] and len(S)>n:
        a = max(F, key=lambda edge: graph[edge[0]][edge[1]]['weight']) #arista con mayor valor del grafo original
        peso_a = graph[a[0]][a[1]]['weight']

        F.remove(a)

        S2 = S.copy()
        S2.append(a)

        eliminados = [] #como todavía no sabemos si la iteración va a mejorar la solución, creamos una nueva lista 
        #para luego añadir a F SOLO las aristas que definitivamente vamos a eliminar de G

        for i,j in list(S2): #iteramos sobre una copia de S2 para que no falle al eliminar aristas
            if graph[i][j]['weight'] > peso_a and ruta_alternativa(S2,i,j):
                S2.remove((i,j))
                eliminados.append((i,j))
        if len(S2)<len(S):
            S = S2 
            F.extend(eliminados)
    
    return S

#Ejecución
solucion = grafo_minimo_equivalente(G)
print("El grafo mínimo equivalente para G tiene las siguientes aristas:")
print(solucion)

solucion2 = grafo_minimo_equivalente(G2)
print("El grafo mínimo equivalente para G2 tiene las siguientes aristas:")
print(solucion2)

#Visualización
plt.figure(figsize=(10,6))

#dibujamos G
plt.subplot(1,2,1)

pos = nx.circular_layout(G)

nx.draw_networkx_nodes(G,pos, node_color='pink',node_size=300)

nx.draw_networkx_edges(G,pos,edge_color='pink',connectionstyle='arc3, rad=0.1')

nx.draw_networkx_labels(G, pos)

#marcamos con verde el grafo mínimo equivalente

nx.draw_networkx_edges(G, pos, edgelist=solucion, edge_color='green', width=2,connectionstyle='arc3, rad=0.1')

plt.title('Grafo G')

#dibujamos G2
plt.subplot(1,2,2)

pos2 = nx.circular_layout(G2)

nx.draw_networkx_nodes(G2,pos2, node_color='lightblue',node_size=300)

nx.draw_networkx_edges(G2,pos2,edge_color='lightblue',connectionstyle='arc3, rad=0.1')

nx.draw_networkx_labels(G2, pos2)

nx.draw_networkx_edges(G2, pos2, edgelist=solucion2, edge_color='green', width=2,connectionstyle='arc3, rad=0.1')

plt.title('Grafo G2')

plt.show()

