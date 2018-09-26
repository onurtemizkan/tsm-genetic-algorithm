from time import perf_counter
from math import inf

PATH_DEF = {
    0: [(1, 3), (2, 5), (6, 3)],
    1: [(0, 3), (2, 3), (3, 7), (6, 11)],
    2: [(0, 5), (1, 3), (3, 5)],
    3: [(1, 7), (2, 3), (4, 3), (5, 9), (6, 11)],
    4: [(3, 3), (5, 3)],
    5: [(3, 9), (4, 3), (6, 3)],
    6: [(0, 3), (1, 11), (3, 11), (5, 3)]
}

all_paths = []


def calc_path_length(path):
    length = 0
    for index in range(len(PATH_DEF) - 1):
        path_dict = dict(PATH_DEF[path[index]])

        length += path_dict[path[index+1]]
    return length


def find_all_paths(current_path, paths=[]):
    if(len(current_path) == len(PATH_DEF)):
        return current_path

    available_paths = PATH_DEF[current_path[-1]]

    for path in available_paths:
        if path[0] not in current_path:
            next_paths = find_all_paths(current_path + [path[0]], paths)

            if next_paths is not None:
                all_paths.append(next_paths)


def trav_salesman():
    t_start = perf_counter()

    for point in PATH_DEF:
        find_all_paths([point])

    min_length = inf
    min_path = None

    for path in all_paths:
        path_length = calc_path_length(path)
        if path_length < min_length:
            min_path = path
            min_length = path_length
    t_end = perf_counter()

    print("shortest path", min_path)
    print("shortest path length", min_length)
    print("paths found", len(all_paths))
    print("time", t_end - t_start)

trav_salesman()
