import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from(['A','B','C','D','E','F'])

edges_with_weights = [('A','C', 7),('A','E', 4),('A','F', 7),
                  ('B','C', 8),('B','E', 7),('B','F', 5),
                  ('B','D', 3),('C','E', 6),('F','D',4)]
G.add_weighted_edges_from(edges_with_weights)

def dephth_first_search(graph, start_vertex):
    # Inicializar la pila vacía S
    S = []

    # Para cada vértice de G: status(v)=1
    # 1: no procesado, 2: en pila, 3: procesado
    status = {node:1 for node in graph.nodes()}

    #status(a)=2, meterlo en la pila
    status[start_vertex] = 2
    S.append(start_vertex)

    visited_count = 0

    while len(S)>0:
        #Cogemos un vértice x de la pila S
        x = S.pop()

        #Marcamos al vértice x como procesado
        status[x] = 3
        visited_count += 1

        #Obtenemos los vecinos de x
        neighbors = sorted(list(graph.neighbors(x)), reverse=True)

        for j in neighbors:
            if status[j] ==1: #j es un vertice no procesado
                status[j] = 2 #Marcamos al vértice j como procesado
                S.append(j) #Metemos al vértice j en la pila S
    return visited_count

def minimum_spanning_tree(G):
    #Hacemos una copia de G
    T = G.copy()
    
    #Contamos el número de nodos
    n = T.number_of_nodes()

    #Ordenamos las aristas de G de manera decreciente 
    #respecto a su peso
    # edges(data=True) -> (u,v,diccionario_datos)
    # reverse= True porque queremos que esten ordenados de forma decreciente,
    # y Python por defecto ordena de forma ascencente 
    sorted_edges = sorted(G.edges(data=True), key = lambda x: x[2]['weight'], reverse = True)

    for u, v, data in sorted_edges:
        weight = data['weight']

        #Si T tiene n vértices y n-1 aristas -> T ya es un árbol de expansión mínimo
        if T.number_of_edges()== n-1 :
            print("T ya es un árbol de expansión mínimo")
            break

        # Eliminar arista (u,v) de T
        T.remove_edge(u,v)

        #Hacemos DFS para comprobar si T sigue siendo un grafo conexo
        nodes_visited = dephth_first_search(T, list(T.nodes())[0])
        
        #Si noDescubiertos>0 -> La arista es un puente -> La devolvemos
        if nodes_visited < n:
            T.add_edge(u,v,weight=weight)
        #Si no, T sigue conectado

    return T

#Ejectutamos el algoritmo
MST = minimum_spanning_tree(G)

#Calculamos el peso total:
total_weight = 0
for u,v,data in MST.edges(data=True):
    total_weight += data['weight']
print(f"Peso total: {total_weight}")

#Visualización

#tamaño total de la "hoja"
plt.figure(figsize=(10,5))

#dividir la hoja. pintamos en el lado izquierdo
plt.subplot(1,2,1)

#seed para que cada vez que ejecutemos el código nos salga el mismo dibujo
pos = nx.spring_layout(G, seed = 42)

#dibujamos el grafo original
nx.draw(G,pos,with_labels=True, node_color='pink')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G,pos, edge_labels= labels)
plt.title('Grafo G original')

#pasamos al lado derecho
plt.subplot(1,2,2)

#dibujamos el grafo T, resultado de MST
nx.draw(MST, pos, with_labels=True, node_color ='green')
labels_mst = nx.get_edge_attributes(MST, 'weight')
nx.draw_networkx_edge_labels(MST, pos, edge_labels = labels_mst)
plt.title('Grafo MST(Borrado inverso)')

plt.show()