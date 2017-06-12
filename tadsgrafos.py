from pandas import DataFrame
from collections import OrderedDict

separator = '-'


class Graph:
    def __init__(self, vertices):
        self.vertices = OrderedDict(vertices)

    def __str__(self):
        '''Converte o grafo em um DataFrame para melhor exibição'''
        df = DataFrame(self.genmatrix(), index=self.vertices, columns=self.vertices)
        return str(df)

    def nonadjacent(self):
        pairs = []
        for vertex in self.vertices:
            for aux_vertex in list(set(self.vertices) - set(vertex)):
                if vertex not in list(set(self.vertices) - set(vertex)):
                    if aux_vertex + separator + vertex not in pairs:
                        pairs.append(vertex + separator + aux_vertex)
        return pairs

    def getedges(self, vertex=None):
        edges = []
        if vertex == None:
            for head in self.vertices:
                for tail in self.vertices[head]:
                    if tail + separator + str(head) not in edges:
                        edges.append(str(head) + separator + tail)
        else:
            for tail in self.vertices[vertex]:
                if tail + separator + str(vertex) not in edges:
                    edges.append(str(vertex) + separator + tail)

        return edges

    def genmatrix(self, hide=True):
        matrix = []

        for v in self.vertices:
            matrix.append([0] * len(self.vertices))

        for vertex in self.vertices:
            for connection in self.vertices[vertex]:
                x = list(self.vertices).index(vertex)
                y = list(self.vertices).index(connection)
                matrix[x][y] = 1

        if hide == True:
            for i in range(len(matrix)):
                for j in range(len(matrix)):
                    if type(matrix[i][j]) != str:
                        matrix[i][j] = str(matrix[i][j])
                    if i > j:
                        matrix[i][j] = '-'

        return matrix

    def degree(self, vertex):
        return len(self.vertices[vertex])

    def getcycle(self):
        cycle = []

        def busca(vertex):
            def checkcycle():
                for v in cycle:
                    if cycle.count(v) > 1:
                        return True

            if checkcycle():
                return cycle

            if vertex in cycle:
                if (len(cycle) - cycle.index(vertex)) > 2:
                    cycle.append(vertex)
                    return cycle
                else:
                    return cycle

            cycle.append(vertex)

            if len(self.vertices[vertex]) <= 1:
                cycle.pop()
                return cycle
            for v in self.vertices[vertex]:
                busca(v)

        for v in self.vertices:
            busca(v)

        return cycle

    def iscomplete(self):
        for vertex in self.vertices:
            if len(self.vertices[vertex]) != len(self.vertices):
                return False
            for aux_vertex in self.vertices:
                if vertex not in self.vertices[aux_vertex]:
                    return False
        return True

    def pathbetween(self, head, tail):
        self.head = head
        self.tail = tail

        path = [head]

        def percorrer(head):
            if self.tail in path:
                return path
            for vertex in list(set(self.vertices[head]) - set(path)):
                if vertex not in path:
                    path.append(str(vertex))
                    if self.tail in path:
                        return path
                adjacencies = list(set(self.vertices[vertex]) - set(path))
                if len(adjacencies) > 0:
                    for adj in adjacencies:
                        if self.tail in path:
                            return path
                        percorrer(adj)
            return path

        percorrer(self.head)
        return path

    def isconex(self):
        for vertex in self.vertices:
            if not self.vertices[vertex]:
                return False
            for aux_vertex in self.vertices:
                if not self.pathbetween(vertex, aux_vertex):
                    return False
        return True

    def getpath(self, size=0):
        path = []

        def search(v):
            if len(path) == size:
                return path

            if not self.vertices[v]:
                return path

            if v not in path:
                path.append(str(v))
                if len(path) == size:
                    return path
            else:
                return

            adjacencies = list(set(self.vertices[v]) - set(path))
            if len(adjacencies) > 0:
                for adj in adjacencies:
                    search(adj)
            else:
                path.pop()
            return path

        for v in self.vertices:
            search(v)
        if len(path) != size:
            return False
        else:
            return path


# Grafo do roteiro
g = Graph([('J', ['C']), ('C', ['J', 'E', 'P', 'M', 'T']), ('E', ['C']), ('P', ['C']), ('M', ['C', 'T']),
           ('T', ['C', 'Z', 'M']), ('Z', ['T'])])

# Grafo com ciclo quadrado
# g = Graph([('a', ['b', 'e']), ('b', ['a', 'c']), ('c', ['b', 'd']), ('d', ['c', 'e']),('e',['d','a'])])

# 3.a: Encontre todos os pares de vértices não adjacentes.
print(g.nonadjacent())
# 3.d: Qual o grau do vértice C?
print(g.degree('c'))
# 3.e: Quais arestas incidem no vertice M?
print(g.getedges('a'))
# 3.f: Esse grafo é completo?
print(g.iscomplete())
# 3.g: (DESAFIO) Encontre um ciclo, se houver.
print(g.getcycle())
# 3.h: Encontre um caminho de comprimento 4, se houver.
print(g.getpath(4))
# 3.i: (DESAFIO) Esse grafo é conexo?
print(g.isconex())
