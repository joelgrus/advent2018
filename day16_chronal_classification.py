from typing import List, Callable, NamedTuple

Registers = List[int]

OPCODES = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
           'setr', 'seti', 'gtir', 'gtrr', 'gtri', 'eqri', 'eqir', 'eqrr']

class Instruction(NamedTuple):
    opcode: str
    a: int
    b: int
    c: int

    def operate(self, registers: Registers) -> Registers:
        output = registers[:]

        # addr (add register) stores into register C the result of adding register A and register B.
        if self.opcode == 'addr':
            output[self.c] = output[self.a] + output[self.b]
        # addi (add immediate) stores into register C the result of adding register A and value B.
        elif self.opcode == 'addi':
            output[self.c] = output[self.a] + self.b
        # mulr (multiply register) stores into register C the result of multiplying register A and register B.
        elif self.opcode == 'mulr':
            output[self.c] = output[self.a] * output[self.b]
        # muli (multiply immediate) stores into register C the result of multiplying register A and value B.
        elif self.opcode == 'muli':
            output[self.c] = output[self.a] * self.b
        # banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
        elif self.opcode == 'banr':
            output[self.c] = output[self.a] & output[self.b]
        # bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
        elif self.opcode == 'bani':
            output[self.c] = output[self.a] & self.b
        # borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
        elif self.opcode == 'borr':
            output[self.c] = output[self.a] | output[self.b]
        # bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
        elif self.opcode == 'bori':
            output[self.c] = output[self.a] | self.b
        # setr (set register) copies the contents of register A into register C. (Input B is ignored.)
        elif self.opcode == 'setr':
            output[self.c] = output[self.a]
        # seti (set immediate) stores value A into register C. (Input B is ignored.)
        elif self.opcode == 'seti':
            output[self.c] = self.a
        # gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
        elif self.opcode == 'gtir':
            if self.a > output[self.b]:
                output[self.c] = 1
            else:
                output[self.c] = 0
        # gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
        elif self.opcode == 'gtri':
            if output[self.a] > self.b:
                output[self.c] = 1
            else:
                output[self.c] = 0
        # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
        elif self.opcode == 'gtrr':
            if output[self.a] > output[self.b]:
                output[self.c] = 1
            else:
                output[self.c] = 0
        # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        elif self.opcode == 'eqir':
            if self.a == output[self.b]:
                output[self.c] = 1
            else:
                output[self.c] = 0
        # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        elif self.opcode == 'eqri':
            if output[self.a] == self.b:
                output[self.c] = 1
            else:
                output[self.c] = 0
        # eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
        elif self.opcode == 'eqrr':
            if output[self.a] == output[self.b]:
                output[self.c] = 1
            else:
                output[self.c] = 0
        else:
            raise ValueError(f"unknown opcode {self.opcode}")

        return output


# parsing code

RAW = """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]

Before: [3, 1, 0, 1]
9 3 3 2
After:  [3, 1, 0, 1]

Before: [1, 0, 3, 1]
4 2 3 2
After:  [1, 0, 0, 1]
"""

import re

rgx = r"Before: \[(.*?)\]\n(.*?)\nAfter:  \[(.*?)\]"

class Example(NamedTuple):
    before: Registers
    pre_instruction: List[int]
    after: Registers

def parse(raw: str) -> List[Example]:
    examples = []

    for b, pi, a in re.findall(rgx, raw):
        before = [int(x) for x in b.split(",")]
        after = [int(x) for x in a.split(",")]
        pre_instructions = [int(x) for x in pi.split()]

        examples.append(Example(before, pre_instructions, after))

    return examples

EXAMPLES = parse(RAW)

def possible_ops(example: Example) -> List[str]:
    _, a, b, c = example.pre_instruction

    return [opcode for opcode in OPCODES
            if Instruction(opcode, a, b, c).operate(example.before) == example.after]

# for example in EXAMPLES:
#     print(example, possible_ops(example))

with open('data/day16a.txt') as f:
    raw = f.read()

examples = parse(raw)

# for example in examples[:1]:
#     _, a, b, c = example.pre_instruction
#     print(example)
#     for opcode in OPCODES:
#         inst = Instruction(opcode, a, b, c)
#         output = inst.operate(example.before)
#         print(inst, output)

# print(len([example
#            for example in examples
#            if len(possible_ops(example)) >= 3]))

candidates = {i: OPCODES[:] for i in range(16)}

for example in examples:
    code, a, b, c = example.pre_instruction
    to_remove = set()
    for opcode in candidates[code]:
        inst = Instruction(opcode, a, b, c)
        output = inst.operate(example.before)
        if output != example.after:
            to_remove.add(opcode)

    candidates[code] = [opcode for opcode in candidates[code] if opcode not in to_remove]

    if len(candidates[code]) == 1:
        my_opcode = candidates[code][0]

        for i in candidates:
            if i != code:
                candidates[i] = [opcode for opcode in candidates[i] if opcode != my_opcode]

assert all(len(codes) == 1 for codes in candidates.values())

with open('data/day16b.txt') as f:
    instructions = []
    for line in f:
        code, a, b, c = [int(x) for x in line.split()]
        opcode = candidates[code][0]
        instructions.append(Instruction(opcode, a, b, c))

registers = [0, 0, 0, 0]
for instruction in instructions:
    registers = instruction.operate(registers)
print(registers)
