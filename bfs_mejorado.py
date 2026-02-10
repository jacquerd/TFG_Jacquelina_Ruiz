import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

G = nx.Graph()

G.add_nodes_from([1,2,3,4,5,6,7,8])
G.add_edges_from([(1,2),(1,3),(1,4),
                  (2,5),(2,6),(3,6),
                  (5,6),(5,7),(7,8)])

def breadth_first_search(graph, start_vertex):
    # Inicializar la cola vacía Q
    Q = deque()

    # Para cada vértice de G: status(v)=1
    # 1: no procesado, 2: en cola, 3: procesado
    status = {node:1 for node in graph.nodes()}

    #status(a)=2, meterlo en la cola
    status[start_vertex] = 2
    Q.append(start_vertex)

    order_of_visit=[]

    while len(Q)>0:
        #Cogemos un vértice x de la cola Q
        x = Q.popleft()

        #Marcamos al vértice x como procesado
        status[x] = 3
        order_of_visit.append(x)
        print(f"Nodo {x} procesado")

        #Obtenemos los vecinos de x
        neighbors = list(graph.neighbors(x))

        for j in neighbors:
            if status[j] ==1: #j es un vertice no procesado
                status[j] = 2 #Marcamos al vértice j como procesado
                Q.append(j) #Metemos al vértice j en la cola S
    return order_of_visit

#ejecutamos el algoritmo empezando por el nodo 1 
resultado = breadth_first_search(G,1)
print(f"\nOrden final de visita: {resultado}")
nx.draw(G, with_labels = True)
plt.show()