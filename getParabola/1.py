import numpy as np
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


input = [Point(1, 0), Point(-1, 0), Point(0, -1), Point(0.1, -10)]


def getPor(input: list[Point]):
    for i in range(0, len(input)-1):
        for j in range(i + 1, len(input)):
            if (input[i].x == input[j].x):
                return

    matrix = []
    for i in range(0, len(input)):
        array = []
        for j in range(len(input)-1, -1, -1):
            array.append(input[i].x**j)
        matrix.append(array)

    y = []
    for i in range(0, len(input)):
        y.append([input[i].y])
    return np.linalg.solve(matrix, y)


ans = getPor(input)


x = np.arange(-1, 1, 0.001)
y = x**0 * ans[len(input) - 1, 0]
for i in range(len(input) - 1):
    y += x ** (len(input) - 1- i)  * ans[i] 

plt.scatter(list(map(lambda x: x.x, input)), list(map(lambda x: x.y, input)))
plt.plot(x, y)
plt.show()