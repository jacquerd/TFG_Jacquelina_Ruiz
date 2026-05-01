import networkx as nx
from collections import deque

#Vamos a hacer una última mejora. Para ahorrarnos una iteración del while, vamos a comprobar
#si hemos llegado al vértice destino en el bucle for

def breadth_first_search(graph, start_vertex, end_vertex):
    if start_vertex==end_vertex:
        return [start_vertex]
    
    # Inicializar la cola vacía Q
    Q = deque()

    parent = {start_vertex: None}

    #Metemos al vértice inicial en la cola
    Q.append(start_vertex)

    while len(Q)>0:
        #Cogemos un vértice x de la cola Q
        x = Q.popleft()

        for j in graph.neighbors(x): #recorremos los vecinos de x
            if j not in parent: #si el vértice j no ha sido descubierto
                parent[j] = x 
                
                if j == end_vertex: #hemos llegado al vértice destino
                    return camino(end_vertex,parent)

                Q.append(j) #encolamos el vértice j
    
    return None #no hemos encontrado un camino de start_vertex a end_vertex


def camino(end_vertex, parent):
    solucion = []
    v = end_vertex
    while v is not None:
        solucion.append(v)
        v = parent[v]
    return solucion[::-1]
