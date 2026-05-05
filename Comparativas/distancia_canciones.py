import networkx as nx
import pandas as pd
import math


#Cargamos el dataset
df_nodes = pd.read_csv('dataset_procesado_generos2.csv')

df_nodes['node_name'] = df_nodes['track_name'] + " - " + df_nodes['track_artist']

#Definimos las features
features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo']

features_dict = {row['node_name']: tuple(row[features]) for c, row in df_nodes.iterrows()}
generos_dict = {row['node_name']: row['playlist_genre'].upper() for c, row in df_nodes.iterrows()}


origen1 = "Fix You - Coldplay"
destino1 = "Yellow - Coldplay"

origen2 = "Mockingbird - Eminem"
destino2 = "Whatever It Takes - Imagine Dragons"

origen3 = "Shape of You - Ed Sheeran"
destino3 = "Enter Sandman - Metallica"

origen4 = "Me Gustas Tu - Manu Chao"
destino4 = "Knockin' On Heaven's Door - Guns N' Roses"

pares = [ (origen1, destino1), (origen2, destino2), (origen3, destino3), (origen4, destino4)]

def distancia_euclidea(u, v, features_dict):
    coordenadas_u = features_dict[u]
    coordenadas_v = features_dict[v]
    
    suma_cuadrados = sum((a - b)**2 for a, b in zip(coordenadas_u, coordenadas_v))

    return math.sqrt(suma_cuadrados)


def calcular_distancias(pares, features_dict):
    resultados = []
    
    for origen, destino in pares:
        if origen not in features_dict or destino not in features_dict:
            resultados.append((origen, destino, None))
            continue
        
        dist = distancia_euclidea(origen, destino, features_dict)
        resultados.append((origen, destino, dist))
    
    return resultados

distancias = calcular_distancias(pares, features_dict)

for origen, destino, dist in distancias:
    print(f"{origen} -> {destino}: {dist}")
