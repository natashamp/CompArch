# SJSU CMPE 120 Spring 2022 TEAM6

# input 1 -> file with assembly code
# input 2 -> file with setup code to run the assembly code specified in input 1

#Step 1: Read the file assembly language program one line at a time.
#Step 2: We need to display encoding of each instruction in program.
#Step 3: Execute each instruction and display register values after each instruction execution.
#Step 4: Log all state and operations into text files in the log directory..
#Step 5: Test all the instructions and be able to demo them.

# print $v0, and $v1 if set
# Used for Register addressing demo
# python instruction_simulator.py "add" --log=INFO
# python instruction_simulator.py "sub" --log=INFO
# python instruction_simulator.py "and" --log=INFO
# python instruction_simulator.py "or" --log=INFO
#
# Used for Register Indirect addressing demo
# python instruction_simulator.py "copy" --log=INFO
#
# Used for Immediate addressing demo
# python instruction_simulator.py "assign_num" --log=INFO

import sys
import logging

#Using a dictionary to find the index of the opcode to find the encoding
opcode = {
    "lw"   : 9,
    "sw"   : 8,
    "add"  : 7,
    "addi" : 6,
    "and"  : 5,
    "sub"  : 4,
    "or"   : 3,
    "slt"  : 2,
    "beq"  : 1,
    "j"    : 0,
}

#Using a dictionary to find the index of the register name to find the encoding
registers = {
    "$0"  : 0,
    "$1"  : 1,
    "$v0" : 2,
    "$a0" : 3,
    "$a1" : 4,
    "$t0" : 5,
    "$t1" : 6,
    "$t2" : 7,
    "$t3" : 8,
    "$s0" : 9,
    "$s1" : 10,
    "$s2" : 11,
    "$s3" : 12,
    "$sp" : 13,
    "$fp" : 14,
    "$ra" : 15,
}

#initialize the 16 register values to 0 
register_value = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#initialize the 256 memory values to 0. We have 8 bits of immediate instru and 2^8 =256 memory values 
memory_value = [0]*256

#copied from logging facility avaliable in python documentation
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

fileHandler = logging.FileHandler("../log/instruction_simulator.log")
fileHandler.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

rootLogger.addHandler(consoleHandler)
rootLogger.addHandler(fileHandler)

def log(line):
    #Step 4: Log all state and operations into text files in the log directory..
    logging.info(line)

def binary(num):
    tmp = "{0:b}".format(num)
    tmp = tmp.zfill(4)
    return tmp

def slt(line):
    #slt $v0, $a0, $a1
    encode  = binary(opcode["slt"])
    line = line.split()
    arg = "".join(line[1:])
    arg = arg.split(',')
    binarg0 = binary(registers[arg[0]])
    binarg1 = binary(registers[arg[1]])
    binarg2 = binary(registers[arg[2]])
    #Step 2: We need to display encoding of each instruction in program.
    log("Encoding of instruction {}: {} {} {} {}".format(line, encode, binarg0, binarg1, binarg2))

    #Step 3: Execute each instruction and display register values after each instruction execution.
    register_value[registers[arg[0]]] = 0
    if register_value[registers[arg[1]]] < register_value[registers[arg[2]]]:
        register_value[registers[arg[0]]] = 1
    log("        Result in Register {} = {}".format(arg[0], register_value[registers[arg[0]]]))
    log("        Register {} = {}".format(arg[1], register_value[registers[arg[1]]]))

def or_reg(line):
    #or $v0, $a0, $a1
    encode  = binary(opcode["or"])
    line = line.split()
    arg = "".join(line[1:])
    arg = arg.split(',')
    binarg0 = binary(registers[arg[0]])
    binarg1 = binary(registers[arg[1]])
    binarg2 = binary(registers[arg[2]])
    #Step 2: We need to display encoding of each instruction in program.
    log("Encoding of instruction {}: {} {} {} {}".format(line, encode, binarg0, binarg1, binarg2))

    #Step 3: Execute each instruction and display register values after each instruction execution.
    register_value[registers[arg[0]]] = register_value[registers[arg[1]]] | register_value[registers[arg[2]]]
    log("        Result in Register {} = {}".format(arg[0], register_value[registers[arg[0]]]))
    log("        Register {} = {}".format(arg[1], register_value[registers[arg[1]]]))

def and_reg(line):
    #and $v0, $a0, $a1
    encode  = binary(opcode["and"])
    line = line.split()
    arg = "".join(line[1:])
    arg = arg.split(',')
    binarg0 = binary(registers[arg[0]])
    binarg1 = binary(registers[arg[1]])
    binarg2 = binary(registers[arg[2]])
    #Step 2: We need to display encoding of each instruction in program.
    log("Encoding of instruction {}: {} {} {} {}".format(line, encode, binarg0, binarg1, binarg2))

    #Step 3: Execute each instruction and display register values after each instruction execution.
    register_value[registers[arg[0]]] = register_value[registers[arg[1]]] & register_value[registers[arg[2]]]
    log("        Result in Register {} = {}".format(arg[0], register_value[registers[arg[0]]]))
    log("        Register {} = {}".format(arg[1], register_value[registers[arg[1]]]))

def sub(line):
    #sub $v0, $a0, $a1
    encode  = binary(opcode["sub"])
    line = line.split()
    arg = "".join(line[1:])
    arg = arg.split(',')
    binarg0 = binary(registers[arg[0]])
    binarg1 = binary(registers[arg[1]])
    binarg2 = binary(registers[arg[2]])
    #Step 2: We need to display encoding of each instruction in program.
    log("Encoding of instruction {}: {} {} {} {}".format(line, encode, binarg0, binarg1, binarg2))

    #Step 3: Execute each instruction and display register values after each instruction execution.
    register_value[registers[arg[0]]] = register_value[registers[arg[1]]] - register_value[registers[arg[2]]]
    log("        Result in Register {} = {}".format(arg[0], register_value[registers[arg[0]]]))
    log("        Register {} = {}".format(arg[1], register_value[registers[arg[1]]]))

