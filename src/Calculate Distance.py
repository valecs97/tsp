import math


def distance(point1, point2):
    return math.sqrt(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)/10)


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
    path = [1, 8, 38, 31, 44, 18, 7, 28, 6, 37, 19, 27, 17, 43, 30, 36, 46, 33, 20, 47, 21, 32, 39, 48, 5, 42, 24, 10,
            45, 35, 4, 26, 2, 29, 34, 41, 16, 22, 3, 23, 14, 25, 13, 11, 12, 15, 40, 9, 1]
    fitness = 0
    for i in range(len(path) - 1):
        fitness += math.ceil(distance(points[path[i] - 1], points[path[i + 1] - 1]))
    print(fitness)
