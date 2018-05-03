from time import perf_counter
from math import inf
import matplotlib.pyplot as plt

import random

PATH_DEF = {
    0: [(1, 3), (2, 5), (6, 3)],
    1: [(0, 3), (2, 3), (3, 7), (6, 11)],
    2: [(0, 5), (1, 3), (3, 5)],
    3: [(1, 7), (2, 3), (4, 3), (5, 9), (6, 11)],
    4: [(3, 3), (5, 3)],
    5: [(3, 9), (4, 3), (6, 3)],
    6: [(0, 3), (1, 11), (3, 11), (5, 3)]
}
PATH_KEYS = list(PATH_DEF.keys())

all_generation_fittest_lengths = []
all_generation_average_lengths = []
all_generation_worst_lengths = []

POPULATION_SIZE = 5
MUTATION_RATE = 1
MAX_GENERATIONS = 100


def calc_path_length(path):
    length = 0
    for index in range(len(PATH_DEF) - 1):
        path_dict = dict(PATH_DEF[path[index]])

        length += path_dict[path[index+1]]
    return length


def dupe_check(point, path):
    if point in path:
        return False
    else:
        return True


def generate_next(current_point, current_path):
    available_points = list(filter(
        lambda tup: tup[0] not in current_path,
        PATH_DEF[current_point]
    ))
    if len(available_points):
        next_point = random.choice(available_points)[0]
    else:
        return None

    if dupe_check(next_point, current_path):
        return next_point
    else:
        return generate_next(current_point, current_path)


def generate_path(start=0, orig_path=[]):
    if len(orig_path):
        random_path = [generate_next(orig_path[-1], orig_path)]
    else:
        random_path = [random.choice(PATH_KEYS)]

    full_path = orig_path + random_path

    # while len(full_path) < len(PATH_KEYS):
    for i in range(start, len(PATH_DEF) - 1):
        next = generate_next(full_path[-1], full_path)

        if next is not None:
            random_path.append(next)

        full_path = orig_path + random_path

    if len(full_path) == len(PATH_KEYS):
        return full_path
    else:
        return None


def mutate_path(old):
    sample_count = round(len(old) * 2 / 10)
    tb_changed = random.choice(old)
    tb_changed_idx = old.index(tb_changed)

    if tb_changed_idx == 0:
        return generate_path()
    else:
        prev = old[tb_changed_idx - 1]
        prev_list = old[:tb_changed_idx]

        return generate_path(tb_changed_idx, prev_list)


def get_fittest(population):
    fittest_path = None
    fittest_length = inf

    for path in population:
        path_length = calc_path_length(path)

        if path_length < fittest_length:
            fittest_path = path
            fittest_length = path_length

    return (fittest_path, fittest_length)


def get_worst(population):
    worst_path = None
    worst_length = 0

    for path in population:
        path_length = calc_path_length(path)

        if path_length > worst_length:
            worst_path = path
            worst_length = path_length

    return (worst_path, worst_length)


def get_average(population):
    sum_lengths = 0
    for path in population:
        sum_lengths += calc_path_length(path)

    return sum_lengths / POPULATION_SIZE


def populate(fittest_path):
    population = [fittest_path]

    while len(population) < POPULATION_SIZE:
        mutated_path = mutate_path(list(fittest_path))
        if mutated_path is not None:
            population.append(mutated_path)
    return population


def pre_populate():
    population = []

    while len(population) < POPULATION_SIZE:
        path = generate_path()
        if path is not None:
            population.append(path)

    return population


def draw():
    fig, ax = plt.subplots()
    ax.plot(all_generation_fittest_lengths)
    ax.plot(all_generation_average_lengths)
    # ax.plot(all_generation_worst_lengths)
    ax.grid()
    plt.show()


def trav_salesman():
    t_start = perf_counter()

    population = pre_populate()

    for i in range(MAX_GENERATIONS):
        fittest = get_fittest(population)
        (fittest_path, fittest_length) = fittest

        all_generation_fittest_lengths.append(fittest_length)
        all_generation_average_lengths.append(
            get_average(population)
        )
        all_generation_worst_lengths.append(
            get_worst(population)[1]
        )

        population = populate(fittest_path)
        print("GENERATION : ", i)
        print("Fittest path : ", fittest_path)
        print("Population : ", population)
        print('Path Size', fittest_length)

    t_end = perf_counter()
    draw()

trav_salesman()
