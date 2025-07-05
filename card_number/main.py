
def p(n: int) -> float:
    if n < 0:
        raise ValueError()
    if n == 0 or n == 1:
        return 0
    res = 1
    for i in range(9999, 10000 - n, -1):
        res *= i
    return 1 - res / 10000 ** (n - 1)


print(p(100))
