import functools
f = open("day1_in","r")
lines = f.readlines()

def rocEq(total, mass):
    mass = int(mass)
    while mass > 0:
        fuel = mass // 3 - 2
        if fuel > 0:
            total += fuel
        mass = fuel
    return total

print(functools.reduce(rocEq, lines, 0))