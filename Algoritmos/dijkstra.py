import networkx as nx

def estimado_minimo(T,d):
    vertex_sol = None
    valor_min = float('inf')
    for u in T:
        if d[u] < valor_min:
            valor_min = d[u]
            vertex_sol = u
    return vertex_sol

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
    
    #T es la lista de vértices no procesados
    T = list(graph.nodes())
    u = start_vertex
    
    while T!=[]:
        #para asegurarnos de que los nodos que quedan son alcanzables
        #(esto es por si el grafo es desconectado)
        if u is None:
            break

        if u==end_vertex:
            break 

        T.remove(u) #hemos procesado el vértice u

        N_u = list(graph.neighbors(u))
        for v in N_u:
            peso = graph[u][v]['weight']
            if (v in T) and (d[v]>d[u]+ peso):
                d[v] = d[u]+ peso
                parent[v] = u
        
        #ahora u es el vértice de T con el estimado más pequeño
        u = estimado_minimo(T,d)

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