import networkx as nx
from collections import deque

#Ahora vamos a mejorar el código anterior: eliminamos la inicialización de los nodos y usamos solo el
#diccionario parents, ya que con él podemos comprobar si un vértice ya ha sido procesado(viendo si está
#en el diccionario) y además encontrar el camino entre start_vertex y end_vertex

def breadth_first_search(graph, start_vertex, end_vertex):
    # Inicializar la cola vacía Q
    Q = deque()

    parent = {start_vertex: None}

    #Metemos al vértice inicial en la cola
    Q.append(start_vertex)

    while len(Q)>0:
        #Cogemos un vértice x de la cola Q
        x = Q.popleft()

        if x == end_vertex: #hemos llegado al vértice destino
            camino = []
            v_actual = j
            while v_actual is not None:
                camino.append(v_actual)
                v_actual = parent[v_actual]
            return camino[::-1]

        for j in graph.neighbors(x): #recorremos los vecinos de x
            if j not in parent: #si el vértice j no ha sido descubierto
                parent[j] = x 
                Q.append(j) #encolamos el vértice j
    
    return None #no hemos encontrado un camino de start_vertex a end_vertex

