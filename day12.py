import copy
import numpy as np
f = open('day12_in','r')
lines = list(f.readlines())
planets = []
for line in lines:
    line = line.strip()[1:-1]
    vals = line.split(',')
    planet = [int(val.split('=')[1]) for val in vals]
    planets.append(planet)
velocities = [list([0, 0, 0]) for _ in planets]

def step(planets, velocities):
    return_velocities = copy.deepcopy(velocities)
    for i in range(0,3):
        for ai, aval in enumerate(planets):
            for bi, bval in enumerate(planets):
                if aval[i] == bval[i]:
                    pass
                elif aval[i] < bval[i]:
                    return_velocities[ai][i] += 1
                else:
                    return_velocities[ai][i] -= 1
    new_planets = [[sum(axis) for axis in zip(pair[0], pair[1])] for pair in zip(planets, return_velocities)]
    return new_planets, return_velocities

def energy(planets, velocities):
    total_energy = 0
    for planet, velocity in zip(planets, velocities):
        total_energy += sum(map(abs,planet)) * sum(map(abs,velocity))
    return total_energy

def p1():
    planets = []
    for line in lines:
        line = line.strip()[1:-1]
        vals = line.split(',')
        planet = [int(val.split('=')[1]) for val in vals]
        planets.append(planet)
    velocities = [list([0, 0, 0]) for _ in planets]
    for _ in range(1000):
        planets, velocities = step(planets, velocities)
    for planet, velocity in zip(planets, velocities):
        print(planet, velocity)
    print(energy(planets, velocities))

def p2():
    planets = []
    for line in lines:
        line = line.strip()[1:-1]
        vals = line.split(',')
        planet = [int(val.split('=')[1]) for val in vals]
        planets.append(planet)
    velocities = [list([0, 0, 0]) for _ in planets]
    i = 0
    periods = [None, None, None]
    previous = [set(),set(),set()]
    while None in periods:
        for axis in range(3):
            positions = []
            for planet in planets:
                positions.append(planet[axis])
            positions = tuple(positions)
            vels = []
            for velocity in velocities:
                vels.append(velocity[axis])
            vels = tuple(vels)
            both = tuple([positions,vels])
            if both in previous[axis] and periods[axis] is None:
                periods[axis] = i
            else:
                previous[axis].add(both)
        i += 1
        planets, velocities = step(planets, velocities)
    print(i)
    print(np.lcm.reduce(periods))
p2()
