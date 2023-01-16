import sys
from tqdm import tqdm
# from collections import Counter
from create_vertex.vertex import create_vertex
from brute_force.brute_force import bruteforce_algorithm
from simulated_annealing.algorithm import SimulatedAnnealing
from global_function import plot_solution, verification
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

original_stdout = sys.stdout

def main(nb_nodes, nb_edges, output_boolean):
    # Create the vertex
    vertex = create_vertex(nb_nodes, nb_edges)
    # Brute Force Algorithm
    bf_solutions = bruteforce_algorithm(vertex) #
    if output_boolean == True:
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

    ### Plot best_solution here
    if output_boolean == True:

        with open("output/history.txt", 'w+') as h:
            h.write(str(history))
    plot_history(history, output_boolean)
    pbar.close()
    solutions = list(set(solutions))
    print(len(best_solution))
    print('All solution:', solutions)

def plot_history(history_list, output_boolean):
    '''
    Plots history of solution energy, best energy (vertical axis)
        over number of iterations of annealing (horizontal axis).
    :param history_list: List of history steps, each element being a list with [iteration_index, temperature, solution_energy, best_energy]
    :return: No return, either plots directly
    '''
    iter, temperature, solution_energy, best_energy = map(list, zip(*history_list))

    iter = np.array([int(i) for i in iter])
    temperature = np.array([np.float32(i) for i in temperature])
    solution_energy = np.array([np.float32(i) for i in solution_energy])
    best_energy = np.array([np.float32(i) for i in best_energy])

    y_bound = max(solution_energy.all(), best_energy.all())

    x = iter
    y1 = solution_energy
    y2 = best_energy

    # Create a set of line segments so that we can color them individually
    # This creates the points as a N x 1 x 2 array so that we can stack points
    # together easily to get the segments. The segments array for line collection
    # needs to be (numlines) x (points per line) x 2 (for x and y)
    points_a = np.array([x, y1]).T.reshape(-1, 1, 2)
    segments_a = np.concatenate([points_a[:-1], points_a[1:]], axis=1)

    points_b = np.array([x, y2]).T.reshape(-1, 1, 2)
    segments_b = np.concatenate([points_b[:-1], points_b[1:]], axis=1)

    fig, axs = plt.subplots(1, 1, sharex=True, sharey=True)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(min(temperature), max(temperature))

    ### Solution energy
    lc = LineCollection(segments_a, cmap='coolwarm', norm=norm)
    # Set the values used for colormapping
    lc.set_array(temperature)
    lc.set_linewidth(2)
    line = axs.add_collection(lc)
    cbar = plt.colorbar(line, ax=axs)
    cbar.set_label('Temperature', rotation=270, labelpad=20)

    ### Best energy
    cmap = ListedColormap(['0'])  # '0' for color black
    lc = LineCollection(segments_b, cmap=cmap, norm=norm)
    # Set the values used for colormapping
    lc.set_array(temperature)
    lc.set_linewidth(2)
    line = axs.add_collection(lc)

    axs.set_xlim(x.min(), 400)
    axs.set_ylim(10, 30)

    plt.title('Energy history of solution (colors) and best solution (black)')
    plt.ylabel('Energy')
    plt.xlabel('Iteration step')
    if output_boolean == True:
        plt.savefig("output/history.png", format = "PNG")
    else:
        plt.show()


if __name__ == '__main__':

    print('start')
    main(20, 40, True)
    print('end')
