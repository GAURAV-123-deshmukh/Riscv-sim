from LoadSection import *
import sys
from Processor import Processor
import argparse
from readElf import *

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Load binary files and run processor simulation.')
    parser.add_argument('file_name_prefix', type=str, 
                        help='Prefix for the binary file names (without extension).')
    parser.add_argument('--num_insts', type=int, default=1000000, 
                        help='Number of instructions to simulate (default: 1000000)')
    
    # Parse the arguments
    args = parser.parse_args()

    # Define the constant path and append the file name prefix with extensions
    base_path = "../../../programs/bins/"

    elf_file_path = base_path + args.file_name_prefix 
   
    init_add,init_section ,init_size= read_section(elf_file_path,'.text.init')
    text_add,text_section,text_size = read_section(elf_file_path,'.text')
    data_add,data_section,data_size = read_section(elf_file_path,'.data')

    SimulatedRam.init_size = init_size//4
    SimulatedRam.text_size = text_size//4
    SimulatedRam.data_size = data_size//4

    SimulatedRam.init_start_add = init_add
    SimulatedRam.text_start_add = text_add
    SimulatedRam.data_start_add = data_add

    Processor.pc = SimulatedRam.init_start_add

    SimulatedRam.init_last_add = SimulatedRam.init_start_add + (SimulatedRam.init_size*4)
    SimulatedRam.text_last_add = SimulatedRam.text_start_add + (SimulatedRam.text_size*4)
    SimulatedRam.data_last_add = SimulatedRam.data_start_add + (SimulatedRam.data_size*4)

    # print(f"init sec size: {SimulatedRam.init_size}, strat add: {hex(SimulatedRam.init_start_add)}, Last add: {hex(SimulatedRam.init_last_add)}")
    # print(f"text sec size: {SimulatedRam.text_size}, strat add: {hex(SimulatedRam.text_start_add)}, Last add: {hex(SimulatedRam.text_last_add)}")
    # print(f"data sec size: {SimulatedRam.data_size}, strat add: {hex(SimulatedRam.data_start_add)}, Last add: {hex(SimulatedRam.data_last_add)}")


    load_init_section(init_section)
    load_text_section(text_section)
    if data_section is not None :
        # print(f"data section  is there")
        load_data_section(data_section)
    
    else :
        SimulatedRam.data_last_add = 0x80008000

    SimulatedRam.stack_start_add = SimulatedRam.data_last_add + 0x20000 

    

    # SimulatedRam.printInstMem()
    print("\n")
    # SimulatedRam.printDataMem()

    # Execute the instructions with the specified number of instructions
    Processor.run(args.num_insts)
