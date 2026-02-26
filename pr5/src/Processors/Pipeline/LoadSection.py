from Memory import SimulatedRam
from SupportedFun import *

def load_init_section( data):
    # Iterate over the section data in 4-byte chunks (assuming each instruction is 4 bytes)
    for i in range(0, len(data), 4):
        # Read 4 bytes as a single 32-bit instruction
        instruction_bytes = data[i:i+4]
        # Convert bytes to a 32-bit binary string
        instr = format(int.from_bytes(instruction_bytes, byteorder='little'), '032b')
        # Add to instructions list
        SimulatedRam.instructionMem.append(instr)

    

def load_text_section(data):
    for i in range(0, len(data), 4):
        # Read 4 bytes as a single 32-bit instruction
        instruction_bytes = data[i:i+4]
        # Convert bytes to a 32-bit binary string
        instr = format(int.from_bytes(instruction_bytes, byteorder='little'), '032b')
        # print(f"instr uis ------------ {instr}")
        # Add to instructions list
        SimulatedRam.instructionMem.append(instr)

def load_data_section(data):
    for i in range(0, len(data), 4):
        # Read 4 bytes as a single 32-bit instruction
        instruction_bytes = data[i:i+4]
        # Convert bytes to a 32-bit binary string
        data1 = format(int.from_bytes(instruction_bytes, byteorder='little'), '032b')
        data1 = twos_complement_to_int(data1)
        # print(f"data is {hex(data1)}")

        # Add to instructions list
        SimulatedRam.dataMem.append(data1)
