import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from(['A','B','C','D','E','F','G'])

G.add_edges_from([('A','B'),('A','C'),('A','D'),('A','E'),
                 ('B','C'),('C','D'),('C','G'),('D','E'),
                 ('D','G'), ('E','F'),('E','G'),('F','G')])
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

#Para hacer este algoritmo vamos a suponer que el grafo es euleriano(todos los vértices de grado par)
#si el grafo fuera semieuleriano(2 vértices de grado impar) funcionaría empezando en uno de los de grado impar
def fleury(graph):
    Gf = graph.copy()
    C = []

    v = list(Gf.nodes())[0] #como el grafo es euleriano, da igual por donde empecemos
    C.append(v)

    mf = Gf.number_of_edges()

    while mf>0 :
        #ordenamos la lista para que siempre salga el mismo resultado
        vecinos_v = sorted(list(Gf.neighbors(v)))

        for x in vecinos_v:
            u = x
            Gf.remove_edge(v,x)
            #Comprobamos si el Grafo factible sigue siendo un grafo conexo 
            nodos_totales = Gf.number_of_nodes()
            nodos_alcanzados = dephth_first_search(Gf,v)
            Gf.add_edge(v,x)
            if nodos_totales==nodos_alcanzados :
                #la arista (u,x) no es un puente, así que nos quedamos con esta
                break
        #añadimos u al cirtuito euleriano
        C.append(u)

        #eliminamos definitivamente la arista (u,v)
        Gf.remove_edge(u,v)

        mf = mf -1

        grado_v = Gf.degree(v)

        #si el vértice v se queda aislado tras eliminar la arista (u,v)=> lo quitamos del subgrafo factible

        if grado_v == 0:
            Gf.remove_node(v)
    
        v = u

    return C

#Ejecución
resultado = fleury(G)

#Visualización
plt.figure(figsize=(10,7))
pos = nx.circular_layout(G)

#dibujamos G
nx.draw_networkx_nodes(G,pos,node_color='gray')
nx.draw_networkx_edges(G,pos,edge_color='blue')
nx.draw_networkx_labels(G,pos) #nombre de los nodos

#vamos a calcular el orden que ha seguido el algoritmo de fleury
orden = {}

for i in range(len(resultado)-1):
    u = resultado[i]
    v= resultado[i+1]

    #escribimos sorted(u,v) para que si la arista es (D,A), nos salga (A,D) y no haya confusión
    edge_key = tuple(sorted((u,v)))
    orden[edge_key] = str(i+1)

#dibujamos los números de orden encima de las aristas correspondientes
nx.draw_networkx_edge_labels(G,pos,edge_labels=orden)

plt.title("Ciclo euleriano(Algoritmo de Fleury)")
plt.show()


