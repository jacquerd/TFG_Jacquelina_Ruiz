import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Datos de la Tabla 5.5
datos = pd.DataFrame({
    'Caso':      ['Caso 1']*3 + ['Caso 2']*3 + ['Caso 3']*3 + ['Caso 4']*3,
    'Algoritmo': ['BFS', 'Dijkstra', 'A*'] * 4,
    'Tiempo (s)':            [0.00, 0.01, 0.01, 0.01, 0.08, 0.01,
                              0.01, 0.07, 0.02, 0.01, 0.09, 0.01],
    'Vértices explorados':   [236, 296, 14, 11633, 10854, 488,
                              10282, 10499, 783, 7417, 11352, 603],
    'Coste de la ruta':      [4.8810, 3.4649, 3.4649, 7.4189, 5.8642, 5.8642,
                              10.6151, 6.0648, 6.0648, 8.2295, 7.5337, 7.5337],
    'Saltos':                [4, 4, 4, 8, 9, 9, 8, 10, 10, 8, 11, 11]
})

sns.set_style("whitegrid")
colores = {'BFS': "lightblue", 'Dijkstra': "pink", 'A*': "yellow"}
metricas = ['Tiempo (s)', 'Vértices explorados', 'Coste de la ruta', 'Saltos']

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for ax, metrica in zip(axes.flatten(), metricas):
    sns.barplot(data=datos, x='Caso', y=metrica, hue='Algoritmo',
                palette=colores, ax=ax)
    ax.set_title(metrica)
    ax.set_xlabel('')
    if metrica == 'Vértices explorados': #los vértices explorados los ponemos en escala logarítimica porque A*
        ax.set_yscale('log')             #explora muy pocos vértices en comparación con BFS y Dijkstra

plt.tight_layout()
plt.savefig('grafica_comparativa.png', bbox_inches='tight')
plt.show()