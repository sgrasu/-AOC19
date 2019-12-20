''' Module defining the intcode machine and any helper classes or functions '''

class IntCode():
    ''' stateful intcode machine '''

    def __init__(self, filename, init_state=None):
        f = open(filename, "r")
        self.memory = DynamicList(map(int, f.readline().split(',')))
        self.out = []
        self.relative_base = 0
        self.input = []
        if init_state: self.memory[0] = init_state
        self.proc = self.operate()

    def out_op(self, output):
        ''' output operation '''
        self.out.append(output)

    def in_op(self, _):
        ''' input operation '''
        return int(self.input.pop(0))

    @staticmethod
    def jmp(n0t):
        ''' returns a function which tells machine to jump if it evaluates to true ''' 
        def _jmp(val, _):
            if n0t:
                return not val
            return bool(val)
        return _jmp

    def set_rel_base(self, offset):
        ''' update the relative base for mode 2 commands '''
        self.relative_base += offset

    def op_code(self, code):
        ''' parses the op code and returns the associated operation, as well as 
            modes of the inputs and outputs, num_args, and opcode identifier '''
        op = code % 100
        if op == 1:
            operation = lambda x, y, _: x + y
            args = 3
        elif op == 2:
            operation = lambda x, y, _: x * y
            args = 3
        elif op == 3:
            operation = self.in_op
            args = 1
        elif op == 4:
            operation = self.out_op
            args = 1
        elif op == 5:
            operation = self.jmp(False)
            args = 2
        elif op == 6:
            operation = self.jmp(True)
            args = 2
        elif op == 7:
            operation = lambda x, y, _: int(x < y)
            args = 3
        elif op == 8:
            operation = lambda x, y, _: int(x == y)
            args = 3
        elif op == 9:
            operation = self.set_rel_base
            args = 1
        elif op == 99:
            raise StopIteration #break opcode 99
        else:
            raise RuntimeError #oops
        modes = [(code // 100 // 10 ** i) % 10 for i in range(args)]
        return (operation, modes, args, op)

    def operate(self, position=0):
        ''' generator which runs the intcode machine, yielding each time there's an output
            raises a StopIteration when it reaches a termination opcode '''
        while True:
            memory = self.memory
            operation, modes, arg_c, op = self.op_code(memory[position])
            vals = [memory[memory[position + offset + 1]] if mode == 0 \
                    else memory[memory[position + offset + 1] + self.relative_base] if mode == 2 \
                    else memory[position + offset + 1] for offset, mode in enumerate(modes)]
            result = operation(*vals)
            if 5 <= op <= 6:
                if result:
                    position = vals[-1] - arg_c - 1
            elif op == 4:
                yield self.out[-1]
            elif op == 9:
                pass
            else:
                write_pos = memory[position + arg_c]
                write_pos += self.relative_base if modes[-1] == 2 else 0
                memory[write_pos] = result
            position += arg_c + 1

    def output(self):
        ''' prints last item in the output queue '''
        if len(self.out) > 0:
            return self.out[-1]
        return None

    def start(self, input=None):
        ''' adds an input (maybe) and runs the
            machine until it yields an output '''
        if input is not None:
            self.input.append(input)
        return next(self.proc)

    def add_input(self, input = None):
        if input is not None:
            self.input.append(input)
            
    def set_input(self, input = None):
        if input is not None:
            self.input = [input]

    def run(self, inputs=None):
        ''' runs the machine repeatedly with an arbitrary
            list inputs, until termination '''
        try:
            while True:
                out = self.start(inputs.pop()) if inputs else self.start()
                print(out)    
        except StopIteration as _:
            print("end")

class DynamicList():
    ''' Wrapper around built-in list which automatically expands with zeros whenever
        there's an attempt to index something out of bounds. Done to satisfy day9 '''
    def __init__(self, gen):
        self.list = list(gen)
    def __add__(self, rhs):
        self.list = self.list + rhs
    def _maybe_expand_list(self, idx):
        if idx >= len(self.list):
            self.list = self.list + [0] * (idx - len(self.list) + 1)
    def __getitem__(self, i):
        self._maybe_expand_list(i)
        return self.list[i]
    def __getslice__(self, i, j):
        return self.list[i:j]
    def __setitem__(self, i, y):
        self._maybe_expand_list(i)
        self.list[i] = y
    def __sizeof__(self):
        return self.list.__sizeof__()
    def __len__(self):
        return len(self.list)
    def append(self, x):
        ''' append to list '''
        self.list.append(x)
