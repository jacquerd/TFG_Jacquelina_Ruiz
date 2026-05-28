# Algoritmos de búsqueda en grafos: Generación de playlists de evolución musical

Trabajo de Fin de Grado del Grado en Matemáticas.
Departamento de Ciencias de la Computación e Inteligencia Artificial, Universidad de Sevilla.

- **Autora**: Jacquelina Ruiz Dontsova
- **Directores**: Antonio Ramírez de Arellano Marrero y Andrés Nicolás Uranga Limón

Este proyecto consiste en la creación de un modelo para crear playlists de transiciones coherentes entre dos canciones dadas. El problema se reformula como un problema del camino más corto en un grafo no dirigido y ponderado en el que:
- los **vértices** son canciones
- las **aristas** se crean usando el algoritmo de k-Nearest Neighbors (k-NN) y ciertas reglas de compatibilidades de géneros
- los **pesos** de las aristas miden la disimilitud entre canciones

Además, este proyecto implementa y compara tres algoritmos de búsqueda en grafos (BFS, Dijkstra y A*), con los que se crean las playlists buscadas.

Para finalizar, el proyecto incluye una aplicación interactiva creada con la librería Streamlit, para visualizar las playlists generadas y comparar los algoritmos entre dos canciones cualesquiera del grafo.


## Requisitos

Para ejecutar este proyecto, asegúrese de tener instaladas las siguientes librerías de Python:
- **pandas**: Manipulación y limpieza de datos.
- **scikit-learn**: Implementación de k-NN y escalado de características.
- **networkx**: Construcción y trabajo con el grafo y análisis de su estructura.
- **matplotlib** y **seaborn**: Generación de gráficas.
- **streamlit**: Creación de la aplicación interactiva.

Puede instalar todas las dependencias necesarias ejecutando:

```bash
pip install pandas scikit-learn networkx matplotlib seaborn streamlit
```


## Estructura del repositorio

```
TFG/
├── README.md
│
├── Crear_grafo/                         # Versión inicial sin géneros (descartada)
│   ├── canciones.csv
│   ├── cargar_datos.py
│   ├── crear_grafo_conexo.py
│   └── ...
│
├── Crear_grafo_con_generos/             # Versión intermedia con géneros (descartada)
│   ├── dataset_generos.csv
│   ├── cargar_datos_con_generos.py
│   └── crear_grafo_conexo_generos.py
│
├── Crear_grafo_con_generos_2/           # Versión final (la que se usa en el TFG, Capítulo 3)
│   ├── spotify_songs.csv                # Dataset original (obtenido de Kaggle)
│   ├── cargar_datos_genero2.py          # Preprocesamiento + estandarización
│   ├── crear_grafo_conexo_generos2.py   # Construcción del grafo con k-NN y restricciones de género
│   ├── analisis_grafo.py                # Estadísticas y figuras
│   ├── dataset_procesado_generos2.csv   # Canciones procesadas (vértices)
│   ├── dataset_final_graph2.csv         # Lista de aristas (grafo)
│   ├── grafica_grados.png
│   └── grafica_pesos.png
│
├── Algoritmos/                          # Implementaciones de los algoritmos (Capítulo 4)
│   ├── bfs.py                           # BFS — primera versión
│   ├── bfs_mejorado.py                  # BFS — segunda versión
│   ├── bfs_mejorado_final.py            # BFS — versión final
│   ├── dijkstra.py                      # Dijkstra — primera versión (array)
│   ├── dijkstra_optimizado.py           # Dijkstra — segunda versión (heapq)
│   └──  A_estrella.py                    # A* con heurística euclídea
│ 
├── Comparativas/                        # Scripts del Capítulo 5
│   ├── distancia_canciones.py
│   ├── dijkstra_vs_bfs.py
│   ├── dijkstra_vs_a_estrella.py
│   ├── dataset_procesado_generos2.csv
│   └── dataset_final_graph2.csv
│
└── Streamlit/                           # Aplicación interactiva
    ├── aplicacion_interactiva.py        # Interfaz
    ├── algoritmos.py                    # Versiones finales de BFS/Dijkstra/A*
    ├── dataset_procesado_generos2.csv
    └── dataset_final_graph2.csv
```


## Cómo reproducir los resultados

### 1. Construir el grafo (Capítulo 3)

Desde la carpeta `Crear_grafo_con_generos_2/`:

```bash
cd Crear_grafo_con_generos_2
python cargar_datos_genero2.py            # Preprocesa el dataset
python crear_grafo_conexo_generos2.py     # Construye el grafo con k-NN
python analisis_grafo.py                  # Genera las gráficas del Capítulo 3
```

Esto produce `dataset_procesado_generos2.csv` (vértices) y `dataset_final_graph2.csv` (aristas).

### 2. Ejecutar los algoritmos (Capítulo 4)

Las distintas versiones de cada algoritmo están en `Algoritmos/`. Pueden ejecutarse de forma independiente sobre un par de canciones origen-destino.

### 3. Generar las comparativas (Capítulo 5)

Desde la carpeta `Comparativas/`:

```bash
cd Comparativas
python distancia_canciones.py             # Distancia entre pares
python dijkstra_vs_bfs.py                 # Comparación BFS vs Dijkstra
python dijkstra_vs_a_estrella.py          # Comparación Dijkstra vs A*
```

### 4. Lanzar la aplicación interactiva (Sección 5.7)

Desde la carpeta `Streamlit/`:

```bash
cd Streamlit
streamlit run aplicacion_interactiva.py
```

Se abrirá automáticamente una pestaña en el navegador con la interfaz. El usuario podrá:

- Elegir una canción de origen y otra de destino entre las 26229 disponibles.
- Seleccionar el algoritmo a ejecutar: BFS, Dijkstra, A* o los tres simultáneamente.
- Ver la playlist generada junto con las métricas (tiempo, vértices explorados, coste, saltos).

---

## Dataset

El dataset utilizado es **30 000 Spotify Songs**, disponible en Kaggle:
<https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs>

Contiene 32834 canciones con sus características, su género y subgénero.


## Licencia y uso

El código de este repositorio se publica con fines académicos en el marco de un Trabajo de Fin de Grado. Para cualquier reutilización, por favor cita el trabajo:

> Ruiz Dontsova, J. *Algoritmos de búsqueda en grafos: Generación de playlists de evolución musical*. Trabajo de Fin de Grado, Grado en Matemáticas, Universidad de Sevilla, 2026.
