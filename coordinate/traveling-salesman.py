import numpy as np

import string
import random
import math
import time

LIMX = 1200
LIMY = 500
NUMP = 5
ITERS = NUMP ** NUMP

points = []
paths = {}


def find_distances():
    dist_mat = np.zeros((NUMP, NUMP))
    for i, p1 in enumerate(points):
        for j in paths[i]:
            dist_mat[i][j] = np.linalg.norm(np.array(points[j]) - np.array(p1))

    return dist_mat


def find_initial_point():
    return random.choice(points)


def find_next_point(current_path):
    last_index = points.index(current_path[-1])
    path = list(paths[last_index])

    for old_index in current_path:
        if old_index in path:
            path.remove(old_index)

    next_index = random.choice(path)

    return points[next_index]


def path_repr(path):
    return list(map(lambda point: points.index(point), path))


def find_path(dist_mat):
    path = []
    path_length = 0
    curr = None

    for i in range(0, NUMP-1):
        if curr is None:
            curr = find_initial_point()
            path.append(curr)

        next = find_next_point(path)

        path_length += dist_mat.item(points.index(curr), points.index(next))

        path.append(next)
        curr = next

    return [path, path_length]


def find_shortest_path(dist_mat):
    record_length = math.inf
    record_path = None

    for i in range(0, ITERS):
        [path, length] = find_path(dist_mat)

        if length < record_length:
            [record_path, record_length] = [path, length]

    return [record_path, record_length]


def main():
    t_start = time.perf_counter()

    gen_points()
    gen_paths()

    distance_matrix = find_distances()
    print(distance_matrix)

    [record_path, record_length] = find_shortest_path(distance_matrix)

    t_end = time.perf_counter()

    print("record_path", path_repr(record_path))
    print("record_length", record_length)
    print("time_elapsed", t_end - t_start)

main()
