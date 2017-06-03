import pandas as pd


class Graph:
    def __init__(self, vertices=[], edges=[]):
        '''
        Português: Constrói um objeto Graph. Se houver um vértice ou aresta inválido(a), uma exceção é chamada
        :param vertices: Uma lista com os vértices do grafo.
        :param edges: Uma lista com as arestas no formato nome(A-B), sendo A e B vértices válidos'''

        self.separator = '-'
        self.vertices = vertices
        self.edges = edges

        for vertix in vertices:
            if not self.checkvertix(vertix):
                raise ValueError("Invalid Vertix: " + vertix)

        for edge in edges:
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
        if edge[:edge.index(self.separator)] not in self.vertices \
                or edge[edge.index(self.separator) + 1:] not in self.vertices:
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

    def __str__(self):
        '''Converte o grafo em um DataFrame para melhor exibição'''
        df = pd.DataFrame(self.generatematrix(), index=self.vertices, columns=self.vertices)
        return str(df)


grafo = Graph(["A", "Bola", "C"], ["A-C", "Bola-C", "A-Bola", "C-Bola", "C-Bola"])
print(grafo)
