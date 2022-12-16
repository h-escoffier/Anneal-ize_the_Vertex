import networkx as nx
import numpy as np


# Generation of a graph with a specified number of nodes and edges
def create_vertex(nb_nodes, nb_edges):
    g = nx.Graph()
    nodes_list = [i for i in range(nb_nodes)]
    edges_list = []
    if nb_edges >= (nb_nodes*(nb_nodes - 1))/2:
        print('The number of edges requested is too large. The number of edges has been set to the maximum number of possible edges')
        nb_edges = (nb_nodes*(nb_nodes - 1))/2
    while len(edges_list) < nb_edges:
        edge = tuple(sorted(tuple(np.random.choice(nodes_list, 2, False))))
        edges_list.append(edge)
        edges_list = list(set(edges_list))
    g.add_nodes_from(nodes_list)
    g.add_edges_from(edges_list)
    return g

