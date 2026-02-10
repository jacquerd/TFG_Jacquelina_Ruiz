import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from(['a','b','c','d','e','f','g','h','i'])

G.add_edges_from([('a','b'),('a','c'),('b','c'),
                  ('c','d'),('c','e'),('d','f'),
                  ('e','f'),('f','g'),('g','h'),('g','i')])


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


def puntos_de_corte_y_puentes(graph):
    C = []
    B = []

    #escribimos tuple(sorted(edge)) para que la arista (2,1) sea igual que la (1,2) (ya que, aunque el
    #grafo es no dirigido, esto Python no lo sabe automáticamente)
    #además debemos escribir tuple(...) porque sorted((2,1)) nos daría [1,2] y en python no podemos usar 
    #listas como claves de un diccionario
    b = {tuple(sorted(edge)): 0 for edge in graph.edges()}

    n = graph.number_of_nodes()

    for i in graph.nodes():
        G2 = graph.copy()
        G2.remove_node(i)

        v_start = list(G2.nodes())[0] #vértice con el que empezamos DFS

        if len(dfs(G2,v_start)) < n-1:
            #i es un punto de corte
            C.append(i)

            aristas_incidentes_i = list(graph.edges(i))

            for u,v in aristas_incidentes_i:
                arista = tuple(sorted((u,v)))
                b[arista] +=1
                if b[arista]==2:
                    #(u,v) es un puente
                    B.append(arista)

        if graph.degree(i) == 1:
            arista_incidente = list(graph.edges(i))[0]
            arista_incidente_ordenada = tuple(sorted(arista_incidente))
            if arista_incidente_ordenada not in B: 
                #comprobamos que la arista no está en B para evitar posibles repeticiones
                B.append(arista_incidente_ordenada)
    return C,B

#ejecución
solucion = puntos_de_corte_y_puentes(G)
print(solucion)

#visualización
plt.figure(figsize=(10,6))

pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G,pos, node_color='pink',node_size=200)

nx.draw_networkx_edges(G,pos,edge_color='pink')

nx.draw_networkx_labels(G, pos)

#señalamos los puntos de corte
nx.draw_networkx_nodes(G,pos,nodelist=solucion[0], node_color='red',node_size=300)

#señalamos los puentes
nx.draw_networkx_edges(G, pos, edgelist=solucion[1], edge_color='green', width=2)

plt.title('Grafo G con puntos de corte en rojo y puentes en verde')

plt.show()



    