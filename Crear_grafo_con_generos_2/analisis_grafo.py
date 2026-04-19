import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns


df_edges = pd.read_csv('dataset_final_graph2.csv')

G = nx.from_pandas_edgelist(df_edges, 'source', 'target', ['weight', 'source_genre', 'target_genre'])

n_nodos = G.number_of_nodes()
n_aristas = G.number_of_edges()

print("Información sobre el grafo:")
print(f"En total hay {n_nodos} canciones (nodos)")
print(f"En total hay {n_aristas} conexiones (aristas)")

#1. Análisis de grados
grados = [deg for node, deg in G.degree()]
media_grados = sum(grados) / n_nodos

print(f"Grado Medio: {media_grados:.2f}")
print(f"Grado Máximo: {max(grados)} (Canción súper conectada)")
print(f"Grado Mínimo: {min(grados)} (Canción periférica) \n")

#2. Análisis de pesos
pesos_naturales = df_edges[df_edges['weight'] < 1.0]
pesos_penalizados = df_edges[(df_edges['weight'] >= 1.0) & (df_edges['weight'] < 5.0)]
pesos_rescate = df_edges[df_edges['weight'] >= 5.0]

print("Distribución de los costes de las conexiones")
print(f"Conexiones naturales (Sin penalización): {len(pesos_naturales)}")
print(f"Conexiones con penalización (Penalización x2): {len(pesos_penalizados)}")
print(f"Conexiones de rescate (Penalización x10): {len(pesos_rescate)}")

#3. Histograma con los pesos
plt.figure(figsize=(10, 6))

sns.histplot(df_edges['weight'], bins=50, kde=True, color = 'blue')
plt.title('Distribución de Pesos')
plt.xlabel('Peso de la arista (Distancia euclídea + Penalización)')
plt.ylabel('Cantidad de Conexiones')
plt.grid(axis='y', alpha=0.3)

nombre_imagen = 'grafica_pesos.png'
plt.savefig(nombre_imagen, dpi=300, bbox_inches='tight')

#4. Histograma con los grados
plt.clf() 
plt.figure(figsize=(10, 6))

#discrete=True porque el número de conexiones son números enteros
sns.histplot(grados, discrete=True, color='blue', alpha=0.8)

#linea roja indicando la media
plt.axvline(x=media_grados, color='red', linewidth=2, label=f'Media ({media_grados:.2f})')

plt.title('Distribución de Conexiones por Canción (Grado de los Nodos)')
plt.xlabel('Número de Conexiones (Grado)')
plt.ylabel('Cantidad de Canciones')

plt.legend() 
plt.grid(axis='y', alpha=0.3)

nombre_imagen_grados = 'grafica_grados.png'
plt.savefig(nombre_imagen_grados, dpi=300, bbox_inches='tight')

plt.close()
