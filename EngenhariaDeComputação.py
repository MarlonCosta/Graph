import networkx as nx
import matplotlib.pyplot as plt

disciplinas = {00: 'Início do Curso',
               11: 'Pré-Cálculo', 12: 'Introdução a Engenharia', 13: 'Inglês instrumental',
               14: 'Algoritmos e Programação', 15: 'Laboratório de Algoritmos e Programação',
               16: 'Sistemas Digitais I', 17: 'Medição Eletro-Eletrônica', 21: 'Cálculo I',
               22: 'Leitura e prodrução de textos', 23: 'Estatística aplicada a computação',
               24: 'Laboratório de estrutura de dados e algoritmo', 25: 'Estrutura de dados e algoritmo',
               26: 'Sistemas Digitais II', 27: 'Ciências do ambiente', 31: 'Cálculo II',
               32: 'Relações Humanas no Trabalho', 33: 'Teoria dos Grafos', 34: 'Programação Orientada a Objetos',
               35: 'Laboratório de Programação orientada a objetos', 36: 'Organização e Arquitetura de Computadores',
               41: 'Física Clássica', 42: 'Metodologia de Pesquisa Científica', 43: 'Teoria da Computação',
               44: 'Sistemas operacionais', 45: 'Microprocessadores e Microcontroladores',
               51: 'Álgebra Linear Aplicada à Computação', 52: 'Eletricidade e Magnetismo', 53: 'Redes de Computadores',
               54: 'Bancos de Dados', 55: 'Projeto de Sistemas Digitais', 61: 'Métodos Numéricos',
               62: 'Inteligência Artificial', 63: 'Padrões de Projetos', 64: 'Sinais e Sistemas',
               65: 'Verificação Funcional de Sistemas', 71: 'Libras', 72: 'Análise e Técnicas de Algoritmos',
               73: 'Análise e Projeto de Sistemas', 74: 'Desenho Assistido por Computador',
               75: 'Circuitos Eletro-Eletrônicos', 81: 'Teste de Software', 82: 'Gerência de Projetos',
               83: 'Técnicas de Prototipagem', 84: 'Processamento Digital de Sinais', 85: 'Sensores e Atuadores',
               91: 'Empreendendorismo de Base Tecnológica', 92: 'Projeto em Engenharia de Computação I',
               93: 'Sistemas Embarcados', 94: 'Controle e Automação I', 95: 'Optativa I', 101: 'Direito e Cidadania',
               102: 'Ética', 103: 'Projeto em Engenharia de Computação II', 104: 'Optativa II', 105: 'Optativa III',
               110: 'Conclusão'}

# Isoladas: ['Leitura e prodrução de textos', 'Laboratório de estrutura de dados e algoritmo', 'Ciências do ambiente',
#  'Relações Humanas no Trabalho', 'Metodologia de Pesquisa Científica', 'Libras',
# 'Empreendendorismo de Base Tecnológica', 'Optativa I']

requisitos = [(00, 11), (00, 12), (00, 13), (00, 14), (00, 15), (00, 16), (00, 17), (22, 110), (24, 110), (27, 110),
              (32, 110), (42, 110), (71, 110), (91, 110), (95, 110), (11, 21), (11, 23), (14, 25), (15, 25), (16, 26),
              (21, 31), (25, 33), (14, 34), (15, 34), (14, 35), (15, 35), (26, 36), (21, 41), (25, 43), (25, 44),
              (36, 44), (36, 45), (31, 51), (31, 52), (25, 53), (25, 54), (36, 55), (44, 55), (51, 61), (43, 62),
              (34, 63), (35, 63), (31, 64), (55, 65), (25, 72), (63, 73), (52, 75), (64, 75), (34, 81), (35, 81),
              (54, 81), (73, 82), (74, 83), (61, 84), (64, 84), (75, 85), (83, 92), (44, 93), (45, 93), (61, 94),
              (75, 94), (92, 110), (101, 110), (102, 110), (103, 110), (104, 110), (105, 110)]

grafo = nx.Graph()
for node in disciplinas:
    grafo.add_node(disciplinas[node], pos=(node // 10, node % 10))
for edge in requisitos:
    grafo.add_edge(disciplinas[edge[0]], disciplinas[edge[1]])

print(grafo.nodes())
print(grafo.edges())
print(nx.isolates(grafo))
d = nx.degree(grafo)
pos = nx.get_node_attributes(grafo, 'pos')
nx.draw_networkx_labels(grafo, pos, font_size=10)
nx.draw(grafo, pos, nodelist=d.keys(), node_size=[v * 75 for v in d.values()])

plt.show()  # display
