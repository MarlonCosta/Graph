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
        self.matrix = self.generatematrix()

        for vertex in vertices:
            self.checkvertex(vertex)

        for edge in edges:
            self.checkedge(edge)

    def __str__(self):
        '''Converte o grafo em um DataFrame para melhor exibição'''
        df = pd.DataFrame(self.generatematrix(), index=self.vertices, columns=self.vertices)
        return str(df)

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
            raise ValueError("Invalid edge " + edge + " vertex not found")

    def checkvertex(self, vertex):
        '''Checa se um vértice é válido'''
        if self.separator in vertex:
            raise ValueError("Invalid vertex " + vertex + ": vertex contains separator character")
        if vertex == "":
            raise ValueError("Invalid vertex: Empty value")
        for v in self.vertices:
            if self.vertices.count(v) > 1:
                raise ValueError("Invalid vertex: Two or more inputs of the same vertex " + v)

    def generatematrix(self, hide=True):
        '''Gera a matriz que representa o grafo'''
        matrix = []
        for v in self.vertices:
            matrix.append([0] * len(self.vertices))

        for vertex in self.vertices:
            for aux_vertex in self.vertices:
                comb = vertex + self.separator + aux_vertex
                rev_comb = aux_vertex + self.separator + vertex
                x = self.vertices.index(vertex)
                y = self.vertices.index(aux_vertex)
                if comb in self.edges:
                    matrix[x][y] += list(self.edges).count(comb)
                    if comb != rev_comb:
                        matrix[x][y] += list(self.edges).count(rev_comb)
        if hide == True:
            for i in range(len(matrix)):
                for j in range(len(matrix)):
                    if type(matrix[i][j]) != str:
                        matrix[i][j] = str(matrix[i][j])
                    if i > j:
                        matrix[i][j] = '-'

        return matrix

    def checkbetweenvertices(self, vertex1, vertex2):
        '''Checa a existência de uma aresta entre os 2 vértices entre os parâmetros
        :param vertex1: Primeiro vértices que compoe a aresta a ser checada
        :param vertex2: Segundo vértice que compoe a aresta a ser checada'''

        if vertex1 + "-" + vertex2 in self.edges or vertex2 + "-" + vertex1 in self.edges:
            return True
        else:
            return False

    def nonadjacentpairs(self):
        '''Retorna uma lista com os pares não adjacentes'''
        pares = []

        for line in range(len(self.matrix)):
            for column in range(len(self.matrix[line])):
                if self.matrix[line][column] == '0':
                    saida = self.vertices[line] + self.separator + self.vertices[column]
                    pares.append(saida)
        if not pares:
            return None
        return pares

    def getloops(self):
        ''' Retorna uma lista com os vértices que possuem loop (adjacentes a eles mesmos), caso existam'''
        loops = []

        for line in range(len(self.matrix)):
            for column in range(len(self.matrix[line])):
                if self.matrix[line][column] != self.separator and int(self.matrix[line][column]) > 0 and self.vertices[
                    line] == \
                        self.vertices[column]:
                    loops.append(self.vertices[line])
        if not loops:
            return None
        return loops

    def getparalleledges(self):
        '''Retorna uma lista com as arestas que tem alguma aresta paralela, caso existam'''
        parallel_edges = []

        for line in range(len(self.matrix)):
            for column in range(len(self.matrix[line])):
                if self.matrix[line][column] != self.separator:
                    if int(self.matrix[line][column]) > 1:
                        parallel_edges.append(self.vertices[line] + self.separator + self.vertices[column])
        if not parallel_edges:
            return None
        return parallel_edges

    def edgesin(self, vertex):
        '''Retorna as arestas incidentes no vértice
        :param vertex: Vértice no qual será conferida a incidência de arestas'''

        if vertex not in self.vertices:
            raise NameError("O grafo não contém o vértice inserido")

        edges = []

        for edge in self.edges:
            if vertex in edge:
                edges.append(edge)

        if not edges:
            return None
        return edges

    def degree(self, vertex):
        '''Retorna o grau do vérticie posto como parâmetro
        :param vertex: Vértice que terá seu grau calculado'''

        if vertex not in self.vertices:
            raise NameError("O grafo não contém o vértice inserido")

        degree = 0

        for edge in self.edges:
            if vertex in edge:
                degree += 1

        return degree

    def iscomplete(self):
        '''Retorna um booleano indicando se o grafo é completo'''
        for line in range(len(self.matrix)):
            for column in range(len(self.matrix[line])):
                if self.matrix[line][column] == '0':
                    return False
                else:
                    return True

    def findpath(self):
        caminho = [self.vertices[0]]

        def checkline(linha, pai):
            if self.matrix[linha].count('0') + self.matrix[linha].count('-') != len(self.matrix[linha]):
                for elem in self.matrix[linha]:
                    if elem != '-' and elem != '0':
                        caminho.append(self.vertices[self.matrix[linha].index(elem)])
                        return caminho + checkline(self.matrix[linha].index(elem), linha)
                    else:
                        continue
            return caminho

        checkline(0, 0)

        return caminho


g = Graph(['J', 'C', 'E', 'P', 'M', 'T', 'Z'], ['J-C', 'C-E', 'C-E', 'C-P', 'C-P', 'C-M', 'C-T', 'M-T', 'T-Z'])
# g = Graph(['a','b','c','d','e','f'],['a-b','b-c','a-d', 'b-e','c-e','c-f'])
print(g, '\n')
''''
print("Pares não adjacentes: ", g.nonadjacentpairs())  # Questão 3.a
print("Vértices adjacentes a si mesmos:",
      g.getloops())  # Questão 3.b (alteração: retorna os vértices onde existem loops em vez de True)
print("Arestas que possuem alguma paralela:",
      g.getparalleledges())  # Questão 3.c (alteração: retorna quais arestas tem outras arestas paralelas em vez de True)
print("Grau do vértice C:", g.degree("C"))  # Questão 3.d
print("Arestas incidentes no vértice M:", g.edgesin("M"))  # Questão 3.e
print("O grafo é completo?:", g.iscomplete())  # Questão 3.f'''
print(g.findpath())
