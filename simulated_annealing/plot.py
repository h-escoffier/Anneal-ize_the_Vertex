import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap


def plot_history(history_list, output_boolean):
    """
    Plots history of solution energy, the best energy (vertical axis) over number of iterations of annealing (horizontal
    axis).
    :param output_boolean:
    :param history_list: List of history steps, each element being a list with
    [iteration_index, temperature, solution_energy, best_energy]
    """
    iteration, temperature, solution_energy, best_energy = map(list, zip(*history_list))
    iteration = np.array([int(i) for i in iteration])
    temperature = np.array([np.float32(i) for i in temperature])
    solution_energy = np.array([np.float32(i) for i in solution_energy])
    best_energy = np.array([np.float32(i) for i in best_energy])
    x = iteration
    y1 = solution_energy
    y2 = best_energy
    # Create a set of line segments so that we can color them individually
    points_a = np.array([x, y1]).T.reshape(-1, 1, 2)
    segments_a = np.concatenate([points_a[:-1], points_a[1:]], axis=1)
    points_b = np.array([x, y2]).T.reshape(-1, 1, 2)
    segments_b = np.concatenate([points_b[:-1], points_b[1:]], axis=1)
    fig, axs = plt.subplots(1, 1)
    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(min(temperature), max(temperature))
    # Solution energy
    lc = LineCollection(segments_a, cmap='coolwarm', norm=norm)
    # Set the values used for color mapping
    lc.set_array(temperature)
    lc.set_linewidth(2)
    line = axs.add_collection(lc)
    cbar = plt.colorbar(line, ax=axs)
    cbar.set_label('Temperature', rotation=270, labelpad=20)
    # Best energy
    cmap = ListedColormap(['0'])  # '0' for color black
    lc = LineCollection(segments_b, cmap=cmap, norm=norm)
    # Set the values used for color mapping
    lc.set_array(temperature)
    lc.set_linewidth(2)
    axs.set_xlim(x.min(), 400)
    axs.set_ylim(10, 30)
    plt.title('Energy history of solution (colors) and best solution (black)')
    plt.ylabel('Energy')
    plt.xlabel('Iteration step')
    if output_boolean:
        plt.savefig("output/history.png", format="PNG")
    else:
        plt.show()
