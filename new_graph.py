from pandas import DataFrame

class Edge:
    def __init__(self, head, tail, weight=1):
        self.head = head
        self.tail = tail
        self.weight = weight

    def __str__(self):
        return self.head + "-" + self.tail + ': ' + str(self.weight)


class NewGraph:
    def __init__(self, edges, undirected=False):
        self.vertices = []
        self.edges = edges
        self.matrix = []
        self.undirected = undirected

        # Transforma as arestas inseridas em objetos Edge
        for i in range(len(self.edges)):
            self.addedge(self.edges[i])

        # Gera matriz
        for v in self.vertices:
            self.matrix.append([0] * len(self.vertices))

        # Preenche a matriz
        for edge in self.edges:
            x = list(self.vertices).index(edge.head)
            y = list(self.vertices).index(edge.tail)
            self.matrix[x][y] = edge.weight


    def __str__(self):
        return str(DataFrame(self.matrix, index=self.vertices, columns=self.vertices))

    def addedge(self, edge):
        self.check_edge(edge)

        if edge[0] not in self.vertices:
            self.vertices.append(edge[0])
        if edge[1] not in self.vertices:
            self.vertices.append(edge[1])
        self.edges[self.edges.index(edge)] = Edge(*edge)
        if self.undirected:
            if len(edge) == 3:
                self.edges.append(Edge(edge[1], edge[0], edge[2]))
            else:
                self.edges.append(Edge(edge[1], edge[0]))

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
        return None

    def getvertices(self):
        return self.vertices

    def getedges(self):
        edges = []
        for edge in self.edges:
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
        for vertex in self.vertices:
            for aux_vertex in self.vertices:
                if vertex != aux_vertex and not (
                                self.pathbetween(vertex, aux_vertex) is None or self.pathbetween(aux_vertex,
                                                                                                 vertex) is None):
                    return False
        return True

    def pathbetween(self, start, end, visited=[]):
        path = []

        if end in self.getdest(start):
            return [start, end]

        else:
            path.append(start)
            visited.append(start)
            adj = list(set(self.getdest(start)) - set(visited))
            if adj:
                for vertex in adj:
                    try:
                        path += self.pathbetween(vertex, end, visited)
                    except TypeError:
                        path += []
            else:
                path.pop()
            if len(path) > 2:
                return path
            else:
                return None

    def getpath(self, size):
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

    def eulerianpath(self):
        return self.getpath(len(self.vertices) - 1)

    def hamiltonianpath(self):
        cycle = self.eulerianpath()
        if cycle:
            if not cycle[0] in self.getdest(cycle[-1]):
                return None
            else:
                return cycle + [cycle[0]]
        return None

    def warshall(self):
        matrix = list(self.matrix)
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[j][i] == 1:
                    for k in range(len(self.vertices)):
                        matrix[j][k] = max(matrix[j][k], matrix[i][k])
        return matrix

    def dijkstra(self, source, df = False):

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
                alt = distance[self.vertices.index(u)]+self.getweight(u, v)
                if alt < distance[self.vertices.index(v)]:
                    distance[self.vertices.index(v)] = alt
                    previous[self.vertices.index(v)] = u


        if df == True:
            return str(DataFrame([distance, previous], index=["Distance:", "From: "], columns=self.vertices))
        else:
            return [distance, previous]

g = NewGraph([['a', 'b', 5], ['a', 'c', 10], ['b', 'd', 6], ['b', 'e', 3], ['d', 'f', 6], ['e', 'c', 2], ['e', 'd', 2],
              ['e', 'g', 2], ['g', 'f', 2]])

print(g)
print(g.dijkstra('a', True))