
matrix = [
    [1, 5, 1, 35],
    [4, -1, 1, 8],
    [2, 5, -1, 10],
    [1, 0, 0, 2],
    [-2, -1, 1, 2]
]


def simplex(matrix):
    for i in range(0, len(matrix)):
        el = matrix[i]
        matrix[i].pop(-1)
        for j in range(len(matrix)-1):
            matrix[i].append(i == j)
        matrix[i].append(el)

    base = []
    first = len(matrix[0]) - len(matrix) + 1
    for i in range(len(matrix)-1):
        base.append(first + i)

    while (True):
        min = 0
        columnOfMin = len(matrix[0])
        for i in range(len(matrix[0]) - 1):
            if matrix[len(matrix)-1][i] < min:
                columnOfMin = i
                min = matrix[len(matrix)-1][i]
        if min == 0:
            break

        min = float('inf')
        rowOfMin = len(matrix)
        for i in range(len(matrix)-1):
            if matrix[i][columnOfMin] <= 0:
                continue
            if matrix[i][columnOfMin] < min:
                min = matrix[i][columnOfMin]
                rowOfMin = i

        base[rowOfMin] = columnOfMin + 1

        newMatrix///
        newMatrix = matrix[::]
        print(matrix[rowOfMin][columnOfMin])
        for i in range(len(matrix)):
            newMatrix[i][columnOfMin] = 0
        for i in range(len(matrix[0])):
            newMatrix[rowOfMin][i] = matrix[rowOfMin][i] / \
                matrix[rowOfMin][columnOfMin]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if i == rowOfMin or j == columnOfMin:
                    continue
                
                newMatrix[i][j] = matrix[i][j] - matrix[i][columnOfMin] * \
                    matrix[rowOfMin][j] / matrix[rowOfMin][columnOfMin]
        matrix = newMatrix
    return matrix

res = simplex(matrix)

print(res)

