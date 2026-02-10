import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_nodes_from(['a','b','c','d','e','f'])

edges_with_weights = [('s','a',3),('s','c',5),('s','e',2),
                      ('a','b',-4),('b','g',4),('c','d',6),
                      ('d','c',-3),('d','g',8),('e','f',3),
                      ('f','e',-6),('f','g',7)]

G.add_weighted_edges_from(edges_with_weights)

G2 = nx.DiGraph()

G2.add_nodes_from(['t','s','x','y','z'])

edges_with_weights2 = [('s', 't', 6),('s', 'y', 7),
                       ('t', 'x', 5),('t', 'y', 8),
                       ('t', 'z', -4),('x', 't', -2),
                       ('y', 'x', -3),('y', 'z', 9),
                       ('z', 's', 2),('z', 'x', 7)]

G2.add_weighted_edges_from(edges_with_weights2)


def bellmanFord (graph, root):
    d = {}
    d[root] = 0
    parent = {}
    parent[root] = -1
    resto = sorted(list(graph.nodes()))
    for v in resto:
        if v != root:
            d[v] = float('inf')
            parent[v] = -1

    n = graph.number_of_nodes()

    #repetimos el proceso de relajar todo n-1 veces
    for i in range(n-1):
        for (u,v) in graph.edges():
            if (d[v]>d[u]+ graph[u][v]['weight']):
                d[v] = d[u]+ graph[u][v]['weight']
                parent[v] = u

    #comprobamos si cambia algo al relajar 1 vez más
    for (u,v) in graph.edges():
         if (d[v]>d[u]+ graph[u][v]['weight']):
             #como algo cambia --> se ha detectado un circuito con peso negativo alcanzable desde root
             ciclo_negativo = [(u, v)]
             return False, None, ciclo_negativo
    return True, parent, None


#Ejecución
solucion = bellmanFord(G,'s')
print(solucion)

solucion2 = bellmanFord(G2,'s')
print(solucion2)

#Visualización

#tamaño total de la "hoja"
plt.figure(figsize=(10,6))

#dividimos la hoja y pintamos en el lado izquierdo
plt.subplot(1,2,1)

pos = nx.circular_layout(G)

#dibujamos G

#dibujar nodos y etiquetas
nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=300)
nx.draw_networkx_labels(G, pos)

nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True,connectionstyle='arc3, rad=0.1')
#connectionstyle='arc3, rad=0.1': para dibujar las aristas como curvas simples 
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u,v): d['weight'] for u,v,d in G.edges(data=True)}, label_pos=0.3)

#pintamos el circuito negativo
if solucion[0] == False:
    nx.draw_networkx_edges(G, pos, edgelist=solucion[2], edge_color='red', width=3, connectionstyle='arc3, rad=0.1')

plt.title('Grafo G')

#pasamos al lado derecho
plt.subplot(1,2,2)
pos2 = nx.circular_layout(G2)

#dibujamos G2
nx.draw_networkx_nodes(G2, pos2, node_color='lightpink', node_size=300)
nx.draw_networkx_labels(G2, pos2)

nx.draw_networkx_edges(G2, pos2, edge_color='pink', arrows=True, connectionstyle='arc3, rad=0.1')
nx.draw_networkx_edge_labels(G2, pos2, edge_labels={(u,v): d['weight'] for u,v,d in G2.edges(data=True)}, label_pos=0.3)

#pintamos los caminos 
if solucion2[0] == True:
    parents = solucion2[1]
    ruta_edges = []
    for u, v in parents.items():
        if v != -1:
            ruta_edges.append((v, u))

    nx.draw_networkx_edges(G2, pos2, edgelist=ruta_edges, edge_color='green', width=2,connectionstyle='arc3, rad=0.1')

plt.title('Grafo G2')

plt.show()