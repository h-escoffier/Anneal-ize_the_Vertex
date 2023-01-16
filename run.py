import sys
from tqdm import tqdm
# from collections import Counter
from create_vertex.vertex import create_vertex
from brute_force.brute_force import bruteforce_algorithm
from simulated_annealing.algorithm import SimulatedAnnealing
from global_function import plot_solution, verification

original_stdout = sys.stdout

def main(nb_nodes, nb_edges, output):
    # Create the vertex
    vertex = create_vertex(nb_nodes, nb_edges)
    # Brute Force Algorithm
    bf_solutions = bruteforce_algorithm(vertex)
    if output == True:
        plot_solution(bf_solutions[0], vertex, 'Brute Force Solution', "output/Brute_force_solution")
    else:
        plot_solution(bf_solutions[0], vertex, 'Brute Force Solution', None)
    print('\nNumber of nodes in the optimal solution: ', len(bf_solutions[0]))
    print('Number of optimal solutions: ', len(bf_solutions[1]))
    # Simulated Annealing
    solutions = []
    # distribution = []
    best_solution = (0,)*nb_edges
    no_change = 0

    pbar = tqdm(total=10)
    while no_change != 10:
        solution, history = SimulatedAnnealing(vertex, bf_solution=len(bf_solutions[0]), max_move=1000, max_fail=10000).run()
        if verification(solution, vertex) and len(solution) < len(best_solution):
            solutions = [solution]
            best_solution = solution
            no_change = 0
            pbar.clear()
        elif verification(solution, vertex) and len(solution) == len(best_solution):
            best_solution = solution
            solutions.append(solution)
            no_change += 1
            pbar.update(1)
    print(history)
    pbar.close()
    solutions = list(set(solutions))
    print(len(best_solution))
    print('All solution :', solutions)


if __name__ == '__main__':
    print('start')
    main(20, 40, True)
    print('end')
