from pandas import DataFrame
from collections import OrderedDict


class SeparatorError(Exception):
    pass


separator = '-'


class Graph:
    def __init__(self, vertices):
        self.vertices = vertices

    def __str__(self):
        '''Converte o grafo em um DataFrame para melhor exibição'''
        df = DataFrame(self.genmatrix(), index=self.vertices, columns=self.vertices)
        return str(df)

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

    def getdegree(self, vertex):
        return len(self.vertices[vertex])

    def getpath(self, size=0):
        path = []

        def search(v):
            if len(path) == size:
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


g = Graph(OrderedDict([('J', ['C']), ('C', ['J', 'E', 'P', 'M', 'T']), ('E', ['C']), ('P', ['C']), ('M', ['C', 'T']),
                       ('T', ['C', 'Z', 'M']), ('Z', ['T'])]))
print(g.getpath(size=5))
