class Graph:
    def __init__(self, vertices=[], edges={}):
        '''
        Português: Constrói um objeto Graph. Se houver um vértice ou aresta inválido(a), uma exceção é chamada
        :param vertices: Uma lista com os vértices do grafo. Os vértices não devem conter mais que uma letra
        (para manter a formatação).
        :param edges: Um dicionário com as arestas no formato nome(A-B), sendo A e B vértices válidos'''

        self.separator = '-'
        self.vertices = vertices
        self.edges = edges

        for vertix in vertices:
            if not self.checkvertix(vertix):
                raise ValueError("Invalid Vertix: " + vertix)

        for edge in edges.values():
            if not self.checkedge(edge):
                raise ValueError("Invalid edge: " + edge)

    def getedges(self):
        '''Retorna as arestas'''
        return self.edges

    def getvertices(self):
        '''Retorna os vértices'''
        return self.vertices

    def checkedge(self, edge):
        '''Checa se uma aresta é válida'''
        if edge.count(self.separator) != 1:
            return False
        if edge.startswith(self.separator) or edge.endswith(self.separator):
            return False
        if edge[0] not in self.vertices or edge[-1] not in self.vertices:
            return False
        return True

    def checkvertix(self, vertix):
        '''Checa se um vértice é válido'''
        if self.separator in vertix or vertix == "":
            return False
        return True

    def generatematrix(self):
        '''Gera a matriz que representa o grafo'''
        matrix = []
        for v in self.vertices:
            matrix.append([0] * len(self.vertices))

        for vertix in self.vertices:
            for aux_vertix in self.vertices:
                comb = vertix + self.separator + aux_vertix
                x = self.vertices.index(vertix)
                y = self.vertices.index(aux_vertix)
                if comb in self.edges.values():
                    matrix[x][y] += list(self.edges.values()).count(comb)
                    if comb != comb[::-1]:
                        matrix[x][y] += list(self.edges.values()).count(comb[::-1])

        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if type(matrix[i][j]) != str:
                    matrix[i][j] = str(matrix[i][j])
                if i > j:
                    matrix[i][j] = '-'

        return matrix

    def __str__(self):
        matrix = self.generatematrix()
        out = '     '
        for vertix in self.vertices:
            out += vertix + '    '

        out += '\n'

        for line in matrix:
            out += self.vertices[matrix.index(line)] + '  ' + str(line) + '\n'
        return out


grafo = Graph(["A", "B", "C", "D", "E"], {"a1": "A-C", "a2": "B-B", "a3": "A-A", "a4": "A-B"})
print(grafo)
