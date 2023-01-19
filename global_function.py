import networkx as nx
import matplotlib.pyplot as plt

# TODO: change the colours of the plot


def verification(solution, vertex):
    """
    Check if a solution is valid
    """
    if len(vertex.edges(solution)) == len(vertex.edges):
        return True
    else:
        return False


# Plot a solution
def plot_solution(solution, vertex, title, file_name):
    pos = nx.spring_layout(vertex, seed=1)
    edges_in = vertex.edges(solution)
    nx.draw_networkx(vertex, pos, node_color="#f17b3e")
    nx.draw_networkx_nodes(vertex, pos, nodelist=list(solution), node_color="#46a4ea", label='Solution')
    nx.draw_networkx_edges(vertex, pos, edgelist=edges_in, width=4, edge_color="#46a4ea")
    plt.title(title)
    plt.legend(markerscale=0.6)
    if file_name:
        plt.savefig(str(file_name) + ".png", format="PNG")
    plt.show()
