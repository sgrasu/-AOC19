import operator

class DynamicList():
    def __init__(self, gen):
        self.list = list(gen)
    def __add__(self, rhs):
        self.list = self.list + rhs
    def maybe_expand_list(self, idx):
        if idx >= len(self.list):
            self.list = self.list + [0] * (idx - len(self.list) + 1)
    def __getitem__(self, i):
        self.maybe_expand_list(i)
        return self.list[i]
    def __getslice__(self, i, j):
        return self.list[i:j]
    def __setitem__(self, i, y):
        self.maybe_expand_list(i)
        self.list[i] = y
    def __sizeof__(self):
        return self.list.__sizeof__()
    def __len__(self):
        return len(self.list)
    def append(self, x):
        self.list.append(x)

class IntCode():
    def __init__(self, filename, phase = None):
        f = open(filename,"r")
        self.memory = DynamicList(map(int,f.readline().split(',')))
        self.out = []
        self.relative_base = 0
        self.input = [phase] if phase else []
        self.proc = self.operate()
        
    def out_op(self, x): 
        self.out.append(x)
        return None
    
    def in_op(self,_): 
        return int(self.input.pop(0))

    @staticmethod
    def jmp(n0t):
        def _jmp(val, _):
            if n0t:
                return not val
            return bool(val)
        return _jmp
    
    def set_rel_base(self, offset):
        self.relative_base += offset

    def op_code(self, code):
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
        else: 
            raise StopIteration #break opcode 99
        modes = [(code // 100 // 10 ** i) % 10 for i in range(args)]
        return (operation, modes, args, op)
    def operate(self,position = 0):
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
        yield from self.operate(position + arg_c + 1)   

    def output(self):
        if len(self.out) > 0:
            return self.out[-1]
        return None
        
    def start(self, input = None):
        self.input.append(input)
        return next(self.proc)

    def run(self, input = None):
        self.input.append(input)
        try:
            while True:
                out = next(self.proc)
                print(out)    
        except StopIteration as _:
            print("end")
