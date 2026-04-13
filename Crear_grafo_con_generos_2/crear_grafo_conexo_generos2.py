import pandas as pd
import networkx as nx
from sklearn.neighbors import NearestNeighbors
import time
import sys

#matriz de adyacencias de los géneros
grafo_generos = {
    'edm': ['pop'],
    'rock': ['pop'],
    'rap': ['latin', 'r&b'],
    'pop': ['rock', 'edm', 'latin', 'r&b'],
    'r&b': ['pop', 'latin'],
    'latin': ['pop', 'r&b', 'rap']
}

#géneros incompatibles
incompatibles = {
    'rock': ['latin', 'rap'],
    'latin': ['rock'],
    'rap': ['rock'],
}

#vamos a analizar el tipo de relación que tienen dos géneros
def tipo_relacion(genero_A, genero_B):
    if genero_A == genero_B:
        return "admisible"
    
    if genero_B in incompatibles.get(genero_A, []):
        return "prohibido"
    
    if genero_A in incompatibles.get(genero_B, []):
        return "prohibido"
    
    if (genero_B in grafo_generos.get(genero_A, []) or genero_A in grafo_generos.get(genero_B, [])):
        return "admisible"
    
    return "penalizado"

#Cargar archivo
try:
    print("leyendo")
    df = pd.read_csv('dataset_procesado_generos2.csv')
except FileNotFoundError:
    print("error")
    sys.exit()

df.reset_index(drop=True, inplace=True) #para que los indices de knn coincidan con los del dataframe

#Vamos a crear el grafo usando k-nn

start_time = time.time() #veamos cuánto se tarda en crear el grafo con k-nn

#definimos las características de las canciones
features = ['danceability', 'energy', 'loudness','speechiness', 'acousticness', 
            'instrumentalness','valence', 'tempo']

#Los datos ya estaban escalados (importante para que todas las características estén en igualdad de condiciones 
#ante k-nn)
df_scaled = df[features]

#Definimos k objetivo: número de vecinos finales que queremos en el grafo
k_objetivo = 11

#Definimos k búsqueda: número de vecinos que propondrá k-nn (después de todos estos vecinos elegiremos 
#con cuáles nos quedamos)
k_busqueda = k_objetivo * 4

knn = NearestNeighbors(n_neighbors=k_busqueda, metric='euclidean', algorithm='ball_tree')
knn.fit(df_scaled.values)
distancias, indices = knn.kneighbors(df_scaled.values)

#crear el grafo
G = nx.Graph()

G.add_nodes_from(df.index) #el índice es el ID del nodo

edges = []
canciones_aisladas = 0 

for i in range(len(df)):
    genero_origen = df.loc[i, 'playlist_genre']
    conexiones_hechas = 0
    
    #iteramos sobre los vecinos candidatos (empezamos en 1 para saltar la propia canción y no formar lazos)
    for j in range(1, k_busqueda):
        vecino = indices[i][j]
        dist = distancias[i][j] #distancia euclídea
        genero_vecino = df.loc[vecino, 'playlist_genre']
        
        #vemos si podemos conectar las canciones según las reglas que describimos antes
        relacion = tipo_relacion(genero_origen, genero_vecino)
        if relacion == "prohibido":
            continue
        elif relacion == "admisible":
            peso_final = dist
        else:  #penalizado
            peso_final = dist * 2

        edges.append((i, vecino, peso_final))
        conexiones_hechas += 1

        #si ya hemos formado 10(11-1) conexiones, paramos
        if conexiones_hechas >= (k_objetivo - 1):
            break
        
    #Si hay una canción que no tenga ningún vecino compatible de sus 43 (44-1) vecinos más cercanos
    #forzamos la conexión con el más cercano (aunque los géneros no sean compatibles) para que no se quede aislada
    if conexiones_hechas == 0:
        vecino_auxiliar = indices[i][1]
        dist_auxiliar = distancias[i][1] * 10.0 # Le ponemos peso alto para que sea el último recurso
        edges.append((i, vecino_auxiliar, dist_auxiliar))
        canciones_aisladas += 1
    

G.add_weighted_edges_from(edges)

#Comprobamos si el grafo que hemos creado es conexo o no
es_conexo = nx.is_connected(G)
print(f"G es totalmente conexo?: {es_conexo}")

if es_conexo:
    G_final = G #el grafo ya era conexo
else: 
    num_componentes = nx.number_connected_components(G)

    #Vemos cual es el tamaño de la componente conexa más grande
    largest_cc_nodes = max(nx.connected_components(G), key=len)

    porcentaje = (len(largest_cc_nodes) / len(df)) * 100

    print(f"La componente conexa más grande cubre el {porcentaje} % del grafo")

    #Si larguest_cc cubre más del 90% de la bbdd, esta parte conexa del grafo es suficientemente grande
    #por lo que quitamos las canciones que lo desconectan
    if porcentaje > 90:
        G_final = G.subgraph(largest_cc_nodes).copy()
        df_final = G_final.nodes()
        print(f"Dataset original: {len(df)} canciones")
        print(f"Dataset final:    {len(df_final)} canciones")
    else: 
        sys.exit() #si no cubre más del 90% no lo queremos => salimos y no creamos ningún archivo

#comprobamos también que no haya demasiadas aristas aisladas(si las hubiera tendríamos que aumentar k)
total_canciones = len(df)
porcentaje_aisladas = (canciones_aisladas / total_canciones) * 100

print(f"Había {porcentaje_aisladas}% de canciónes 'aisladas'")
if porcentaje_aisladas > 20:
    sys.exit()

#ahora vamos a crear un .csv con las aristas y también a cambiar los índices numéricos por los nombres
#de las canciones
lista_aristas = []


#escribimos las canciones como: "Canción - Arista" por si hay dos canciones con el mismo nombre pero de 
#artistas diferentes

columna_nombre = 'track_name'
columna_artista = 'track_artist'


for u,v,data in G_final.edges(data=True):
    cancion_origen = f"{df.loc[u, columna_nombre]} - {df.loc[u, columna_artista]}"
    cancion_destino = f"{df.loc[v, columna_nombre]} - {df.loc[v, columna_artista]}"

    genero_origen = df.loc[u, 'playlist_genre']
    genero_destino = df.loc[v, 'playlist_genre']

    peso = data['weight']

    lista_aristas.append({'source': cancion_origen, 'target':cancion_destino, 'weight': peso,
                          'source_genre': genero_origen, 'target_genre': genero_destino})
 
df_aristas = pd.DataFrame(lista_aristas)

df_aristas.to_csv('dataset_final_graph2.csv', index=False)

end_time = time.time()

tiempo_total = end_time - start_time

print(f"El grafo G se ha creado en {tiempo_total} segundos")

