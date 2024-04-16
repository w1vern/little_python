from math import factorial


def C(n, k):
    return factorial(n)/factorial(k)/factorial(n-k);

def A(n, k):
    return factorial(n)/factorial(n-k);

print(C(6, 3)*C(43, 3)/C(49, 6))