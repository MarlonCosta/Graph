from graph import Graph

g = Graph([('J', ['C']), ('C', ['J', 'E', 'P', 'M', 'T']), ('E', ['C']), ('P', ['C']), ('M', ['C', 'T']),
           ('T', ['C', 'Z', 'M']), ('Z', ['T'])])
print(g)
