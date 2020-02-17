import statistics
from numpy.random import seed
from numpy.random import randn
from scipy.stats import wilcoxon, ttest_ind, ttest_rel, f_oneway
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt




# print("Avarage cost: " + str(int(statistics.mean(res))))
# print("Standard deviation: " + str(int(statistics.stdev(res))))
# print(max(res))
# print(min(res))


res = [11103, 11279, 11148, 11075, 11194, 11477, 10922, 11157, 11121, 11052, 10755, 11341, 11044, 10859, 10760, 11248,
       10767, 10930, 11055, 11151, 11341, 10835, 11194, 11355, 11374, 11348, 10988, 10993, 10977, 11175]
res1 = [11299, 11225, 11116, 11654, 11185, 11595, 11399, 11509, 11127, 10982, 11289, 11798, 11177, 11652, 11409, 11028,
        11478, 11165, 11200, 11447, 11234, 11492, 11314, 11142, 11114, 11481, 11560, 11177, 11417, 11220]
res2 = [11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508,
        11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508, 11508]
stat, p = f_oneway(res, res1)
print('SA and GA Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = f_oneway(res1, res2)
print('SA and TS Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = f_oneway(res, res2)
print('GA and TS Statistics=%.3f, p=%.3f' % (stat, p))
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')

if __name__ == '__main__':
    pass


def plotTSP(paths, points, num_iters=1):
    x = []
    y = []
    for i in paths[0]:
        x.append(points[i][0])
        y.append(points[i][1])
    plt.plot(x, y, 'co')

    a_scale = float(max(x)) / float(100)

    if num_iters > 1:
        for i in range(1, num_iters):
            xi = []
            yi = []
            for j in paths[i]:
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
