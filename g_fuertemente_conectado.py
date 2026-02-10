import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_nodes_from([1,2,3,4,5])

G.add_edges_from([(1,2),(1,4),(1,5),
                  (2,1),(2,3),(2,5),
                  (3,2),(3,4),(4,1),
                  (4,3),(5,1),(5,2)])

G2 = nx.DiGraph()

G2.add_nodes_from([1,2,3,4,5])

G2.add_edges_from([(1,2),(1,4),(1,5),
                  (2,1),(2,5),(2,3),
                  (3,4),(4,3),(5,1),(5,2)])

def dfs(graph, start_vertex):
    # Inicializar la pila vacía S
    S = []

    # Para cada vértice de G: status(v)=1
    # 1: no procesado, 2: en pila, 3: procesado
    status = {node:1 for node in graph.nodes()}

    #status(a)=2, meterlo en la pila
    status[start_vertex] = 2
    S.append(start_vertex)

    order_of_visit=[]

    while len(S)>0:
        #Cogemos un vértice x de la pila S
        x = S.pop()

        #Marcamos al vértice x como procesado
        status[x] = 3
        order_of_visit.append(x)

        #Obtenemos los vecinos de x
        neighbors = list(graph.neighbors(x))

        for j in neighbors:
            if status[j] ==1: #j es un vertice no procesado
                status[j] = 2 #Marcamos al vértice j como procesado
                S.append(j) #Metemos al vértice j en la pila S
    return order_of_visit

def comprobar_fuertem_conectado(graph):
    n = graph.number_of_nodes()
    #hacemos DFS con cada vértice y comprobamos si la salida que obtenemos es un árbol que 
    #contiene a todos los vértices de grafo
    for u in graph.nodes():
        sol = dfs(graph,u)
        if len(sol)!=n:
            return False
    return True

#Solución G
solucion = comprobar_fuertem_conectado(G)
if solucion:
    print("G es un grafo dirigido fuertemente conectado")
    titulo = "Grafo G fuertemente conectado"
else: 
    print("G es un grafo dirigido pero NO fuertemente conectado")
    titulo = "Grafo G NO fuertemente conectado"

#Solución G2
solucion2 = comprobar_fuertem_conectado(G2)
if solucion2:
    print("G2 es un grafo dirigido fuertemente conectado")
    titulo2 = "Grafo G2 fuertemente conectado"
else: 
    print("G2 es un grafo dirigido pero NO fuertemente conectado")
    titulo2 = "Grafo G2 NO fuertemente conectado"

#Dibujar G
#tamaño total de la "hoja"
plt.figure(figsize=(10,6))

#dividimos la hoja y pintamos en el lado izquierdo
plt.subplot(1,2,1)

pos = nx.circular_layout(G)

#dibujamos G

#dibujar nodos y etiquetas
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=300)
nx.draw_networkx_labels(G, pos)

nx.draw_networkx_edges(G, pos, edge_color='blue', arrows=True,connectionstyle='arc3, rad=0.1')

plt.title(titulo)

#pasamos al lado derecho
plt.subplot(1,2,2)
pos2 = nx.circular_layout(G2)

#dibujamos G2
nx.draw_networkx_nodes(G2, pos2, node_color='lightpink', node_size=300)
nx.draw_networkx_labels(G2, pos2)

nx.draw_networkx_edges(G2, pos2, edge_color='pink', arrows=True, connectionstyle='arc3, rad=0.1')

plt.title(titulo2)

plt.show()