from Graph import Graph


def recebe_vertice():
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
    vertices = []
    while res == "y":
        vertice = input("Informe um vertice:")
        try:
            checkvertix(vertice)
        except ValueError:
            print('Vértice inválido')
            continue
        vertices.append(vertice)
        res = input("se deseja continuar digite \'y\'")

    return vertices


def recebe_arestas(vertices):
    def checkedge(edge):
        '''Checa se uma aresta é válida'''
        if edge.count('-') != 1:
            raise ValueError("Invalid edge " + edge + ": more than one separator on the edge")

        if edge.startswith('-') or edge.endswith('-'):
            raise ValueError("Invalid edge " + edge + ": separator character at the beggining or the end of the edge")

        if edge[:edge.index('-')] not in vertices \
                or edge[edge.index('-') + 1:] not in vertices:
            raise ValueError("Invalid edge " + edge + " vertix not found")

    res = "y"
    arestas = []
    while res == "y":
        aresta = input("Informe uma aresta (Ex:J-G):")
        try:
            checkedge(aresta)
        except ValueError:
            print('Aresta inválida')
            continue
        arestas.append(aresta)
        res = input("se deseja continuar digite \'y\'")

    return arestas


vertices = recebe_vertice()
arestas = recebe_arestas(vertices)

g = Graph(vertices, arestas)

print(g)