def add(line):
    #add $v0, $a0, $a1
    encode  = binary(opcode["add"])
    line = line.split()
    arg = "".join(line[1:])
    arg = arg.split(',')
    binarg0 = binary(registers[arg[0]])
    binarg1 = binary(registers[arg[1]])
    binarg2 = binary(registers[arg[2]])
    #Step 2: We need to display encoding of each instruction in program.
    log("Encoding of instruction {}: {} {} {} {}".format(line, encode, binarg0, binarg1, binarg2))

    #Step 3: Execute each instruction and display register values after each instruction execution.
    register_value[registers[arg[0]]] = register_value[registers[arg[1]]] + register_value[registers[arg[2]]]
    log("        Result in Register {} = {}".format(arg[0], register_value[registers[arg[0]]]))
    log("        Register {} = {}".format(arg[1], register_value[registers[arg[1]]]))
    log("        Register {} = {}".format(arg[2], register_value[registers[arg[2]]]))

def addi(line):
    #addi $a1, $0, 7
    encode = binary(opcode["addi"])
    line = line.split()
    arg = "".join(line[1:])
    arg = arg.split(',')
    binarg0 = binary(registers[arg[0]])
    binarg1 = binary(registers[arg[1]])
    binarg2 = binary(int(arg[2]))
    #Step 2: We need to display encoding of each instruction in program.
    log("Encoding of instruction {}: {} {} {} {}".format(line, encode, binarg0, binarg1, binarg2))

    #Step 3: Execute each instruction and display register values after each instruction execution.
    register_value[registers[arg[0]]] = register_value[registers[arg[1]]] + int(arg[2])
    log("        Result in Register {} = {}".format(arg[0], register_value[registers[arg[0]]]))
    log("        Register {} = {}".format(arg[1], register_value[registers[arg[1]]]))

def sw(line):
    #sw $t0, i($a1)
    encode = binary(opcode["sw"])
    line = line.split()

    arg = "".join(line[1:])
    arg = arg.split(',')

    binarg0 = binary(registers[arg[0]])
    source = arg[0]

    arg = arg[1].split('(')
    binarg2 = binary(int(arg[0]))
    immediate = int(arg[0])
    
    arg = arg[1][0:3]
    binarg1 = binary(registers[arg])
    dest = arg

    #Step 2: We need to display encoding of each instruction in program.
    log("Encoding of instruction {}: {} {} {} {}".format(line, encode, binarg1, binarg0, binarg2))

    #Step 3: Execute each instruction and display register values after each instruction execution.
    memory_value[register_value[registers[dest]] + immediate] = register_value[registers[source]]
    log("     Result at memory address {} = {}".format(register_value[registers[dest]],  memory_value[register_value[registers[dest]] + immediate]))

def lw(line):
    #lw $t0, i($a0)
    encode = binary(opcode["lw"])
    line = line.split()

    arg = "".join(line[1:])
    arg = arg.split(',')

    binarg0 = binary(registers[arg[0]])
    dest = arg[0]

    arg = arg[1].split('(')
    binarg2 = binary(int(arg[0]))
    immediate = int(arg[0])
    
    arg = arg[1][0:3]
    binarg1 = binary(registers[arg])
    source = arg

    #Step 2: We need to display encoding of each instruction in program.
    log("Encoding of instruction {}: {} {} {} {}".format(line, encode, binarg1, binarg0, binarg2))

    #Step 3: Execute each instruction and display register values after each instruction execution.
    register_value[registers[dest]] = memory_value[register_value[registers[source]] + immediate]
    log("     Value in register {} = {}".format(dest, register_value[registers[dest]]))

def jump(line):
    #j label
    log("Executing jump")
    #For a jump instruction we are storing the instructions line by line in a dictionary as we execute them. 
    #So when we see a label we will have the number of the instr#uction line saved in the index of the dictionary.
    #So when we reach a jump instruction we can move the PC to the index saved in the dictionary and execute the instructions from there

def beq(line):
    #beq $t0, $t1, label
    log("Executing beq")
    #For a beq instruction we are storing the instructions line by line in a dictionary as we execute them. 
    #So when we see a label we will have the number of the instr#uction line saved in the index of the dictionary.
    #So when we reach a beq instruction can check whether we need to jump and if so then we implement the  PC to the index saved 
    #and execute the instructions from there


def decode_instructions(line):
    if line.startswith('addi'):
        addi(line)
        return
    if line.startswith('add'):
        add(line)
        return
    if line.startswith('lw'):
        lw(line)
        return
    if line.startswith('sw'):
        sw(line)
        return
    if line.startswith('sub'):
        sub(line)
        return
    if line.startswith('and'):
        and_reg(line)
        return
    if line.startswith('or'):
        or_reg(line)
        return
    if line.startswith('slt'):
        slt(line)
        return
    if line.startswith('beq'):
        beq(line)
        return
    if line.startswith('j'):
        jump(line)
        return

def print_return_values():
    log("\n\nReturn Value in $v0 is {}".format(register_value[registers["$v0"]]))

def execute_all(instruction_file):
    #Step 1: Read the file assembly language program one line at a time
    print("\n\n")
    print instruction_file
    with open(instruction_file) as f:
        line = f.readline()
        while line:
            line = f.readline()
            if line.startswith('#'):
                continue
            decode_instructions(line)

if __name__ == "__main__":
    execute_all(sys.argv[1]+".setup")
    execute_all(sys.argv[1])
    # print return value registers
    print_return_values()

