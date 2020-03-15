import numpy as np
from random import random
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import MaxNLocator

model_settings = {}  # global variable for model settings


def init_custom(rows, cols, s_prob=0.1, o_prob=0.1):
    """
    Returns  matrix initiated with custom distribution of "o"  (0) and "s" (3) groups
    with values consisting of numbers in {0,...,3}.
    :param rows: the number of rows in the matrix
    :param cols: the number of columns in the matrix
    :param k: the number of states in the cellular automaton (2, by default)
    :param s_prob: probability of spreader's spawn (0.1, by default)
    :param o_prob: probability of opposer's spawn (0.1, by default)
    :return: a tensor with shape (1, rows, cols), randomly initialized with numbers in {0,...,k - 1}
    """
    random_numbers = []
    for r in range(rows):
        random_row = []
        for c in range(cols):
            rnd = random()
            if rnd < o_prob:
                random_row.append(0)
            elif rnd < o_prob+s_prob:
                random_row.append(3)
            else:
                random_row.append(1)
        random_numbers.append(random_row)

    return np.array([random_numbers])


def evolve(cellular_automaton, timesteps, apply_rule, r=1, neighbourhood='Moore'):
    """

    :param cellular_automaton:
    :param timesteps: the number of time steps in this evolution; note that this value refers to the total number of
                      time steps in this cellular automaton evolution, which includes the initial condition
    :param apply_rule: a function representing the rule to be applied to each cell during the evolution; this function
                       will be given three arguments, in the following order: the neighbourhood, which is a numpy
                       2D array of dimensions 2r+1 x 2r+1, representing the neighbourhood of the cell (if the
                       'von Neumann' neighbourhood is specified, the array will be a masked array); the cell identity,
                       which is a tuple representing the row and column indices of the cell in the cellular automaton
                       matrix, as (row, col); the time step, which is a scalar representing the time step in the
                       evolution
    :param r: the neighbourhood radius; the neighbourhood dimensions will be 2r+1 x 2r+1
    :param neighbourhood: the neighbourhood type; valid values are 'Moore' or 'von Neumann'
    :return:
    """
    _, rows, cols = cellular_automaton.shape
    array = np.zeros((timesteps, rows, cols), dtype=cellular_automaton.dtype)
    array[0] = cellular_automaton
    # demographics for initial state
    demographics = np.zeros((2, timesteps))  # variable for N/I ration graphic
    n_amount = 0
    i_amount = 0
    for x in cellular_automaton[0]:
        for y in x:
            if y == 1:
                n_amount += 1
    demographics[0][0] = n_amount
    demographics[1][0] = i_amount

    von_neumann_mask = np.zeros((2*r + 1, 2*r + 1), dtype=bool)
    for i in range(len(von_neumann_mask)):
        mask_size = np.absolute(r - i)
        von_neumann_mask[i][:mask_size] = 1
        if mask_size != 0:
            von_neumann_mask[i][-mask_size:] = 1

    def get_neighbourhood(cell_layer, row, col):
        row_indices = range(row - r, row + r + 1)
        row_indices = [i - cell_layer.shape[0] if i > (cell_layer.shape[0] - 1) else i for i in row_indices]
        col_indices = range(col - r, col + r + 1)
        col_indices = [i - cell_layer.shape[1] if i > (cell_layer.shape[1] - 1) else i for i in col_indices]
        n = cell_layer[np.ix_(row_indices, col_indices)]
        if neighbourhood == 'Moore':
            return n
        elif neighbourhood == 'von Neumann':
            return np.ma.masked_array(n, von_neumann_mask)
        else:
            raise Exception("unknown neighbourhood type: %s" % neighbourhood)

    for t in range(1, timesteps):
        cell_layer = array[t - 1]
        n_amount = 0
        i_amount = 0
        for row, cell_row in enumerate(cell_layer):
            for col, cell in enumerate(cell_row):
                n = get_neighbourhood(cell_layer, row, col)
                array[t][row][col] = apply_rule(n, (row, col), t)
                if array[t][row][col] == 1:
                    n_amount += 1
                elif array[t][row][col] == 2:
                    i_amount += 1
        demographics[0][t] = n_amount
        demographics[1][t] = i_amount
    return array, demographics


