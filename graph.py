from pandas import DataFrame
from collections import OrderedDict

separator = '-'


class EdgeError(Exception):
    pass


class Edge:
    def __init__(self, head, tail, weight=1):
        self.head = head
        self.tail = tail
        self.weight = weight

    def __repr__(self):
        return self.head + separator + self.tail

    def __reversed__(self):
        return self.tail + separator + self.head


class Graph:
    def __init__(self, vertices):
        """
        Graph constructor.
        :param vertices: Receives a OrderedDict, which consists on a list of tuples, each one containing the vertex name
        and a list of vertices that the vertex is connected to.
        After that, checks if there's an edge described on only one vertex.
        """

        self.vertices = OrderedDict(vertices)
        self.edges = []

        for vertex in self.vertices:
            for aux_vertex in self.vertices[vertex]:
                self.edges.append(Edge(vertex, aux_vertex))

    def __str__(self):
        """Converts the graph to a panda's DataFrame for better formatting"""
        return str(DataFrame(self.genmatrix(), index=self.vertices, columns=self.vertices))

    def nonadjacent(self):
        """:return: Returns a list containing the pairs of non-adjacent vertices."""
        pairs = []
        for vertex in self.vertices:
            for aux_vertex in list(set(self.vertices) - set(vertex)):
                if vertex not in list(set(self.vertices) - set(vertex)):
                    if aux_vertex + separator + vertex not in pairs:
                        pairs.append(vertex + separator + aux_vertex)
        return pairs

    def getedges(self, vertex=None):
        """
        Returns a list with all edges on the graph (if vertex == None) or the ones containing the vertex.
        """

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

    def addedge(self, head, tail):
        for vertex in self.vertices:
            if vertex == head and tail not in self.vertices[vertex]:
                self.vertices[vertex].append(tail)
            if vertex == tail and head not in self.vertices[vertex]:
                self.vertices[vertex].append(head)
        self.edges.append(Edge(head, tail))

    def removeedge(self, head, tail):
        for vertex in self.vertices:
            if vertex == head and tail in self.vertices[vertex]:
                self.vertices[vertex].remove(tail)
            if vertex == tail and head in self.vertices[vertex]:
                self.vertices[vertex].remove(head)
        for edge in self.edges:
            if (edge.head == head and edge.tail == tail) or (edge.head == tail and edge.tail == head):
                self.edges.remove(edge)

    def genmatrix(self, hide=True):
        """
        Generates and returns a matrix that represents the adjacencies between the vertices.
        :param: hide: If True, replaces duplicate values (e.g: A-B and B-A) on the matrix for '-'.
        """

        matrix = []

        for v in self.vertices:
            matrix.append([0] * len(self.vertices))

        for vertex in self.vertices:
            for connection in self.vertices[vertex]:
                x = list(self.vertices).index(vertex)
                y = list(self.vertices).index(connection)
                matrix[x][y] = 1

        if hide:
            for i in range(len(matrix)):
                for j in range(len(matrix)):
                    if type(matrix[i][j]) != str:
                        matrix[i][j] = str(matrix[i][j])
                    if i > j:
                        matrix[i][j] = '-'

        return matrix

    def degree(self, vertex):
        """Returns the degree of given vertex."""
        return len(self.vertices[vertex])

    def getcycle(self):
        """Searches for any cycle on the graph, if a cycle is found, returns it, else, returns False."""

        cycle = []

        def search(vertex):
            """Recursive search function"""

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
                search(v)

        for v in self.vertices:
            search(v)

        if cycle:
            return '-'.join(cycle)
        else:
            return False

    def iscomplete(self):
        """Checks if the graph is complete. Returns a corresponding boolean."""
        for vertex in self.vertices:
            if len(self.vertices[vertex]) != len(self.vertices):
                return False
            for aux_vertex in self.vertices:
                if vertex not in self.vertices[aux_vertex]:
                    return False
        return True

    def pathbetween(self, head, tail):

        path = []

        if head + separator + tail in self.getedges() or tail + separator + head in self.getedges():
            path.append(head)
            path.append(tail)
            return path

        def search(vertex):
            path.append(vertex)

            if path[0] == head and path[-1] == tail:
                return path
            adjacencies = (set(self.vertices[vertex]) - set(path))

            if not adjacencies:
                if path[0] == head and path[-1] == tail:
                    return path
                else:
                    path.pop()
                    return path

            for v in adjacencies:
                if path[0] == head and path[-1] == tail:
                    return path
                else:
                    search(v)

        search(head)

        if path[0] == head and path[-1] == tail:
            return path
        else:
            return False

    def isconnected(self):
        """Check if the graph is connected. i.e. if the every vertex has a path to every different vertex.
        Returns a corresponding boolean."""

        for vertex in self.vertices:
            if not self.vertices[vertex]:
                return False
            for aux_vertex in self.vertices:
                if not self.pathbetween(vertex, aux_vertex):
                    return False

        return True

    def getpath(self, length=0):
        """Searches for a path of given length, if found, returns it, else, returns False."""
        path = []

        def search(vert):
            if len(path) == length + 1:
                return path

            if not self.vertices[vert]:
                return path

            if vert not in path:
                path.append(str(vert))
                if len(path) == length + 1:
                    return path
                if len(path) > 1 and vert not in self.vertices[path[-2]]:
                    path.pop()
                    return
            else:
                return

            adjacencies = list(set(self.vertices[vert]) - set(path))
            if len(adjacencies) > 0:
                for adj in adjacencies:
                    search(adj)
            else:
                path.pop()
            return path

        for v in self.vertices:
            search(v)
            if len(path) == length + 1:
                return '-'.join(path)
            elif path:
                path.pop()

        return False

    def warshall(self, df=False):
        matrix = self.genmatrix(hide=False)

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

    def getbridges(self):
        bridges = []
        for vertex in self.vertices:
            for aux_vertex in self.vertices[vertex]:
                v = vertex + separator + aux_vertex
                rv = aux_vertex + separator + vertex
                self.removeedge(vertex, aux_vertex)
                self.removeedge(aux_vertex, vertex)
                if not self.isconnected() and (v not in bridges and rv not in bridges):
                    bridges.append(vertex + separator + aux_vertex)
                self.addedge(vertex, aux_vertex)
                self.addedge(aux_vertex, vertex)
        return bridges

    def eulerianpath(self):
        odd = 0
        for vertex in self.vertices:
            if self.degree(vertex) % 2 != 0:
                odd += 1

        if odd == 2 or odd == 0:
            return True
        else:
            return False

    def euleriancycle(self):
        vertices = [v for v in self.vertices if self.degree(v) > 0 and self.degree(v) % 2 == 0]
        if len(vertices) == len(self.vertices):
            return True
        else:
            return False


g = Graph([('0', ['1', '2', '3']), ('1', ['0', '2']), ('2', ['0', '1']), ('3', ['0', '4']), ('4', ['3'])])

print(g)
print(g.eulerianpath())
print(g.euleriancycle())
