import time
import streamlit as st
import pandas as pd
import networkx as nx

from algoritmos import breadth_first_search, dijkstra, a_estrella, heuristica_euclidea


st.set_page_config(page_title = "Playlists de evolución musical", 
                   layout = "wide", initial_sidebar_state="expanded")


path_nodes = "dataset_procesado_generos2.csv"
path_edges = "dataset_final_graph2.csv"

#características para la heurística
features = ["danceability", "energy", "loudness", "speechiness",
            "acousticness", "instrumentalness", "valence", "tempo",]

#Color asociado a cada género (para que la playlist quede más visual)
color_genero = { "POP":   "blue", "ROCK":  "red", "RAP":   "orange", 
                "R&B":   "purple", "LATIN": "green", "EDM":   "yellow"}


#Función para cargar los datos y guardarlos en el caché. Así solo hay que cargarlos una vez
@st.cache_data
def cargar_datos():
    df_nodes = pd.read_csv(path_nodes)
    df_nodes["node_name"] = df_nodes["track_name"] + " - " + df_nodes["track_artist"]

    df_edges = pd.read_csv(path_edges)
    G = nx.from_pandas_edgelist(df_edges, "source", "target", edge_attr=["weight"])

    features_dict = {
        row["node_name"]: tuple(row[features])
        for _, row in df_nodes.iterrows()
    }
    generos_dict = {
        row["node_name"]: row["playlist_genre"].upper()
        for _, row in df_nodes.iterrows()
    }
    return G, df_nodes, features_dict, generos_dict


#Función para ejecutar cada algoritmo
def ejecutar(algoritmo, G, origen, destino, features_dict):
    inicio = time.perf_counter()
    if algoritmo == "BFS":
        camino, coste, vertices = breadth_first_search(G, origen, destino)
    elif algoritmo == "Dijkstra":
        camino, coste, vertices = dijkstra(G, origen, destino)
    else:
        camino, coste, vertices = a_estrella(G, origen, destino, heuristica_euclidea, features_dict)
    duracion = time.perf_counter() - inicio
    return camino, coste, vertices, duracion

#Función para mostrar la(s) playlis(s) y los resultados en pantalla
def mostrar_resultado(titulo, camino, coste, vertices, duracion, generos_dict):

    st.subheader(titulo) #Título con el/los algoritmo(s) que hemos elegido: BFS, Dijkstra, A* o los tres

    if not camino: #camino == []
        st.error("No se ha encontrado camino entre las canciones seleccionadas.")
        return
    
    #Resultados con las métricas seleccionadas
    st.markdown(
        f"**Tiempo:** {duracion:.4f} s \n"
        f"**Vértices explorados:** {vertices:,} \n"
        f"**Coste de la ruta:** {coste:.4f} \n"
        f"**Saltos:** {len(camino) - 1}"
    )

    st.divider() #dividir los resultados de las métricas de la playlist

    #Playlist
    for i, cancion in enumerate(camino):
        genero = generos_dict.get(cancion, "?") #si la canción no estuviera en el diccionario, obtenemos "?"
        color = color_genero.get(genero, "gray") #si la canción tuviese un género que no está en el diccionario, 
        #le asignamos el negro
        st.markdown(
            f"<div style='padding:6px 0;'>"
            f"<span style='color:gray; font-family:monospace;'>{i:>2}.</span> "
            f"<span style='background:{color}; color:white; "
            f"padding:2px 8px; border-radius:4px; font-size:0.85em; "
            f"font-weight:600;'>{genero}</span> "
            f"{cancion}"
            f"</div>",
            unsafe_allow_html=True,
        )


#Cómo se ve la web
st.title("Playlists de evolución musical 🎵")
st.write("Selecciona una canción de origen, una canción de destino y el algotirmo que " \
          "deseas usar para generar una playlist que conecte ambas canciones. También"
          "puedes seleccionar los tres algoritmos para compararlos simultáneamente.")

#Cargar los datos
G, df_nodes, features_dict, generos_dict = cargar_datos()
canciones_disponibles = sorted(df_nodes["node_name"].unique())

#Sidebar en el que elegir los datos
with st.sidebar:
    st.header("Elige tu ruta")

    origen = st.selectbox("Canción origen", canciones_disponibles, index=0)
    destino = st.selectbox("Canción destino", canciones_disponibles, index=1)
    modo = st.radio("Algoritmo", ["BFS", "Dijkstra", "A*", "Comparar los tres"], index=3)

    boton = st.button("Generar playlist", type="primary")

#pantalla principal
if not boton:
    st.info("Configura los datos en la barra lateral y pulsa "
            "**Generar playlist**.")
elif origen == destino:
    st.warning("La canción de origen y destino son la misma.")
elif origen not in G.nodes() or destino not in G.nodes():
    st.error("Alguna de las canciones no se encuentra en el grafo.")
else:
    if modo == "Comparar los tres":
        col_bfs, col_dij, col_a = st.columns(3)
        with col_bfs:
            resultado = ejecutar("BFS", G, origen, destino, features_dict)
            mostrar_resultado("BFS", *resultado, generos_dict) #*resultado para desempaquetar
        with col_dij:
            resultado = ejecutar("Dijkstra", G, origen, destino, features_dict)
            mostrar_resultado("Dijkstra", *resultado, generos_dict)
        with col_a:
            resultado = ejecutar("A*", G, origen, destino, features_dict)
            mostrar_resultado("A*", *resultado, generos_dict)
    else:
        camino, coste, vertices, duracion = ejecutar(modo, G, origen, destino, features_dict)
        mostrar_resultado( f"Playlist generada por {modo}", camino, coste, vertices, duracion, generos_dict)