import numpy as np

def LFtoY(L: np.matrix, f: np.matrix) -> np.matrix:
    y = np.matrix([0.] * L.shape[0]).reshape(L.shape[0], 1)
    for i in range(L.shape[0]):
        y[i, 0] = f[i, 0]
        for j in range(0, i):
            y[i, 0] -= y[j, 0] * (L[i, j])
    return y
    
def UYtoX(U: np.matrix, y: np.matrix) -> np.matrix:
    x = np.matrix([0.] * U.shape[0]).reshape(U.shape[0], 1)
    for i in range(U.shape[0]-1, -1, -1):
        x[i, 0] = y[i, 0]
        for j in range(U.shape[0] - 1, i, -1):
            x[i, 0] -= x[j, 0] * (U[i, j])
        x[i, 0] /= U[i, i]
    return x

y = (LFtoY(np.matrix([[1, 0, 0], [0.58, 1, 0], [0.3569, 1.6433, 1]]), np.matrix([[6.1213], [3.868], [2.694]])))
#print(y)
U = np.matrix([[53.5999, 31.0882, 19.1314], [0, 1.1001, 1.8077], [0, 0, 0.2009]])
print(U**-1 * y)
print(UYtoX(U, y))
 