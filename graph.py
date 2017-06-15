from pandas import DataFrame
from collections import OrderedDict

separator = '-'


class EdgeError(Exception):
    pass


class Graph:
    def __init__(self, vertices):
        """
        Graph constructor.
        :param vertices: Receives a OrderedDict, which consists on a list of tuples, each one containing the vertex name
        and a list of vertices that the vertex is connected to.
        After that, checks if there's an edge described on only one vertex.
        """

        self.vertices = OrderedDict(vertices)

        for vertex in self.vertices:
            for aux_vertex in self.vertices[vertex]:
                if aux_vertex not in self.vertices[vertex] or vertex not in self.vertices[aux_vertex]:
                    raise EdgeError("Edge only present in one of the vertices")

    def __str__(self):
        """Converts the graph to a panda's DataFrame for better formatting"""
        df = DataFrame(self.genmatrix(), index=self.vertices, columns=self.vertices)
        return str(df)

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

        def search(v):
            if len(path) == length + 1:
                return path

            if not self.vertices[v]:
                return path

            if v not in path:
                path.append(str(v))
                if len(path) == length + 1:
                    return path
                if len(path) > 1 and v not in self.vertices[path[-2]]:
                    path.pop()
                    return
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
        if len(path) != length + 1:
            return False
        else:
            return '-'.join(path)


grafos_teste = [
    Graph([('a', []), ('b', []), ('c', []), ('d', []), ('e', [])]),  # Grafo sem arestas
    Graph([('a', ['b', 'e']), ('b', ['a', 'c']), ('c', ['b', 'd']), ('d', ['c', 'e']), ('e', ['d', 'a'])]),
    # Grafo circular de 5 vértices e 5 arestas
    Graph([('a', ['b']), ('b', ['a']), ('c', ['d']), ('d', ['c'])]),  # Grafo com 2 arestas desconexas
    Graph([('J', ['C']), ('C', ['J', 'E', 'P', 'M', 'T']), ('E', ['C']), ('P', ['C']), ('M', ['C', 'T']),
           # Grafo do roteiro
           ('T', ['C', 'Z', 'M']), ('Z', ['T'])]),
    Graph([('a', ['b', 'c']), ('b', ['c', 'a']), ('c', ['b', 'a'])]),  # Grafo triangular
    Graph([('a', ['b', 'c', 'd', 'e']), ('b', ['a', 'c', 'd', 'e']), ('c', ['a', 'b', 'd', 'e']),
           ('d', ['a', 'b', 'c', 'e']), ('e', ['a', 'b', 'c', 'd'])])
    # Grafo completo de 5 vértices

]

'''for i in range(len(grafos_teste)):

    print("Grafo-teste número %d\n" %(i+1)+str(grafos_teste[i]))
    print("Ciclo encontrado:\n"+str(grafos_teste[i].getcycle())+"\n")
    for j in range(5):
        print("Buscando caminho de comprimento %d\n" %j+str(grafos_teste[i].getpath(j))+"\n")
    print("O grafo-teste número %d é conexo?\n" %(i+1)+str(grafos_teste[i].isconnected())+"\n\n")
'''

print(grafos_teste[3].getpath(4))
