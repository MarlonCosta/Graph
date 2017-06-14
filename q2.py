from graph import *
from collections import OrderedDict


def getvertex():
    def checkvertix(vertix):
        '''Checa se um vértice é válido'''
        if '-' in vertix or ' ' in vertix:
            raise ValueError("Invalid Vertix " + vertix + ": vertix contains separator character")
        if vertix == "":
            raise ValueError("Invalid Vertix: Empty value")
        for v in vertices:
            if vertices.count(v) > 1:
                raise ValueError("Invalid Vertix: Two or more inputs of the same vertix " + v)

    res = "y"
    end_vertex = "y"
    vertices = []
    connections = []

    while res.lower() == "y" or res.lower() == "yes":
        vertex = input("Type a new vertex:")
        end_vertex = "y"
        try:
            checkvertix(vertex)
        except ValueError:
            print('\nInvalid Vertex\n')
            continue
        vertices.append(vertex)
        connections.append([])
        while end_vertex.lower() == "y" or end_vertex.lower() == "yes":
            edge = input("Type a vertex that %s is linked to: " % vertex)
            connections[-1].append(edge)
            end_vertex = input("Want to add another connection? (Y)")

        res = input("Want to add another vertex? (Y)")

    count = 0
    for vertex in vertices:
        vertex = (vertex, connections[vertices.index(vertex)])
        vertices[count] = vertex
        count += 1

    vertices = OrderedDict(vertices)

    for vertex in vertices:
        for aux_vertex in vertices[vertex]:
            if vertex not in vertices[aux_vertex]:
                raise EdgeError

    return vertices


vertices = getvertex()

g = Graph(vertices)

print(g)
