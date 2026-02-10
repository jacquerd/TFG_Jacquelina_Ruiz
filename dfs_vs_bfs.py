import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

G = nx.Graph()

G.add_nodes_from([1,2,3,4,5,6,7,8])
G.add_edges_from([(1,2),(1,3),(1,4),
                  (2,5),(2,6),(3,6),
                  (5,6),(5,7),(7,8)])
def dephth_first_search(graph, start_vertex):
    # Inicializar la pila vacía S
    S = []

    # Para cada vértice de G: status(v)=1
    # 1: no procesado, 2: en pila, 3: procesado
    status = {node:1 for node in graph.nodes()}

    #status(a)=2, meterlo en la pila
    status[start_vertex] = 2
    S.append(start_vertex)

    order_of_visit=[]

    while len(S)>0:
        #Cogemos un vértice x de la pila S
        x = S.pop()

        #Marcamos al vértice x como procesado
        status[x] = 3
        order_of_visit.append(x)
        print(f"Nodo {x} procesado")

        #Obtenemos los vecinos de x
        neighbors = list(graph.neighbors(x))

        for j in neighbors:
            if status[j] ==1: #j es un vertice no procesado
                status[j] = 2 #Marcamos al vértice j como procesado
                S.append(j) #Metemos al vértice j en la pila S
    return order_of_visit

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


#ejecutamos los algoritmos empezando por el nodo 1 
resultado_dfs = dephth_first_search(G,1)
resultado_bfs = breadth_first_search(G,1)

print("-" * 30)
print(f"{'PASO':<6} | {'DFS':<10} | {'BFS':<10}")
print("-" * 30)
for i in range(len(resultado_dfs)):
    print(f"{i+1:<6} | {resultado_dfs[i]:<10} | {resultado_bfs[i]:<10}")
print("-" * 30)
