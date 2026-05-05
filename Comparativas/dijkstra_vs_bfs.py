import networkx as nx
import pandas as pd
import time
import heapq
from collections import deque


def breadth_first_search(graph, start_vertex, end_vertex):
    if start_vertex==end_vertex:
        return [start_vertex]
    
    # Inicializar la cola vacía Q
    Q = deque()

    parents = {start_vertex: None}
    procesados = 0

    #Metemos al vértice inicial en la cola
    Q.append(start_vertex)

    while len(Q)>0:
        #Cogemos un vértice x de la cola Q
        x = Q.popleft()
        procesados += 1

        for j in graph.neighbors(x): #recorremos los vecinos de x
            if j not in parents: #si no hemos procesado el vértice j
                parents[j] = x 
                
                if j == end_vertex: #hemos llegado al vértice destino
                    return camino(end_vertex,parents), procesados

                Q.append(j) #Metemos al vértice j en la cola 
    
    return None, procesados #no hemos encontrado un camino de start_vertex a end_vertex


def camino(end_vertex, parents):
    solucion = []
    v = end_vertex
    while v != None:
        solucion.append(v)
        v = parents[v]
    return solucion[::-1]


def dijkstra(graph, start_vertex, end_vertex):
    if start_vertex==end_vertex:
        return [start_vertex], 0, 0

    d = {node: float('inf') for node in graph.nodes()}
    d[start_vertex] = 0
    
    parent = {node: -1 for node in graph.nodes()}
    
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
    
    while x != -1:
        camino.append(x)
        x = parent[x]
        
    return camino[::-1], d[end_vertex], nodos_explorados


#Cargamos el dataset
df_nodes = pd.read_csv('dataset_procesado_generos2.csv')

df_nodes['node_name'] = df_nodes['track_name'] + " - " + df_nodes['track_artist']

#Definimos las features
features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo']

features_dict = {row['node_name']: tuple(row[features]) for c, row in df_nodes.iterrows()}
generos_dict = {row['node_name']: row['playlist_genre'].upper() for c, row in df_nodes.iterrows()}

#Cargamos el grafo
df_edges = pd.read_csv('dataset_final_graph2.csv')
G = nx.from_pandas_edgelist(df_edges, 'source', 'target', ['weight'])


origen = "Fix You - Coldplay"
destino = "Yellow - Coldplay"

#origen = "Mockingbird - Eminem"
#destino = "Whatever It Takes - Imagine Dragons"

#origen = "Shape of You - Ed Sheeran"
#destino = "Enter Sandman - Metallica"

#origen = "Me Gustas Tu - Manu Chao"
#destino = "Knockin' On Heaven's Door - Guns N' Roses"

#Ejecutamos Dijkstra
start = time.perf_counter()
camino_d, coste_d, nodos_explorados_d = dijkstra(G, origen, destino)
time_d = time.perf_counter() - start

#Ejecutamos bfs
start_bfs = time.perf_counter()
camino_bfs, nodos_explorados_bfs = breadth_first_search(G, origen, destino)
time_bfs = time.perf_counter() - start_bfs

coste_real_bfs = sum(G[u][v]['weight'] for u, v in zip(camino_bfs[:-1], camino_bfs[1:]))

print("Comparativa Dijskstra VS BFS")
print("-" * 60)
print(f"{'Criterio':<20} | {'Dijkstra':<15} | {'BFS'}")
print("-" * 60)
print(f"{'Tiempo de cálculo':<20} | {time_d:.2f} s          | {time_bfs:.2f} s")
print(f"{'Nodos explorados':<20} | {nodos_explorados_d:<15} | {nodos_explorados_bfs}")
print(f"{'Coste de la ruta':<20} | {coste_d:.4f}          | {coste_real_bfs:.4f}")
print(f"{'Saltos (Canciones)':<20} | {len(camino_d)-1:<15} | {len(camino_bfs)-1}")
print("-" * 60)

print("PLAYLIST DE DIJKSTRA:")
for i, nodo in enumerate(camino_d):
    print(f" {i}. [{generos_dict.get(nodo, 'Desconocido')}] {nodo}")

print("PLAYLIST DE BFS:")
for i, nodo in enumerate(camino_bfs):
    print(f" {i}. [{generos_dict.get(nodo, 'Desconocido')}] {nodo}")

