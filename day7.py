from intcode import IntCode

def maxAmp(phases = {0, 1, 2, 3, 4}, input = 0):
    if len(phases) == 1:
        return IntCode("day7_in", next(iter(phases))).start(input)

    maximum = -float("inf")
    for phase in phases:
        t_machine = IntCode("day7_in", phase)
        remaining_phases = phases -  {phase}
        next_input = t_machine.start(input)
        out = maxAmp(remaining_phases, next_input)
        maximum = max(maximum, out)
    return maximum

def generate_amps(phases = {0, 1, 2, 3, 4}, amps = []):
    if len(phases) == 1:
        amps.append(next(iter(phases)))
        yield list(map(lambda phase: IntCode("day7_in", phase), amps))
        amps.pop()
    else:
        for phase in phases:
            remaining_phases = phases -  {phase}
            amps.append(phase)
            yield from generate_amps(remaining_phases, amps)
            amps.pop()

def run_amps(amps):
    input = 0
    amp = 0
    try:
        while True:
            output = amps[amp].start(input)
            amp = (amp + 1) % len(amps)
            input = output
        return input
    except StopIteration as _:
        return input
    
maximum = -float("inf")
for amps in generate_amps({5, 6, 7, 8, 9}):
    out = run_amps(amps)
    maximum = max(out, maximum)
print(maximum)
