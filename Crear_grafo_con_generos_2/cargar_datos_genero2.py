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

#Definimos las características de las canciones. Seleccionamos aquellas que son atributos numéricos y nos quedamos
#con las más relevantes (hemos quitado key, mode, liveness)
audio_features = ['danceability', 'energy', 'key', 'loudness', 'mode',
                  'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                  'valence', 'tempo']

#IMPORTANTE: Normalizamos los valores
scaler = StandardScaler()

#Sobreescribimos los datos ya normalizados
df[audio_features] = scaler.fit_transform(df[audio_features])

#Guardamos el dataset ya procesado
df.to_csv('dataset_procesado_generos2.csv', index=False)


