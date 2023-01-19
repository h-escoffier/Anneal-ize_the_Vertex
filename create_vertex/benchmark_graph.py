import networkx as nx
from tqdm import tqdm


def file_to_graph(file):
    """
    This function can be used to plot a graph from a file
    """
    edges_list = []
    nodes_list = []
    with open(file, 'r') as benchmark_file:
        content = [x.strip('\n') for x in benchmark_file.readlines()]
        for elm in tqdm(iterable=content, desc='read'):
            cols = elm.split(' ')
            if cols[0] == 'e':
                nodes_list.append(int(cols[1]))
                nodes_list.append(int(cols[2]))
                edge = (int(cols[1]), int(cols[2]))
                edges_list.append(edge)
    nodes_list.append(0)
    nodes_list = list(set(nodes_list))
    g = nx.Graph()
    g.add_nodes_from(nodes_list)
    g.add_edges_from(edges_list)
    return g

