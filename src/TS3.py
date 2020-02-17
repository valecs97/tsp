"""
This is pure python implementation of Tabu search algorithm for a Travelling Salesman Problem, that the distances
between the cities are symmetric (the distance between city 'a' and city 'b' is the same between city 'b' and city 'a').
The TSP can be represented into a graph. The cities are represented by nodes and the distance between them is
represented by the weight of the ark between the nodes.

The .txt file with the graph has the form:

node1 node2 distance_between_node1_and_node2
node1 node3 distance_between_node1_and_node3
...

Be careful node1, node2 and the distance between them, must exist only once. This means in the .txt file
should not exist:
node1 node2 distance_between_node1_and_node2
node2 node1 distance_between_node2_and_node1

For pytests run following command:
pytest

For manual testing run:
python tabu_search.py -f your_file_name.txt -number_of_iterations_of_tabu_search -s size_of_tabu_search
e.g. python tabu_search.py -f tabudata2.txt -i 4 -s 3
"""

import copy
import argparse
import math
import sys


def distance(point1, point2):
    return math.ceil((math.sqrt(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)/10)))


def generate_neighbours(points):
    dict_of_neighbours = {}

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if i not in dict_of_neighbours:
                dict_of_neighbours[i] = {}
                dict_of_neighbours[i][j] = distance(points[i], points[j])
            else:
                dict_of_neighbours[i][j] = distance(points[i], points[j])
                # dict_of_neighbours[i] = sorted(dict_of_neighbours[i].items(), key=lambda kv: kv[1])
            if j not in dict_of_neighbours:
                dict_of_neighbours[j] = {}
                dict_of_neighbours[j][i] = distance(points[j], points[i])
            else:
                dict_of_neighbours[j][i] = distance(points[j], points[i])
                # dict_of_neighbours[i] = sorted(dict_of_neighbours[i].items(), key=lambda kv: kv[1])

    return dict_of_neighbours


def generate_first_solution(dict_of_neighbours):
    """
    Pure implementation of generating the first solution for the Tabu search to start, with the redundant resolution
    strategy. That means that we start from the starting node (e.g. node 'a'), then we go to the city nearest (lowest
    distance) to this node (let's assume is node 'c'), then we go to the nearest city of the node 'c', etc
    till we have visited all cities and return to the starting node.

    :param path: The path to the .txt file that includes the graph (e.g.tabudata2.txt)
    :param dict_of_neighbours: Dictionary with key each node and value a list of lists with the neighbors of the node
    and the cost (distance) for each neighbor.
    :return first_solution: The solution for the first iteration of Tabu search using the redundant resolution strategy
    in a list.
    :return distance_of_first_solution: The total distance that Travelling Salesman will travel, if he follows the path
    in first_solution.

    """

    start_node = 0
    end_node = start_node

    first_solution = []

    visiting = start_node

    distance_of_first_solution = 0

    while visiting not in first_solution:
        minim = 10000
        for k, v in dict_of_neighbours[visiting].items():
            if int(v) < int(minim) and k not in first_solution:
                minim = v
                best_node = k

        first_solution.append(visiting)
        distance_of_first_solution = distance_of_first_solution + int(minim)
        visiting = best_node

    first_solution.append(end_node)

    position = 0
    for k in dict_of_neighbours[first_solution[-2]]:
        if k == start_node:
            break
        position += 1

    # print(dict_of_neighbours[first_solution[-2]])

    distance_of_first_solution = distance_of_first_solution + int(
        dict_of_neighbours[first_solution[-2]][position]) - 10000
    return first_solution, distance_of_first_solution


