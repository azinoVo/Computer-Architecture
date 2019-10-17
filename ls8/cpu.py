"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 75
        self.register = [0] * 8
        self.pc = 0
        self.sp_index = 7

    def load(self):
        """Load a program into memory."""

        address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b10000010,  # LDI R1,9
        #     0b00000001,
        #     0b00001001,
        #     0b10100010,  # MUL R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001  # HLT
        # ]

        program = [
            # From stack.ls8
            0b10000010,  # LDI R0,1
            0b00000000,
            0b00000001,
            0b10000010,  # LDI R1,2
            0b00000001,
            0b00000010,
            0b01000101,  # PUSH R0
            0b00000000,
            0b01000101,  # PUSH R1
            0b00000001,
            0b10000010,  # LDI R0,3
            0b00000000,
            0b00000011,
            0b01000110,  # POP R0
            0b00000000,
            0b01000111,  # PRN R0
            0b00000000,
            0b10000010,  # LDI R0,4
            0b00000000,
            0b00000100,
            0b01000101,  # PUSH R0
            0b00000000,
            0b01000110,  # POP R2
            0b00000010,
            0b01000110,  # POP R1
            0b00000001,
            0b01000111,  # PRN R2
            0b00000010,
            0b01000111,  # PRN R1
            0b00000001,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        # try:
        #     address = 0

        #     with open(sys.argv[1]) as f:
        #         for line in f:
        #         # Process comments:
        #         # Ignore anything after a # symbol
        #             comment_split = line.split("#")

        #         # Convert any numbers from binary strings to integers
        #             num = comment_split[0].strip()
        #             try:
        #                 val = int(num, 2)
        #             except ValueError:
        #                 continue

        #             self.ram[address] = val
        #             address += 1
        #         # print(f"{val:08b}: {val:d}")

        # except FileNotFoundError:
        #     print(f"{sys.argv[0]}: {sys.argv[1]} not found")
        #     sys.exit(2)

        # for x in range(len(self.ram)):
        #     print(self.ram[x])

        # for y in range(len(self.register)):
        #     print("register", self.register[y])
        print("LOAD RAM:", self.ram)
        print("LOAD REG:", self.register)

    def ram_read(self, memory_address):
        return self.ram[memory_address]

    def ram_write(self, memory_address, memory_data):
        self.ram[memory_address] = memory_data
        return self.ram[memory_address]

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            print("opA", reg_a, "opB", reg_b)
            # self.register[reg_a] += self.register[reg_b]
            self.register[reg_a] = reg_b
            print("Register", self.register[reg_a])
            return self.register[reg_a]

        elif op == "MUL":
            print("opA", reg_a, "opB", reg_b)
            # self.register[reg_a] = self.register[reg_b]*self.register[reg_a]
            self.register[reg_a] *= self.register[reg_b]
            print("Register at", self.register[reg_a])
            return self.register[reg_a]
        # elif op == "SUB": etc
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
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b10000010, # LDI R1,9
        #     0b00000001,
        #     0b00001001,
        #     0b10100010, # MUL R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001 # HLT
        # ]

        # Head tags for instructions
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

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
                print(self.register)
                continue

            elif IR == MUL:
                multiplied = self.alu("MUL", operand_a, operand_b)
                self.pc += 3
                print("multiply at index zero", self.register[0])
                print("MULTIPLIED", multiplied)
                print(self.register)
                continue

            elif IR == PRN:
                print("IR == PRN")
                self.pc += 2

            elif IR == PUSH:
                # Push the value at pc in memory to the index of operand_a within register
                self.register[self.sp_index] -= 1
                value = self.register[operand_a]
                self.ram[self.register[self.sp_index]] = value
                print("IN PUSH, RAM", self.ram)
                print("IN PUSH, REG", self.register)
                self.pc += 2
                pass

            elif IR == POP:
                value = self.ram[self.register[self.sp_index]]
                self.register[operand_a] = value
                self.register[self.sp_index] += 1
                print("IN POP, RAM", self.ram)
                print("IN POP, REG", self.register)
                self.pc += 2
                pass

            elif IR == HLT:
                print("IR == HLT")
                running = False

            else:
                print("IR == ELSE")
                sys.exit(1)


cpu = CPU()
cpu.load()
cpu.run()
