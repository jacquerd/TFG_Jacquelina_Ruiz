import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import sys #para salir del programa si hay error

#Vamos a mapear los géneros a 8 "super-géneros" principales
mapa_generos = {
    'techno': 'ELECTRONIC', 'house': 'ELECTRONIC', 'edm': 'ELECTRONIC',
    'electro': 'ELECTRONIC', 'dubstep': 'ELECTRONIC', 'trance': 'ELECTRONIC',
    'disco': 'ELECTRONIC', 'party': 'ELECTRONIC', 'dance': 'ELECTRONIC',
    'club': 'ELECTRONIC', 'industrial': 'ELECTRONIC', 'idm': 'ELECTRONIC',
    'electronic': 'ELECTRONIC', 'breakbeat': 'ELECTRONIC', 'chicago-house': 'ELECTRONIC',
    'deep-house': 'ELECTRONIC', 'detroit-techno': 'ELECTRONIC', 'drum-and-bass': 'ELECTRONIC',
    'garage': 'ELECTRONIC', 'hardcore': 'ELECTRONIC', 'hardstyle': 'ELECTRONIC',
    'minimal-techno': 'ELECTRONIC', 'progressive-house': 'ELECTRONIC',

    'metal': 'ROCK', 'rock': 'ROCK', 'punk': 'ROCK', 'indie': 'ROCK',
    'alt-rock': 'ROCK', 'heavy-metal': 'ROCK', 'black-metal': 'ROCK',
    'grunge': 'ROCK', 'punk-rock': 'ROCK', 'death-metal': 'ROCK',
    'hard-rock': 'ROCK', 'psych-rock': 'ROCK', 'metalcore': 'ROCK',
    'alternative': 'ROCK', 'emo': 'ROCK', 'goth': 'ROCK', 'grindcore': 'ROCK',
    'j-rock': 'ROCK', 'rock-n-roll': 'ROCK', 'rockabilly': 'ROCK',

    'pop': 'POP', 'k-pop': 'POP', 'indie-pop': 'POP', 'cantopop': 'POP',
    'mandopop': 'POP', 'synth-pop': 'POP', 'power-pop': 'POP', 'j-pop': 'POP',
    'j-dance': 'POP', 'j-idol': 'POP', 'pop-film': 'POP', 'happy': 'POP',
    'british': 'POP', 'french': 'POP', 'german': 'POP', 'indian': 'POP',
    'iranian': 'POP', 'malay': 'POP', 'spanish': 'POP', 'swedish': 'POP',
    'turkish': 'POP',

    'hip-hop': 'URBAN', 'trap': 'URBAN', 'r-n-b': 'URBAN', 'trip-hop': 'URBAN',
    'afrobeat': 'URBAN', 'funk': 'URBAN', 'soul': 'URBAN', 'groove': 'URBAN',
    'dancehall': 'URBAN', 'dub': 'URBAN',

    'reggaeton': 'LATIN', 'salsa': 'LATIN', 'latin': 'LATIN', 'latino': 'LATIN',
    'mpb': 'LATIN', 'samba': 'LATIN', 'pagode': 'LATIN', 'reggae': 'LATIN',
    'brazil': 'LATIN', 'forro': 'LATIN', 'sertanejo': 'LATIN', 'tango': 'LATIN',

    'classical': 'JAZZ_CLASSICAL', 'opera': 'JAZZ_CLASSICAL', 'jazz': 'JAZZ_CLASSICAL',
    'blues': 'JAZZ_CLASSICAL', 'country': 'JAZZ_CLASSICAL', 'ska': 'JAZZ_CLASSICAL',
    'bluegrass': 'JAZZ_CLASSICAL', 'folk': 'JAZZ_CLASSICAL', 'gospel': 'JAZZ_CLASSICAL',
    'honky-tonk': 'JAZZ_CLASSICAL', 'world-music': 'JAZZ_CLASSICAL',

    'ambient': 'CHILL', 'piano': 'CHILL', 'acoustic': 'CHILL',
    'chill': 'CHILL', 'sleep': 'CHILL', 'new-age': 'CHILL',
    'romance': 'CHILL', 'study': 'CHILL',
    'guitar': 'CHILL', 'sad': 'CHILL', 
    'singer-songwriter': 'CHILL', 'songwriter': 'CHILL',

    'anime': 'TV_CINEMA', 'disney': 'TV_CINEMA', 'show-tunes': 'TV_CINEMA',
    'children': 'TV_CINEMA', 'kids': 'TV_CINEMA',
    'soundtracks': 'TV_CINEMA', 'movies': 'TV_CINEMA'
}

blacklist = ['comedy'] #gente hablando, no nos interesa

#Procesamos el dataset
#Cargamos el archivo csv
try:
    df = pd.read_csv('dataset_generos.csv')
    print('Archivo encontrado')
except FileNotFoundError:
    sys.exit()

#Eliminamos las canciones con titulos duplicados (nos quedamos con la primera ocurrencia)
df = df.drop_duplicates(subset=['track_name', 'artists'], keep='first')

#quitamos el genero de la lista negra
if 'track_genre' in df.columns:
    df = df[~df['track_genre'].isin(blacklist)]

#creamos la columna 'super_genre' usando mapa_generos. si el género no está en el mapa,
#lo metemos a 'OTROS'
df['super_genre'] = df['track_genre'].map(mapa_generos).fillna('OTROS')

#eliminamos las canciones de 'OTROS'
df = df[df['super_genre'] != 'OTROS']

#después de filtrar, reiniciamos los indices
df = df.reset_index(drop=True)
print(f"Filas finales tras limpieza y filtrado: {len(df)}")

#Definimos las columnas que son atributos de audio (numéricos)
audio_features = ['danceability', 'energy', 'key', 'loudness', 'mode',
                    'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                    'valence', 'tempo']

#IMPORTANTE: Normalizamos los valores
scaler = MinMaxScaler()

#Sobre escribimos los datos ya normalizados
df[audio_features] = scaler.fit_transform(df[audio_features])

#Guardamos el dataset ya procesado
df.to_csv('dataset_procesado_con_generos.csv', index=False)


