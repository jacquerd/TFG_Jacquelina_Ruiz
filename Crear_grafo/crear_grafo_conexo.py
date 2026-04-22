import pandas as pd
import networkx as nx
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import time
import sys

df = pd.read_csv('dataset_procesado.csv')

df.reset_index(drop=True, inplace=True) #para que los indices de knn coincidan con los del dataframe

print(f"Trabajando con {len(df)} canciones")

#Vamos a crear el grafo usando k-nn
#probamos con k=11 (11-1, ya que el vecino 1 es la propia canción): no queremos que
#k sea muy pequeño(porque entonces el grafo no sería conexo) ni tampoco muy grande(porque
#complicaría el grafo)
k = 11

start_time = time.time() #veamos cuánto se tarda en crear el grafo con k-nn

#primero he probado con todas las features pero entonces G solo cubría el 61.16% de las canciones,
#así que he eliminado key, mode, liveness ya que no eran muy relevantes

features = ['danceability', 'energy', 'loudness','speechiness', 'acousticness', 
            'instrumentalness','valence', 'tempo']

#Los datos ya estaban escalados
df_scaled = df[features].copy()


#Hay características a las que les tenemos que dar más peso, ya que si no se podrían juntar, por ejemplo,
#una cancion de pop con una de rock solo por que las dos son rápidas 

weights = {
    #mide lo "bailable" que es una canción
    'danceability': 1.1, 

    #diferencia lo chill de lo intenso
    'energy': 1, 

    #depende solo de la grabación
    'loudness': 0.2,

    #mide si la voz suena a discurso(palabras habladas) o a una melodía cantada
    #nos puede servir para separar el rap del resto de géneros
    'speechiness': 1.0,

    #es el más útil para diferenciar géneros
    'acousticness': 3.0,     

    #separa que solo tienen instrumento(entonces >>>) de las que tienen voz, ya sea "hablando" o cantando (<<<)
    'instrumentalness': 1.5, 

    #diferencia lo triste de lo feliz
    'valence': 1.8,                      

    #mide lo "rápido" que va una canción
    'tempo': 0.5,                  
}

#le damos a cada feature su importancia
for feature, weight in weights.items():
    if feature in df_scaled.columns:
        df_scaled[feature] = df_scaled[feature] * weight

knn = NearestNeighbors(n_neighbors=k, metric='euclidean', algorithm='ball_tree')
knn.fit(df_scaled.values)
distancias, indices = knn.kneighbors(df_scaled.values)

#crear el grafo
G = nx.Graph()

G.add_nodes_from(df.index) #el índice es el ID del nodo

edges = []
for i in range(len(df)):
    for j in range(1, k): #empezamos en 1 para no crear un lazo
        vecino_idx = indices[i][j]
        distancia = distancias[i][j]
        edges.append((i, vecino_idx, distancia))

G.add_weighted_edges_from(edges)

#Comprobamos si el grafo que hemos creado es conexo o no
es_conexo = nx.is_connected(G)
print(f"G es totalmente conexo?: {es_conexo}")


if es_conexo:
    G_final = G #el grafo ya era conexo
else: 
    #Vemos cual es el tamaño de la componente conexa más grande
    largest_cc_nodes = max(nx.connected_components(G), key=len)

    porcentaje = (len(largest_cc_nodes) / len(df)) * 100

    print(f"La componente conexa más grande cubre el {porcentaje} % del grafo")

    #Si larguest_cc cubre más del 90% de la bbdd, esta parte conexa del grafo es suficientemente grande
    #por lo que quitamos las canciones que lo desconectan
    if porcentaje > 90:
        G_final = G.subgraph(largest_cc_nodes).copy()
        nodos_final = G_final.nodes()
        print(f"Dataset original: {len(df)} canciones")
        print(f"Dataset final:    {len(nodos_final)} canciones")
    else: 
        sys.exit() #si no cubre más del 90% no lo queremos => salimos y no creamos ningún archivo


#ahora vamos a crear un .csv con las aristas y también a cambiar los índices numéricos por los nombres
#de las canciones
lista_aristas = []

columna_nombre = 'name'

for u,v,data in G_final.edges(data=True):
    cancion_origen = df.loc[u,columna_nombre]
    cancion_destino = df.loc[v,columna_nombre]
    peso = data['weight']

    lista_aristas.append({'source': cancion_origen, 'target':cancion_destino, 'weight': peso})

df_aristas = pd.DataFrame(lista_aristas)

df_aristas.to_csv('dataset_final_graph.csv', index=False)

end_time = time.time()

tiempo_total = end_time - start_time

print(f"El grafo G se ha creado en {tiempo_total} segundos")
