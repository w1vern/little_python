import datetime

a = [(0, -1/50, -1/50, 1.3),
     (-1/40, 0, 1/4, 0.25),
     (4/11, 4/110, 0, -15/11)]


iters = [[0]*len(a)]
diffs = [0]
start = datetime.datetime.now()
while True:
    iters.append([0]*len(a))
    for i in range(len(a)):
        sm = 0
        for j in range(len(a)):
            if i > j:
                sm += iters[-1][j] * a[i][j]
            else:
                sm += iters[-2][j] * a[i][j]
        iters[-1][i] = round(sm + a[i][-1], 3)
    diffs.append(max([abs(iters[-1][i] - iters[-2][i]) for i in range(len(a))]))
    if diffs[-1] < 0.01:
        break
stop = datetime.datetime.now()
for i in range(len(iters)):
    print(iters[i], diffs[i])
print("======== Result ========")
print(len(iters) - 1, iters[-1], diffs[-1])
print("========================")