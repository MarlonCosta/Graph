from graph import Graph

g = Graph([('J', ['C']), ('C', ['J', 'E', 'P', 'M', 'T']), ('E', ['C']), ('P', ['C']), ('M', ['C', 'T']),
           ('T', ['C', 'Z', 'M']), ('Z', ['T'])])

print('3.a: Encontre todos os pares de vértices não adjacentes.')
print(g.nonadjacent())
print('3.d: Qual o grau do vértice C?')
print(g.degree('C'))
print('3.e: Quais arestas incidem no vertice M?')
print(g.getedges('M'))
print('3.f: Esse grafo é completo?')
print(g.iscomplete())
print(
    '3.g: (DESAFIO) Encontre um ciclo, se houver (Retorne a sequência de vértices e arestas do ciclo ou False se não houver ciclo)')
print(g.getcycle())
print(
    '3.h: (DESAFIO) Encontre um caminho de comprimento 4, se houver (Faça uma função genérica que encontre um caminho de tamanho arbitrário)')
print(g.getpath(4))
print('3.i: (DESAFIO) Esse grafo é conexo?')
print(g.isconnected())
