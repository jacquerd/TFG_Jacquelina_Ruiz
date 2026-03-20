import networkx as nx
import heapq 

#Hemos quitado la función estimado_minimo(T, d) ya que ahora no es necesaria

def dijkstra(graph, start_vertex, end_vertex):
    d = {}
    d[start_vertex] = 0

    parent = {}
    parent[start_vertex] = -1

    resto = list(graph.nodes())

    for vertex in resto: 
        if vertex != start_vertex:
            parent[vertex] = -1
            d[vertex] = float('inf')
    
    T = [(0, start_vertex)] #T es ahora la cola de prioridad
    procesados = set() 
    
    while T!=[]:
        #Sacamos el vértice u con el estimado más pequeño directamente de T
        dist, u = heapq.heappop(T)

        #Evitamos procesar nodos repetidos
        if u in procesados:
            continue
        procesados.add(u) #hemos procesado el vértice u

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

    #pasamos a reconstruir el camino de start_vertex a end_vertex
    #(lo reconstruimos desde end_vertex --> ...-->start_vertex y luego le damos la vuelta)

    if d[end_vertex] == float('inf'): #si la distancia es infinita, no hay camino
        return [] 

    camino = []
    x = end_vertex
    
    while x != -1:
        camino.append(x)
        x = parent[x]
        
    return camino[::-1]