import copy
import math
import statistics

import matplotlib.pyplot as plt


def distance(point1, point2):
    return math.ceil(math.sqrt(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) / 10))


def generate_neighbours(points):
    dict_of_neighbours = {}

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if i not in dict_of_neighbours:
                dict_of_neighbours[i] = {}
                dict_of_neighbours[i][j] = distance(points[i], points[j])
            else:
                dict_of_neighbours[i][j] = distance(points[i], points[j])
            if j not in dict_of_neighbours:
                dict_of_neighbours[j] = {}
                dict_of_neighbours[j][i] = distance(points[j], points[i])
            else:
                dict_of_neighbours[j][i] = distance(points[j], points[i])

    return dict_of_neighbours


def generate_first_solution(start, dict_of_neighbours):
    start_node = start
    end_node = start_node

    first_solution = []
    distance = 0
    visiting = start_node
    pre_node = None
    while visiting not in first_solution:
        minim = 9999999
        next_node = 0
        for k, v in dict_of_neighbours[visiting].items():
            if v < minim and k not in first_solution:
                minim = v
                next_node = k
        distance += dict_of_neighbours[visiting][next_node]
        first_solution.append(visiting)
        pre_node = visiting
        visiting = next_node
    first_solution.append(start)
    distance += dict_of_neighbours[pre_node][end_node]
    return first_solution, distance


def find_neighborhood(solution, dict_of_neighbours, n_opt=1):
    neighborhood_of_solution = []
    for n in solution[1:-n_opt]:
        idx1 = []
        n_index = solution.index(n)
        for i in range(n_opt):
            idx1.append(n_index + i)
        for kn in solution[1:-n_opt]:
            idx2 = []
            kn_index = solution.index(kn)
            for i in range(n_opt):
                idx2.append(kn_index + i)
            if bool(set(solution[idx1[0]:(idx1[-1] + 1)]) &
                    set(solution[idx2[0]:(idx2[-1] + 1)])):
                continue
            _tmp = copy.deepcopy(solution)
            for i in range(n_opt):
                _tmp[idx1[i]] = solution[idx2[i]]
                _tmp[idx2[i]] = solution[idx1[i]]
            distance = 0
            for k in _tmp[:-1]:
                next_node = _tmp[_tmp.index(k) + 1]
                distance = distance + dict_of_neighbours[k][next_node]

            _tmp.append(distance)
            if _tmp not in neighborhood_of_solution:
                neighborhood_of_solution.append(_tmp)

    indexOfLastItemInTheList = len(neighborhood_of_solution[0]) - 1

    neighborhood_of_solution.sort(key=lambda x: x[indexOfLastItemInTheList])
    return neighborhood_of_solution


def tabu_search(first_solution, distance_of_first_solution, dict_of_neighbours, iters, size, n_opt=1):
    count = 1
    solution = first_solution
    tabu_list = list()
    best_cost = distance_of_first_solution
    best_solution_ever = solution
    while count <= iters:
        neighborhood = find_neighborhood(solution, dict_of_neighbours, n_opt=n_opt)
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        best_cost_index = len(best_solution) - 1
        found = False
        while found is False:
            i = 0
            first_exchange_node, second_exchange_node = [], []
            while i < len(best_solution):
                if best_solution[i] != solution[i]:
                    first_exchange_node.append(best_solution[i])
                    second_exchange_node.append(solution[i])
                    break
                i = i + 1

            exchange = first_exchange_node + second_exchange_node
            if first_exchange_node + second_exchange_node not in tabu_list and second_exchange_node + first_exchange_node not in tabu_list:
                tabu_list.append(exchange)
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[index_of_best_solution][best_cost_index]
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
                    print(str(count) + " " + str(best_cost))
            elif index_of_best_solution < len(neighborhood):
                best_solution = neighborhood[index_of_best_solution]
                index_of_best_solution = index_of_best_solution + 1

        while len(tabu_list) > size:
            tabu_list.pop(0)

        count = count + 1
    # best_solution_ever.pop(-1)
    return best_solution_ever, best_cost


def plotTSP(paths, points, num_iters=1):
    x = []
    y = []
    for i in paths:
        x.append(points[i][0])
        y.append(points[i][1])
    plt.plot(x, y, 'co')

    a_scale = float(max(x)) / float(100)

    if num_iters > 1:
        for i in range(1, num_iters):
            xi = []
            yi = []
            for j in paths:
                xi.append(points[j][0])
                yi.append(points[j][1])

            plt.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]),
                      head_width=a_scale, color='r',
                      length_includes_head=True, ls='dashed',
                      width=0.001 / float(num_iters))
            for i in range(0, len(x) - 1):
                plt.arrow(xi[i], yi[i], (xi[i + 1] - xi[i]), (yi[i + 1] - yi[i]),
                          head_width=a_scale, color='r', length_includes_head=True,
                          ls='dashed', width=0.001 / float(num_iters))
    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=a_scale,
              color='g', length_includes_head=True)
    for i in range(0, len(x) - 1):
        plt.arrow(x[i], y[i], (x[i + 1] - x[i]), (y[i + 1] - y[i]), head_width=a_scale,
                  color='g', length_includes_head=True)
    plt.xlim(min(x) * 1.1, max(x) * 1.1)
    plt.ylim(min(y) * 1.1, max(y) * 1.1)
    plt.show()


if __name__ == '__main__':
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
    first_solution, distance = generate_first_solution(23, dict_of_neighbours)
    costs = []
    for i in range(1, 31):
        print("Run NO." + str(i))
        best_solution_ever, best_cost = tabu_search(first_solution, distance, dict_of_neighbours, 3000, siz, 4)
        costs.append(best_cost)
        print(best_cost)
    print("Avarage cost: " + str(int(statistics.mean(costs))))
    print("Standard deviation: " + str(int(statistics.stdev(costs))))
    #plotTSP(best_solution_ever, points)

    best_solution_ever = [x + 1 for x in best_solution_ever]
    print(best_solution_ever)
    print(best_cost)
    print("Lowest cost: " + str(best_cost))
