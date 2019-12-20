import operator
f = open("day2_in","r")
const = list(map(int,f.readline().split(',')))
for x in range(100):
    for y in range(100):
        intcode = const.copy()
        intcode[1] = x
        intcode[2] = y
        for i in range(0, len(intcode) - 3, 4):
            a, b, c, d = intcode[i:i + 4]
            if a == 1:
                op = operator.add
            elif a == 2:
                op = operator.mul
            else: break
            intcode[d] = op(intcode[b], intcode[c])
        if intcode[0] == 19690720: print(x, y)

print(intcode)