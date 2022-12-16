import numpy as np


class SimulatedAnnealing:
    def __init__(self, vertex, bf_solution, alpha=0.95, t0=50, max_move=100, max_fail=10, temp='geometric'):
        self.vertex = vertex
        self.alpha = alpha
        self.t0 = t0
        self.max_move = max_move
        self.max_fail = max_fail
        self.temp = temp
        self.solution = tuple(self.vertex.number_of_nodes()*[1])
        self.best_solution = ()
        self.bf_solution = bf_solution

    # Determines S0
    def f_s0(self):
        """
        S0 is the solution containing all the vertex
        """
        self.solution = tuple(self.vertex.number_of_nodes() * [1])

    # Update the temperature
    def temp_update(self, t, i):
        if self.temp == 'geometric':
            t = self.alpha*t
        if self.temp == 'arithmetic':
            t -= self.alpha
        if self.temp == 'logarithmic':
            t = self.t0/(1 + np.log10(1 + i))  # TODO: CHERCHER LA BONNE VERSION
        return t

    # Change the solution by randomly adding or removing a node
    def switch(self, solution):
        changing_position = np.random.randint(0, self.vertex.number_of_nodes())
        l_solution = list(solution)
        if l_solution[changing_position] == 0:
            l_solution[changing_position] = 1
        else:
            l_solution[changing_position] = 0
        new_solution = tuple(l_solution)
        if l_solution == self.vertex.number_of_nodes()*[0]:
            new_solution = self.switch(solution)[0]
        v_i = (new_solution[changing_position], changing_position)   # v_i equal to 1 or 0
        return new_solution, v_i

    # Change the solution by removing one node from the solution and integrating another that is not part of the solution
    def swap(self, solution):
        t_solution = conversion(solution)
        non_solution = tuple([i for i in list(range(self.vertex.number_of_nodes())) if i not in list(t_solution)])
        select_1 = np.random.choice(t_solution)
        select_2 = np.random.choice(non_solution)
        l_solution = list(solution)
        for i in [select_1, select_2]:
            if l_solution[i] == 0:
                l_solution[i] = 1
            else:
                l_solution[i] = 0
        new_solution = tuple(l_solution)
        return new_solution

    # The energy depends on whether the solution is valid, the number of nodes covered and the number of nodes in the solution
    @staticmethod
    def energy(b_solution):
        solution = conversion(b_solution)
        # Variables
        nodes_nb = len(solution)
        # Energy equation
        energy = 1000/nodes_nb
        return energy

    # Calculates the probability of accepting a less optimal answer
    @staticmethod
    def probability(delta, t):
        probability = np.exp(delta/t)
        return probability

    # Simulated Annealing Algorithm
    def algorithm(self):
        # Initialisation
        failure = 0
        t = self.t0
        self.best_solution = self.solution
        all_time_best_energy = optimise_energy(self.vertex, self.solution)
        i = 0
        # Algorithm
        while self.max_fail != failure and t > 0:
            # if failure <= (self.max_fail/2):
            #     s_ = self.switch(self.solution)
            # else:
            #     s_ = self.swap(self.solution)
            #     failure = 0
            # delta = self.energy(s_) - self.energy(self.solution)
            # if verification(conversion(s_), self.vertex) and self.energy(s_) >= self.energy(self.solution):
            #     self.solution = s_
            #     if self.energy(s_) >= energy_best_solution:
            #         self.best_solution = s_
            #         energy_best_solution = self.energy(s_)
            #     failure = 0
            # elif verification(conversion(s_), self.vertex) and np.random.uniform() < self.probability(delta, t):
            #     self.solution = s_
            #     failure = 0
            # else:
            #     failure += 1
            list_s_vi = self.switch(self.solution)
            s_, v_i = list_s_vi
            # if verification(conversion(s_), self.vertex) and len(conversion(s_)) == self.bf_solution:
            #     print(s_)
            delta = optimise_energy(self.vertex, s_) - optimise_energy(self.vertex, self.solution)
            if delta < 0:
                self.solution = s_
                if optimise_energy(self.vertex, s_) <= all_time_best_energy:
                    self.best_solution = s_
                    all_time_best_energy = optimise_energy(self.vertex, s_)
                failure = 0
            # elif np.random.uniform() < self.probability(delta, t):
            elif np.random.uniform() < optimise_probability(self.vertex, v_i, delta, t):
                self.solution = s_
                failure = 0
            else:
                failure += 1
            t = self.temp_update(t, i=i)
        final_solution = conversion(self.best_solution)
        return final_solution

    def run(self):
        self.f_s0()
        self.algorithm()
        return conversion(self.best_solution)


def conversion(b_solution):
    """
    Convert a list format solution into a tuple format solution
    :param b_solution: list of the shape n w/ 0 & 1 for each node (e.g [0, 1, 0, 0, 0, 1, 0, 0, 0, 1])
    :return: tuple (e.g. (1, 5, 9))
    """
    t_solution = ()
    index = 0
    for node in b_solution:
        if node == 1:
            t_solution += (index, )
        index += 1
    return t_solution


# Return Deg(vi)
def deg_v(vertex, v):
    degree = len(set(vertex.edges(v)))
    edge_num = vertex.number_of_edges()
    deg = float(degree/edge_num)
    return deg


# Return probability depending on the value of vi
def optimise_probability(vertex, v, delta, t):
    deg = deg_v(vertex, v[1])
    if v[0] == 0:
        probability = np.exp(-(delta * (1 + deg)) / t)
    else:
        probability = np.exp(-(delta * (1 - deg)) / t)
    return probability


# Explanation of the energy fonction is available in the publication
def optimise_energy(vertex, b_solution, a=0.99, b=1):
    solution = conversion(b_solution)
    f1 = len(solution)  # OK
    f2 = -1*len(set(vertex.edges(solution)))  # OK
    f3 = len(set(vertex.edges))  # OK
    f = a*f1 + b*f2 + b*f3
    return f