def find_neighborhood(solution, dict_of_neighbours):
    """
    Pure implementation of generating the neighborhood (sorted by total distance of each solution from
    lowest to highest) of a solution with 1-1 exchange method, that means we exchange each node in a solution with each
    other node and generating a number of solution named neighborhood.

    :param solution: The solution in which we want to find the neighborhood.
    :param dict_of_neighbours: Dictionary with key each node and value a list of lists with the neighbors of the node
    and the cost (distance) for each neighbor.
    :return neighborhood_of_solution: A list that includes the solutions and the total distance of each solution
    (in form of list) that are produced with 1-1 exchange from the solution that the method took as an input


    Example:
    >>> find_neighborhood(['a','c','b','d','e','a'])
    [['a','e','b','d','c','a',90], [['a','c','d','b','e','a',90],['a','d','b','c','e','a',93],
    ['a','c','b','e','d','a',102], ['a','c','e','d','b','a',113], ['a','b','c','d','e','a',93]]

    """

    neighborhood_of_solution = []

    for n in solution[1:-1]:
        idx1 = solution.index(n)
        for kn in solution[1:-1]:
            idx2 = solution.index(kn)
            if n == kn:
                continue

            _tmp = copy.deepcopy(solution)
            _tmp[idx1] = kn
            _tmp[idx2] = n

            distance = 0

            for k in _tmp[:-1]:
                next_node = _tmp[_tmp.index(k) + 1]
                for i, j in dict_of_neighbours[k].items():
                    if i == next_node:
                        distance = distance + j
            _tmp.append(distance)

            if _tmp not in neighborhood_of_solution:
                neighborhood_of_solution.append(_tmp)

    indexOfLastItemInTheList = len(neighborhood_of_solution[0]) - 1

    neighborhood_of_solution.sort(key=lambda x: x[indexOfLastItemInTheList])
    return neighborhood_of_solution


def tabu_search(first_solution, distance_of_first_solution, dict_of_neighbours, iters, size):
    """
    Pure implementation of Tabu search algorithm for a Travelling Salesman Problem in Python.

    :param first_solution: The solution for the first iteration of Tabu search using the redundant resolution strategy
    in a list.
    :param distance_of_first_solution: The total distance that Travelling Salesman will travel, if he follows the path
    in first_solution.
    :param dict_of_neighbours: Dictionary with key each node and value a list of lists with the neighbors of the node
    and the cost (distance) for each neighbor.
    :param iters: The number of iterations that Tabu search will execute.
    :param size: The size of Tabu List.
    :return best_solution_ever: The solution with the lowest distance that occured during the execution of Tabu search.
    :return best_cost: The total distance that Travelling Salesman will travel, if he follows the path in best_solution
    ever.

    """
    count = 1
    solution = first_solution
    tabu_list = list()
    best_cost = distance_of_first_solution
    best_solution_ever = solution

    while count <= iters:
        neighborhood = find_neighborhood(solution, dict_of_neighbours)
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        best_cost_index = len(best_solution) - 1

        found = False
        while found is False:
            i = 0
            while i < len(best_solution):

                if best_solution[i] != solution[i]:
                    first_exchange_node = best_solution[i]
                    second_exchange_node = solution[i]
                    break
                i = i + 1

            if [first_exchange_node, second_exchange_node] not in tabu_list and [second_exchange_node,
                                                                                 first_exchange_node] not in tabu_list:
                tabu_list.append([first_exchange_node, second_exchange_node])
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[index_of_best_solution][best_cost_index]
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
                    print(str(count) + " " + str(best_cost))
            else:
                index_of_best_solution = index_of_best_solution + 1
                best_solution = neighborhood[index_of_best_solution]

        if len(tabu_list) >= size:
            tabu_list.pop(0)

        count = count + 1

    return best_solution_ever, best_cost


def main():
    siz = 0
    points = []
    with open("att48.tsp", "r") as f:
        readPoints = False
        for line in f.readlines():
            if readPoints:
                coords = line.split(' ')
                points.append((int(coords[1]), int(coords[2].strip())))
            elif "DIMENSION" in line:
                size = int(line.strip().split(':')[1])
            elif "NODE_COORD_SECTION" in line:
                readPoints = True

    dict_of_neighbours = generate_neighbours(points)
    # print(dict_of_neighbours)
    first_solution, distance_of_first_solution = generate_first_solution(dict_of_neighbours)
    # print(first_solution)
    # print(distance_of_first_solution)
    best_sol, best_cost = tabu_search(first_solution, distance_of_first_solution, dict_of_neighbours, 100, siz)

    print(best_sol)
    print(best_cost)


if __name__ == "__main__":
    main()
