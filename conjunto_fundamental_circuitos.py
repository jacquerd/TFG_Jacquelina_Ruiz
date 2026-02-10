import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from([1,2,3,4,5,6])

G.add_edges_from([(1,3),(1,4),(1,5),(1,6),
                  (2,3),(2,6),(3,4),(3,5),
                  (4,5),(5,6)])

def cj_fundamental_circuitos(graph):
    graph2 = graph.copy() #hacemos una copia para no modificar el grafo original
    
    aristas_T = []
    circuitos = []

    aristas_procesadas = set()

    u = list(graph.nodes())[0]
    T = {u} #T: conjunto de vértices del árbol de expansión

    arbol = nx.Graph()
    arbol.add_node(u)

    while True:
        #Calculamos T∩V(G)
        interseccion = [v for v in T if v in graph2.nodes()]

        if interseccion == []:
            break

        x = interseccion[0]

        vecinos_x = list(graph2.neighbors(x))

        arista_nueva = False

        for j in vecinos_x:
            arista = tuple(sorted((x,j))) #para que siempre salga ordenada y no repetirla

            if arista in aristas_procesadas:
                continue

            aristas_procesadas.add(arista)
            arista_nueva = True

            if j in T:
                ruta = nx.shortest_path(arbol,x,j)
                circuitos.append(ruta + [x])
            else : 
                arbol.add_edge(*arista) #tenemos que desempaquetar la tupla
                aristas_T.append(arista)
                T.add(j)

                graph2.remove_edge(*arista)

                if graph2.degree(x) == 0: graph2.remove_node(x)
                if graph2.degree(j) == 0: graph2.remove_node(j)

        if not arista_nueva and x in graph2:
            #si ya he revisado x y no había aristas nuevas, lo elimino de 
            #la lista de nodos pendientes por revisar
            graph2.remove_node(x)

    return aristas_T, circuitos

#Ejecución
aristas, circuitos = cj_fundamental_circuitos(G)

print("Áristas árbol:", aristas)
print("Circuitos:", circuitos)

#Visualización
plt.figure(figsize=(10,6))

pos= nx.circular_layout(G)

nx.draw_networkx_nodes(G,pos,node_color='pink',node_size=300)

nx.draw_networkx_edges(G,pos,edge_color='pink')

nx.draw_networkx_labels(G, pos)

#marcamos con verde el árbol de expansión

nx.draw_networkx_edges(G,pos,edgelist=aristas,edge_color='green',width=2)

#marcamos en rojo lar aristas que forman los ciruitos
todas_aristas = set(tuple(sorted(e)) for e in G.edges())
set_arbol = set(aristas)
aristas_circuitos = list(todas_aristas - set_arbol)

nx.draw_networkx_edges(G,pos,edgelist=aristas_circuitos,edge_color='red',width=2)

plt.title('Grafo G con el árbol en verde y las aristas que forman circuitos en rojo')

plt.show()