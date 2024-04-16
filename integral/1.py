import math

coef = [3, 0.4, 2]
interval = [0, 100]
steps = 10000000


def f_val(x):
    return math.sin(x)


def int(coef: list[float], interval: list[float], steps: int) -> float:
    f = 0
    for i in range(0, steps):
        f += (interval[1]-interval[0])/steps * \
            f_val((interval[1]-interval[0])/steps*(i+1) + interval[0])
    return f


print(int(coef, interval, steps))
