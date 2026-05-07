import networkx as nx
from collections import deque

#Vamos a cambiar el algoritmo para que dados un vértice inicial y final, nos devuelva el camino más corto
#entre estos dos vértices

def breadth_first_search(graph, start_vertex, end_vertex):
    #Inicializar la cola vacía Q
    Q = deque()

    #Para cada vértice de G: status(v)=1
    # 1: no procesado, 2: en cola, 3: procesado
    status = {node: 1 for node in graph.nodes()}

    #añadimos esto para saber el camino del vértice final al inicial
    parent = {node: None for node in graph.nodes()}

    #status(a)=2, meterlo en la cola
    status[start_vertex] = 2
    Q.append(start_vertex)

    found = False #para saber si hemos encontrado o no el camino

    while len(Q)>0:
        #Cogemos un vértice x de la cola Q
        x = Q.popleft()

        if x == end_vertex: #hemos llegado al vértice destino
            found = True
            break

        #Marcamos al vértice x como procesado
        status[x] = 3

        #Obtenemos los vecinos de x
        neighbors = list(graph.neighbors(x))

        for j in neighbors:
            if status[j] == 1: #j es un vertice no procesado
                status[j] = 2 #Marcamos al vértice j como descubierto
                parent[j] = x
                Q.append(j) #Metemos al vértice j en la cola 
    
    if found:
        #hemos encontrado el camino
        camino = []
        v_actual = end_vertex
        while v_actual is not None:
            camino.append(v_actual)
            v_actual = parent[v_actual]
        return camino[::-1] #le damos la vuelta al camino para que salga desde el inicial hasta el final
    else:
        return [] #no hemos encontrado el camino
