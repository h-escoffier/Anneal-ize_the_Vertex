import itertools
from tqdm import tqdm
from global_function import verification


# Generate of all possible combinations
def parsing(vertex):
    all_combination_list = []
    nodes_list = vertex.nodes()
    for n in range(1, vertex.number_of_nodes() + 1):
        combinations = [i for i in itertools.combinations(nodes_list, n)]
        all_combination_list = list(itertools.chain(all_combination_list, combinations))
    return all_combination_list


def bf_solution(vertex, all_combination_list):
    """
    Test the whole range of possible combinations
    :return:
        best_solution is a tuple containing one of the best solution
        all_best_solution is a list of tuple containing all the solutions
    """
    best_solution = tuple(vertex.nodes())
    all_best_solution = [best_solution]
    for solution in tqdm(iterable=all_combination_list, desc='Brute Force'):
        if verification(solution, vertex) and len(solution) < len(best_solution):
            best_solution = solution
            all_best_solution = [best_solution]
        elif verification(solution, vertex) and len(solution) == len(best_solution):
            all_best_solution.append(solution)
    return best_solution, all_best_solution


def bruteforce_algorithm(vertex):
    """
    This program finds the optimal solution to a minimum vertex cover problem using a brute force algorithm.
    :return: best_solution is a list of 2 elements [best_solution, all_best_solution] (cf. bf_solution)
    """
    best_solution = bf_solution(vertex, parsing(vertex))
    return best_solution
