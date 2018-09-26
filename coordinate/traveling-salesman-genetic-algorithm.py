import numpy as np

import string
import random
import math
import time

LIMX = 1200
LIMY = 500
NUMP = 10
ITERS = NUMP ** NUMP
points = []


def gen_points():
    for i in range(0, NUMP):
        points.append([random.randint(0, LIMX), random.randint(0, LIMY)])


def find_distances():
    dist_mat = np.zeros((NUMP, NUMP))
    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points):
            dist_mat[i][j] = np.linalg.norm(np.array(p2) - np.array(p1))

    return dist_mat


def find_next_point(current_path):
    next = random.choice(points)

    if next in current_path:
        return find_next_point(current_path)
    else:
        return next


def path_repr(path):
    return list(map(lambda point: points.index(point), path))


def find_path(dist_mat):
    path = []
    path_length = 0
    curr = None

    for i in range(0, NUMP-1):
        if curr is None:
            curr = find_next_point(path)
            path.append(curr)

        next = find_next_point(path)

        path_length += dist_mat.item(points.index(curr), points.index(next))

        path.append(next)
        curr = next

    points_repr = path_repr(path)

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
    distance_matrix = find_distances()

    [record_path, record_length] = find_shortest_path(distance_matrix)

    t_end = time.perf_counter()

    print("record_path", path_repr(record_path))
    print("record_length", record_length)
    print("time_elapsed", t_end - t_start)

main()
