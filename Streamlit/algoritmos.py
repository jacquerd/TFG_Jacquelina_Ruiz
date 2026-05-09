from collections import deque
import heapq
import math

def breadth_first_search(graph, start_vertex, end_vertex):
    if start_vertex==end_vertex:
        return [start_vertex], 0, 0
    
    # Inicializar la cola vacía Q
    Q = deque()

    parent = {start_vertex: None}
    procesados = 0

    #Metemos al vértice inicial en la cola
    Q.append(start_vertex)

    while len(Q)>0:
        #Cogemos un vértice x de la cola Q
        x = Q.popleft()
        procesados += 1

        for j in graph.neighbors(x): #recorremos los vecinos de x
            if j not in parent: #si no hemos procesado el vértice j
                parent[j] = x 
                
                if j == end_vertex: #hemos llegado al vértice destino
                    camino = []
                    v_actual = j
                    while v_actual is not None:
                        camino.append(v_actual)
                        v_actual = parent[v_actual]

                    camino = camino[::-1]
                    coste = sum(graph[u][v]['weight'] for u, v in zip(camino[:-1], camino[1:]))

                    return camino, coste, procesados

                Q.append(j) #Metemos al vértice j en la cola 
    
    return [], float('inf'), procesados #no hemos encontrado un camino de start_vertex a end_vertex


def dijkstra(graph, start_vertex, end_vertex):
    if start_vertex==end_vertex:
        return [start_vertex], 0, 0

    d = {node: float('inf') for node in graph.nodes()}
    d[start_vertex] = 0
    
    parent = {node: None for node in graph.nodes()}
    
    T = [(0, start_vertex)] #T es ahora la cola de prioridad
    procesados = set() 
    nodos_explorados = 0
    
    while T:
        #Sacamos el vértice u con el estimado más pequeño directamente de T
        dist, u = heapq.heappop(T)

        #Evitamos procesar nodos repetidos
        if u in procesados:
            continue
        procesados.add(u) #hemos procesado el vértice u
        nodos_explorados += 1

        #para asegurarnos de que los nodos que quedan son alcanzables
        #(esto es por si el grafo es desconectado)
        if dist == float('inf'):
            break

        if u==end_vertex:
            break 

        N_u = list(graph.neighbors(u))
        for v in N_u:
            peso = graph[u][v]['weight']
            if (v not in procesados) and (d[v]>d[u]+ peso):
                d[v] = d[u]+ peso
                parent[v] = u
                heapq.heappush(T, (d[v], v))
                #metemos el vértice v con su nueva distancia => el vértice v puede estar
                #varias veces en T con distintas distancias, pero como heap saca primero los números
                #más pequeños, la versión más corta saldrá primero

    #pasamos a reconstruir el camino de start_vertex a end_vertex
    #(lo reconstruimos desde end_vertex --> ...-->start_vertex y luego le damos la vuelta)

    if d[end_vertex] == float('inf'): #si la distancia es infinita, no hay camino
        return [], d[end_vertex], nodos_explorados


    camino = []
    x = end_vertex
    
    while x is not None:
        camino.append(x)
        x = parent[x]
        
    return camino[::-1], d[end_vertex], nodos_explorados


def heuristica_euclidea(u, v, features_dict):
    coordenadas_u = features_dict[u]
    coordenadas_v = features_dict[v]
    
    suma_cuadrados = sum((a - b)**2 for a, b in zip(coordenadas_u, coordenadas_v))

    return math.sqrt(suma_cuadrados)

def a_estrella(graph, start_vertex, end_vertex, heuristica, features_dict):
    if start_vertex==end_vertex:
        return [start_vertex], 0, 0
    
    d = {node: float('inf') for node in graph.nodes()}
    d[start_vertex] = 0
    
    parent = {node: None for node in graph.nodes()}

    T = [(0 + heuristica(start_vertex, end_vertex, features_dict), start_vertex)] 
    procesados = set()

    nodos_explorados = 0
    
    while T:
        #Sacamos el vértice u con el estimado más pequeño directamente de T
        dist, u = heapq.heappop(T)

        #Evitamos procesar nodos repetidos
        if u in procesados:
            continue
        procesados.add(u) #hemos procesado el vértice u
        nodos_explorados += 1

        #para asegurarnos de que los nodos que quedan son alcanzables
        #(esto es por si el grafo es desconectado)
        if dist == float('inf'):
            break

        if u==end_vertex:
            break 

        N_u = list(graph.neighbors(u))
        for v in N_u:
            peso = graph[u][v]['weight']
            if (v not in procesados) and (d[v]>d[u]+ peso):
                d[v] = d[u]+ peso
                parent[v] = u
                heapq.heappush(T, (d[v] + heuristica(v, end_vertex, features_dict), v))

    #pasamos a reconstruir el camino de start_vertex a end_vertex
    #(lo reconstruimos desde end_vertex --> ...-->start_vertex y luego le damos la vuelta)

    if d[end_vertex] == float('inf'): #si la distancia es infinita, no hay camino
        return [], d[end_vertex], nodos_explorados

    camino = []
    x = end_vertex
    
    while x is not None:
        camino.append(x)
        x = parent[x]
        
    return camino[::-1], d[end_vertex], nodos_explorados
