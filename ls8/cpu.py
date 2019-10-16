"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        
        for x in range(len(self.ram)-249):
            print(self.ram[x])

        for y in range(len(self.reg)):
            print("register", self.reg[y])

    def ram_read(self, memory_address):
        return self.ram[memory_address]

    def ram_write(self, memory_address, memory_data):
        self.ram[memory_address] = memory_data
        return self.ram[memory_address]

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            print("opA", reg_a, "opB", reg_b)
            # self.reg[reg_a] += self.reg[reg_b]
            self.reg[reg_a] = reg_b
            print("Register", self.reg[0])
            return reg_a + reg_b
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # Head tags for instructions
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        
        running = True

        while running:
            IR = self.ram[self.pc]
            operand_a = self.ram[self.pc+1]
            operand_b = self.ram[self.pc+2]
            print("MEMORY", IR)

            if IR == LDI:
                added = self.alu("ADD", operand_a, operand_b)
                self.pc += 3
                print("Added", added)
                continue

            elif IR == PRN:
                print("IR == PRN")
                self.pc += 2

            elif IR == HLT:
                print("IR == HLT")
                running = False

            else:
                print("IR == ELSE")
                sys.exit(1)


cpu = CPU()
cpu.load()
cpu.run()