import copy
import argparse
import math


def distance(point1, point2):
    return math.ceil(math.sqrt(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) / 10))


def generate_neighbours(points):
    dict_of_neighbours = {}
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if i not in dict_of_neighbours:
                _list = list()
                _list.append([points[i][1], points[i][2]])
                dict_of_neighbours[i] = _list
            else:
                dict_of_neighbours[i].append(
                    [points[i][1], points[i][2]]
                )
            if points[i][1] not in dict_of_neighbours:
                _list = list()
                _list.append([line.split()[0], line.split()[2]])
                dict_of_neighbours[line.split()[1]] = _list
            else:
                dict_of_neighbours[line.split()[1]].append(
                    [line.split()[0], line.split()[2]]
                )
    return dict_of_neighbours


def generate_neighbours(points):
    dict_of_neighbours = {}

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if i not in dict_of_neighbours:
                _list = list()
                _list.append([j, distance(points[i], points[j])])
                dict_of_neighbours[i] = _list
            else:
                dict_of_neighbours[i].append([j, distance(points[i], points[j])])
            if j not in dict_of_neighbours:
                _list = list()
                _list.append([i, distance(points[i], points[j])])
                dict_of_neighbours[j] = _list
            else:
                dict_of_neighbours[j].append([i, distance(points[i], points[j])])

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
        for k in dict_of_neighbours[visiting]:
            if int(k[1]) < int(minim) and k[0] not in first_solution:
                minim = k[1]
                best_node = k[0]

        first_solution.append(visiting)
        distance_of_first_solution = distance_of_first_solution + int(minim)
        visiting = best_node

    first_solution.append(end_node)

    position = 0
    for k in dict_of_neighbours[first_solution[-2]]:
        if k[0] == start_node:
            break
        position += 1

    distance_of_first_solution = (
            distance_of_first_solution
            + int(dict_of_neighbours[first_solution[-2]][position][1])
            - 10000
    )
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
    >>) find_neighborhood(['a','c','b','d','e','a'])
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
                for i in dict_of_neighbours[k]:
                    if i[0] == next_node:
                        distance = distance + int(i[1])
            _tmp.append(distance)

            if _tmp not in neighborhood_of_solution:
                neighborhood_of_solution.append(_tmp)

    indexOfLastItemInTheList = len(neighborhood_of_solution[0]) - 1

    neighborhood_of_solution.sort(key=lambda x: x[indexOfLastItemInTheList])
    return neighborhood_of_solution


def tabu_search(
        first_solution, distance_of_first_solution, dict_of_neighbours, iters, size
):
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
    :return best_solution_ever: The solution with the lowest distance that occurred during the execution of Tabu search.
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

            if [first_exchange_node, second_exchange_node] not in tabu_list and [
                second_exchange_node,
                first_exchange_node,
            ] not in tabu_list:
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


if __name__ == "__main__":
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

    first_solution, distance_of_first_solution = generate_first_solution(
        dict_of_neighbours
    )

    best_sol, best_cost = tabu_search(
        first_solution,
        distance_of_first_solution,
        dict_of_neighbours,
        100,
        siz
    )

    print(f"Best solution: {best_sol}, with total distance: {best_cost}.")
