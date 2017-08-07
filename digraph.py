from pandas import DataFrame


class Edge:
    def __init__(self, head, tail, weight=1):
        self.head = head
        self.tail = tail
        self.weight = weight

    def __repr__(self):
        return self.head + "-" + self.tail + ': ' + str(self.weight)

    def get(self):
        return [self.head, self.tail, self.weight]


class DiGraph:
    def __init__(self, edges):
        self.vertices = []
        self.edges = edges
        self.matrix = []

        # Transforma as arestas inseridas em objetos Edge
        for edge in self.edges:
            self.importedge(edge)

        self.matrix = self.genmatrix()

    def __str__(self):
        return str(DataFrame(self.matrix, index=self.vertices, columns=self.vertices))

    def genmatrix(self):
        matrix = []
        for v in self.vertices:
            matrix.append([0] * len(self.vertices))

        # Preenche a matriz
        for edge in self.edges:
            x = list(self.vertices).index(edge.head)
            y = list(self.vertices).index(edge.tail)
            matrix[x][y] = edge.weight

        return matrix

    def addedge(self, edge):
        assert isinstance(edge, Edge)
        self.edges.append(edge)
        self.genmatrix()

    def importedge(self, edge):

        self.check_edge(edge)

        if edge[0] not in self.vertices:
            self.vertices.append(edge[0])
        if edge[1] not in self.vertices:
            self.vertices.append(edge[1])

        self.edges[self.edges.index(edge)] = Edge(*edge)

    def removeedge(self, edge):
        if type(edge) == str:
            edges = self.edgestostr()
            for e in edges:
                if edge == str(e):
                    self.edges.remove(self.edges[edges.index(e)])

        if type(edge) == list:
            edges = self.edgestolist()
            for e in edges:
                if edge[0:2] == e[0:2]:
                    self.edges.remove(self.edges[edges.index(e)])

        self.matrix = self.genmatrix()
        return

    def check_edge(self, edge):
        if len(edge) == 3:
            if not (type(edge[0]) == str and type(edge[1]) == str and (type(edge[2]) == int or type(edge[2] == float))):
                raise ValueError("Edge incorrectly defined")
        elif len(edge) == 2:
            if not (type(edge[0]) == str and type(edge[1]) == str):
                raise ValueError("Edge incorrectly defined")
        else:
            raise ValueError("Edge incorrectly defined")

    def nonadjacent(self):
        pairs = []
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix)):
                if self.matrix[x][y] == 0 and self.matrix[y][x] == 0:
                    pairs.append(self.vertices[x] + "-" + self.vertices[y])
        return pairs

    def getweight(self, origin, dest):
        for edge in self.edges:
            if edge.head == origin and edge.tail == dest:
                return edge.weight
        return 0

    def getvertices(self):
        return self.vertices

    def edgestolist(self):
        edges = []

        for edge in [edge.get() for edge in self.edges]:
            if edge not in edges:
                edges.append(edge)
        return edges

    def edgestostr(self):
        edges = []

        for edge in self.edges:
            if str(edge) not in edges:
                edges.append(str(edge))
        return edges

    def degree(self, vertex):
        deg = 0
        for elem in self.matrix[self.vertices.index(vertex)]:
            if elem != 0:
                deg += 1
        for line in self.matrix:
            if line[self.vertices.index(vertex)] != 0:
                deg += 1
        return deg

    def getdest(self, vertex):
        adj = []
        for i in range(len(self.matrix[self.vertices.index(vertex)])):
            if self.matrix[self.vertices.index(vertex)][i] != 0:
                adj.append(self.vertices[i])

        return adj

    def iscomplete(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                if x != y and (self.matrix[x][y] == 0 or self.matrix[y][x] == 0):
                    return False
        return True

    def isconnected(self):
        # TODO Refazer com DFS/BFS
        for vertex in self.vertices:
            for aux_vertex in self.vertices:
                if vertex != aux_vertex and not (
                                self.pathbetween(vertex, aux_vertex) is None or self.pathbetween(aux_vertex,
                                                                                                 vertex) is None):
                    return False
        return True

    def pathbetween(self, start, end):

        if start not in self.vertices or end not in self.vertices:
            raise IndexError("Vertex not found")

        path = [start]

        previous = self.dijkstra(start)[1]
        temp = end

        while temp != start:
            path.insert(-1, temp)
            temp = previous[self.vertices.index(temp)]

        return path[::-1]

    def getpath(self, size):
        if size > len(self.getedges()):
            raise IndexError("Size greater than the number of edges")

        def search(size, root, path, visited):
            path.append(root)
            visited.append(root)
            adj = list(set(self.getdest(root)) - set(visited))

            if size == len(path) - 1:
                return path
            if not adj:
                path.pop()
                return

            for vertex in adj:
                search(size, vertex, path, visited)
                if size == len(path) - 1:
                    return path

        for vertex in self.vertices:
            path = []
            visited = []
            search(size, vertex, path, visited)
            if size == len(path) - 1:
                return path
        return None

    def getcycle(self):
        root = self.vertices[0]
        for vertex in self.vertices[1:]:
            cycle = self.pathbetween(root, vertex)
            if cycle[0] in self.getdest(cycle[-1]):
                return cycle + [cycle[0]]
        return None

    def hamiltonianpath(self):
        return self.getpath(len(self.vertices) - 1)

    def warshall(self, df=False):
        matrix = []

        for line in self.matrix:
            matrix.append(line.copy())

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] > 0:
                    matrix[i][j] = 1

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[j][i] == 1:
                    for k in range(len(self.vertices)):
                        matrix[j][k] = max(matrix[j][k], matrix[i][k])
        if not df:
            return matrix
        else:
            return DataFrame(matrix, self.vertices, self.vertices)

    def dijkstra(self, source, df=False):

        if source not in self.vertices:
            return "Source vertex not found"

        # Initial Setup
        unvisited = self.vertices.copy()
        distance = [float("inf")] * len(unvisited)
        previous = [""] * len(unvisited)

        for i in range(len(unvisited)):
            if unvisited[i] in self.getdest(source):
                distance[i] = self.getweight(source, unvisited[i])
                previous[i] = source

            else:
                if unvisited[i] == source:
                    distance[i] = 0

        while unvisited:
            u = self.vertices[self.vertices.index(min(unvisited))]
            unvisited.remove(u)

            for v in self.getdest(u):
                alt = distance[self.vertices.index(u)] + self.getweight(u, v)
                if alt < distance[self.vertices.index(v)]:
                    distance[self.vertices.index(v)] = alt
                    previous[self.vertices.index(v)] = u

        if df:
            return str(DataFrame([distance, previous], index=["Distance:", "From: "], columns=self.vertices))
        else:
            return [distance, previous]


g = DiGraph([['a', 'b'], ['b', 'c']])
