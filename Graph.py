import pandas as pd


class Graph:
    def __init__(self, vertices=[], edges=[]):
        '''
        Constrói um objeto Graph. Se houver um vértice ou aresta inválido(a), uma exceção é chamada
        :param vertices: Uma lista com os vértices do grafo.
        :param edges: Uma lista com as arestas no formato nome(A-B), sendo A e B vértices válidos'''

        self.separator = '-'
        self.vertices = vertices
        self.edges = edges

        for vertix in vertices:
            self.checkvertix(vertix)

        for edge in edges:
            self.checkedge(edge)

    def getedges(self):
        '''Retorna as arestas'''
        return self.edges

    def getvertices(self):
        '''Retorna os vértices'''
        return self.vertices

    def checkedge(self, edge):
        '''Checa se uma aresta é válida'''
        if edge.count(self.separator) != 1:
            raise ValueError("Invalid edge " + edge + ": more than one separator on the edge")

        if edge.startswith(self.separator) or edge.endswith(self.separator):
            raise ValueError("Invalid edge " + edge + ": separator character at the beggining or the end of the edge")

        if edge[:edge.index(self.separator)] not in self.vertices \
                or edge[edge.index(self.separator) + 1:] not in self.vertices:
            raise ValueError("Invalid edge " + edge + " vertix not found")

    def checkvertix(self, vertix):
        '''Checa se um vértice é válido'''
        if self.separator in vertix:
            raise ValueError("Invalid Vertix " + vertix + ": vertix contains separator character")
        if vertix == "":
            raise ValueError("Invalid Vertix: Empty value")
        for v in self.vertices:
            if self.vertices.count(v) > 1:
                raise ValueError("Invalid Vertix: Two or more inputs of the same vertix " + v)

    def generatematrix(self):
        '''Gera a matriz que representa o grafo'''
        matrix = []
        for v in self.vertices:
            matrix.append([0] * len(self.vertices))

        for vertix in self.vertices:
            for aux_vertix in self.vertices:
                comb = vertix + self.separator + aux_vertix
                rev_comb = aux_vertix + self.separator + vertix
                x = self.vertices.index(vertix)
                y = self.vertices.index(aux_vertix)
                if comb in self.edges:
                    matrix[x][y] += list(self.edges).count(comb)
                    if comb != rev_comb:
                        matrix[x][y] += list(self.edges).count(rev_comb)

        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if type(matrix[i][j]) != str:
                    matrix[i][j] = str(matrix[i][j])
                if i > j:
                    matrix[i][j] = '-'

        return matrix

    def checkbetweenvertices(self, vertix1, vertix2):

        if vertix1 + "-" + vertix2 in self.edges or vertix2 + "-" + vertix1 in self.edges:
            return True
        else:
            return False

    def nonadjacentpairs(self):
        pares = []
        matrix = self.generatematrix()
        for line in range(len(matrix)):
            for column in range(len(matrix[line])):
                if matrix[line][column] == 0:
                    saida = self.vertices[matrix.index(line)] + self.separator + self.vertices[matrix.index(column)]
                    pares.append(saida)
        return pares


    def __str__(self):
        '''Converte o grafo em um DataFrame para melhor exibição'''
        df = pd.DataFrame(self.generatematrix(), index=self.vertices, columns=self.vertices)
        return str(df)


g = Graph(['J', 'C', 'E', 'P', 'M', 'T', 'Z'], ['J-C', 'C-E', 'C-E', 'C-P', 'C-P', 'C-M', 'C-T', 'M-T', 'T-Z'])
print(g)
print(g.nonadjacentpairs())
