import networkx as nx
import heapq 

#Hemos quitado la función estimado_minimo(T, d) ya que ahora no es necesaria

def dijkstra(graph, start_vertex, end_vertex):
    if start_vertex==end_vertex:
        return [start_vertex]
    

    d = {node: float('inf') for node in graph.nodes()}
    d[start_vertex] = 0
    
    parent = {node: -1 for node in graph.nodes()}
    
    T = [(0, start_vertex)] #T es ahora la cola de prioridad
    procesados = set() 
    
    while T:
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
                #metemos el vértice v con su nueva distancia => el vértice v puede estar
                #varias veces en T con distintas distancias, pero como heap saca primero los números
                #más pequeños, la versión más corta saldrá primero

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