def update_model_settings(settings):
    # method for updating global variable of model settings
    global model_settings
    model_settings = settings


def update_demographics(value):
    # method for updating global variable of model settings
    global demographics
    demographics = value


def destructive_distribution_rule(neighbourhood, c, t):
    """
    :param neighbourhood: numpy array of dimensions 2r+1 x 2r+1, representing the neighbourhood
    :param c: the cell identity, which is a tuple representing the row and column indices of the cell in the cellular
    automaton matrix, as (row, col)
    :param t: the time step, which is a scalar representing the time step in the evolution
    :return: cell's new state
    """
    # total values of neighbours' influence
    total_destruction_influence = 0
    total_anti_influence = 0
    global model_settings  # using set on the form model settings

    for neighbour_row in neighbourhood:
        for neighbour in neighbour_row:
            if neighbour == 0:  # opposers
                total_anti_influence += model_settings['opposers_influence']
            elif neighbour == 1:  # normal
                total_anti_influence += model_settings['normal_influence']
            elif neighbour == 2:  # infected
                total_destruction_influence += model_settings['infected_influence']
            elif neighbour == 3:  # supporters
                total_destruction_influence += model_settings['spreaders_influence']
            else:
                pass

    if neighbourhood[1][1] == 0:
        return 3 if total_destruction_influence - total_anti_influence > model_settings['opposers_resistance'] else 0
    if neighbourhood[1][1] == 1:
        return 2 if total_destruction_influence - total_anti_influence > model_settings['normal_resistance'] else 1
    if neighbourhood[1][1] == 2:
        return 1 if total_anti_influence - total_destruction_influence > model_settings['infected_resistance'] else 2
    if neighbourhood[1][1] == 3:
        return 0 if total_anti_influence - total_destruction_influence > model_settings['spreaders_resistance'] else 3
    return -1


# creating new color scheme, which is corresponding to paper's model group's colors

N = 4
values = np.ones((N, 4))
values[0] = np.array([14/256, 14/256, 230/256, 1])
values[1] = np.array([14/256, 230/256, 14/256, 1])
values[2] = np.array([153/256, 0/256, 153/256, 1])
values[3] = np.array([230/256, 14/256, 14/256, 1])
newcmp = ListedColormap(values)


def plot_animate(ca, fig_count, title='', dem=None):
    """
    :param ca: array of all CA's states
    :param fig_count: index of new figure
    :param title: figure title
    :param dem: array of demographics
    :return:
    """
    cmap = plt.get_cmap(newcmp)
    fig = plt.figure(fig_count - 1)
    fig.canvas.set_window_title(title)
    im = plt.imshow(ca[0], animated=True, cmap=cmap)
    i = {'index': 0}

    def updatefig(*args):
        i['index'] += 1
        if i['index'] == len(ca):
            i['index'] = 0
        im.set_array(ca[i['index']])
        return im,
    ani = animation.FuncAnimation(fig, updatefig, interval=100, blit=True)
    if dem is not None:
        plot_demographics(dem, fig_count, 'Соотношение Обычных и Заражённых людей для ' + title)
    plt.show()


def plot_demographics(dem_value, fig_count, title=''):
    time = np.arange(0, len(dem_value[0]))
    fig_number = fig_count
    plt.figure(fig_count)
    plt.figure(fig_count).canvas.set_window_title(title)
    lines = plt.plot(time, dem_value[0], time, dem_value[1])
    plt.setp(lines[0], linestyle='-', color='green')
    plt.setp(lines[1], linestyle='-', color='xkcd:violet')
    plt.ylabel('Число')
    plt.xlabel('Шаг')
    ax = plt.figure(fig_count).gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.legend(('Обычные (N)', 'Заражённые (I)'), loc='upper right')
    plt.show()
