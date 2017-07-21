from graph import Graph
'''
grafos_teste = [
    Graph([('a', []), ('b', []), ('c', []), ('d', []), ('e', [])]),  # Grafo sem arestas
    Graph([('a', ['b', 'e']), ('b', ['a', 'c']), ('c', ['b', 'd']), ('d', ['c', 'e']), ('e', ['d', 'a'])]),
    # Grafo circular de 5 vértices e 5 arestas
    Graph([('a', ['b']), ('b', ['a']), ('c', ['d']), ('d', ['c'])]),  # Grafo com 2 arestas desconexas
    Graph([('J', ['C']), ('C', ['J', 'E', 'P', 'M', 'T']), ('E', ['C']), ('P', ['C']), ('M', ['C', 'T']),
           # Grafo do roteiro
           ('T', ['C', 'Z', 'M']), ('Z', ['T'])]),
    Graph([('a', ['b', 'c']), ('b', ['c', 'a']), ('c', ['b', 'a'])]),  # Grafo triangular
    Graph([('a', ['b', 'c', 'd', 'e']), ('b', ['a', 'c', 'd', 'e']), ('c', ['a', 'b', 'd', 'e']),
           ('d', ['a', 'b', 'c', 'e']), ('e', ['a', 'b', 'c', 'd'])])
    # Grafo completo de 5 vértices

]
'''

grafos_teste = [
    #Grafos direcionados

    Graph([('a', ['b']), ('b', ['c']), ('c', ['d']), ('d', ['e']), ('e', ['a'])]), # Grafo circular de 5 vértices e 5 arestas
    Graph([('a', ['b']), ('b', ['c']), ('c', [])])]  # Grafo triangular

for i in range(len(grafos_teste)):

    print("Grafo-teste número %d\n" % (i + 1) + str(grafos_teste[i]))
    print("Ciclo encontrado:\n" + str(grafos_teste[i].getcycle()) + "\n")
    for j in range(6):
        print("Buscando caminho de comprimento %d\n" % j + str(grafos_teste[i].getpath(j)) + "\n")
    print("O grafo-teste número %d é conexo?\n" % (i + 1) + str(grafos_teste[i].isconnected()) + "\n\n")
