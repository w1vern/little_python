

p2t = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 1]
]

t2p = [
    [0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0]
]

states = [[1, 0, 0, 0, 0]]
status = [True]


while True:
    n = 0
    for i in range(len(states)):
        if status[i]:
            n += 1
            for t in range(len(p2t[0])):
                flag = True
                for j in range(len(p2t)):
                    if 


    if n == 0:
        break
