"""CPU functionality."""

import sys
import re


HLT = '00000001'
LDI = '10000010'
PRN = '01000111'

ADD = '10100000'
SUB = '10100001'
MUL = '10100010'
DIV = '10100011'
MOD = '10100100'

alu = {
       '10100000': 'ADD',
       '10100001': 'SUB',
       '10100010': 'MUL',
       '10100011': 'DIV',
       '10100100': 'MOD'
       }

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.mar = 3  # initialize to R4, I think
        self.mdr = self.reg[3]  # initialize to the value R4 holds, I think

    def ram_read(self, mar):
        if 0 > mar or mar > len(self.ram): return None
        self.mar = mar
        self.mdr = self.ram[mar]
        return self.mdr

    def ram_write(self, mdr, mar):
        if 0 > mar or mar > len(self.ram): return None
        self.mar = mar
        self.ram[mar] = mdr
        self.mdr = self.ram[mar]

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        print(filename)

        lines = open(filename, 'r').read().splitlines()
        pattern = re.compile(r'[\d]{8}')
        instructions = []
        address = 0
        for line in lines:
            match = pattern.match(line)
            if match:
                self.ram[address] = match.group()
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # print(f'Reg A: {reg_a}[{self.reg[reg_a]}]')
        # print(f'Reg A: {reg_b}[{self.reg[reg_b]}]')
        if op == "ADD":
            self.reg[reg_a] = format(int(self.reg[reg_a], 2) + int(self.reg[reg_b], 2), '08b')
        elif op == "SUB":
            self.reg[reg_a] = format(int(self.reg[reg_a], 2) - int(self.reg[reg_b], 2), '08b')
        elif op == 'MUL':
            self.reg[reg_a] = format(int(self.reg[reg_a], 2) * int(self.reg[reg_b], 2), '08b')
        elif op == 'DIV':
            self.reg[reg_a] = format(int(self.reg[reg_a], 2) / int(self.reg[reg_b], 2), '08b')
        elif op == 'MOD':
            self.reg[reg_a] = format(int(self.reg[reg_a], 2) % int(self.reg[reg_b], 2), '08b')

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        ir = self.pc
        counter = 0
        while ir < len(self.ram) and counter < 20:
            counter += 1
            instruction = self.ram_read(ir)
            operand_a = self.ram_read(ir + 1)
            operand_b = self.ram_read(ir + 2)

            if instruction == HLT:
                return # figure out exit()
            elif instruction == LDI:
                index = int(operand_a, 2)
                self.reg[index] = operand_b
                ir += 3
            elif instruction == PRN:
                index = int(operand_a)
                value = int(self.reg[index], 2)
                print(value)
                ir += 2
            elif instruction in alu:
                self.alu(alu[instruction], int(operand_a, 2), int(operand_b, 2))
                ir += 3
