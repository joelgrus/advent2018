from typing import List

from day16_chronal_classification import Registers, Instruction

Program = List[Instruction]

RAW = """seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""

def parse(raw: str) -> Program:
    program = []
    for line in raw.strip().split("\n"):
        opcode, a, b, c = line.split()
        program.append(Instruction(opcode, int(a), int(b), int(c)))
    return program

def one_step(program: Program, registers: Registers, ip: int, ip_bound: int = 2) -> Registers:
    registers = registers[:]
    registers[ip_bound] = ip
    instruction = program[ip]
    registers = instruction.operate(registers)
    ip = registers[ip_bound] + 1

    return registers, ip

def execute(program: Program, ip_bound: int, initial_registers=None) -> Registers:
    if initial_registers is None:
        registers = [0, 0, 0, 0, 0, 0]
    else:
        registers = initial_registers[:]

    ip = registers[ip_bound]

    while 0 <= ip < len(program):
        print(ip, registers)
        # Get the corresponding instruction
        instruction = program[ip]
        registers[ip_bound] = ip
        registers = instruction.operate(registers)
        ip = registers[ip_bound] + 1

    return registers

PROGRAM = parse(RAW)
#assert execute(PROGRAM, ip_bound=0) == [6, 5, 6, 0, 0, 9]

with open('data/day19.txt') as f:
    raw = f.read().strip()

lines = raw.split("\n")
ip_bound = int(lines[0].split()[-1])
raw = "\n".join(lines[1:])
program = parse(raw)

# print(execute(program, ip_bound))
print(execute(program, ip_bound, [1, 0, 0, 0, 0, 0]))

import tqdm

def all_factors(n: int):
    factors = []
    for i in tqdm.trange(1, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors

f = all_factors(10551315)
