from graph import Graph

# Grafo do roteiro
g = Graph([('J', ['C']), ('C', ['J', 'E', 'P', 'M', 'T']), ('E', ['C']), ('P', ['C']), ('M', ['C', 'T']),
           ('T', ['C', 'Z', 'M']), ('Z', ['T'])])

# Grafo desconexo

# Grafo com ciclo triangular
# g = Graph([('a',['b','c']),('b',['c','a']),('c',['b','a'])])

# Grafo com ciclo quadrado
# g = Graph([('a', ['b', 'd']), ('b', ['a', 'c']), ('c', ['b', 'd']), ('d', ['a', 'c'])])

# Grafo com ciclo de 5 vertices
# g = Graph([('a', ['b', 'e']), ('b', ['a', 'c']), ('c', ['b', 'd']), ('d', ['c', 'e']),('e',['d','a'])])

# Questoes

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
