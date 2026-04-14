import pandas as pd
from sklearn.preprocessing import StandardScaler
import sys #para salir del programa si hay error

#Procesamos el dataset
#Cargamos el archivo csv
try:
    df = pd.read_csv('spotify_songs.csv')
    print('Archivo encontrado')
except FileNotFoundError:
    sys.exit()

#Eliminamos las canciones con titulos duplicados (nos quedamos con la primera ocurrencia)
df = df.drop_duplicates(subset=['track_name', 'track_artist'], keep='first')

#después de filtrar, reiniciamos los índices
df = df.reset_index(drop=True)
print(f"Filas finales tras limpieza y filtrado: {len(df)}")

#Elegimos las variables que vamos a escalar
features_to_scale = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness','valence', 'tempo']

#Escalamos los valores
scaler = StandardScaler()
df[features_to_scale] = scaler.fit_transform(df[features_to_scale])

#key y mode siguen en el dataframe pero con sus valores originales

#Guardamos el dataset ya procesado
df.to_csv('dataset_procesado_generos2.csv', index=False)


