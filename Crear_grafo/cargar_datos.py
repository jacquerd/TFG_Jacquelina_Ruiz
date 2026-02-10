import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import sys #para salir del programa si hay error

#Cargamos el archivo csv
try:
    df = pd.read_csv('canciones.csv')
    print('Archivo encontrado')
except FileNotFoundError:
    sys.exit()

#Unificamos las fechas: en la columna 'release_date' a veces tenemos 'YYYY-MM-DD' y otras 'YYYY'
# => cogemos solo los 4 primeros caracteres para quedarnos con el año (para hacer esto nos tenemos que
#asegurar de que los datos de la columna sean string)
df['release_date'] = df['release_date'].astype(str) #"obligamos" a que los datos sean strings

df['year'] = df['release_date'].str[:4] #cogemos los 4 primero caracteres

df['year'] = df['year'].astype(int) #convertimos el string a int

#Filtramos las canciones del año 2000 en adelante
df = df[df['year'] >= 2000]

#Eliminamos las canciones con titulos duplicados (nos quedamos con la primera ocurrencia)
df = df.drop_duplicates(subset=['name', 'artists'], keep='first')

#después de filtrar, reiniciamos los indices
df = df.reset_index(drop=True)

#Definimos las columnas que son atributos de audio (numéricos)
audio_features = ['danceability', 'energy', 'key', 'loudness', 'mode',
                    'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                    'valence', 'tempo']

#IMPORTANTE: Normalizamos los valores
scaler = MinMaxScaler()

#Sobre escribimos los datos ya normalizados
df[audio_features] = scaler.fit_transform(df[audio_features])

#Guardamos el dataset ya procesado
df.to_csv('dataset_procesado.csv', index=False)
