from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_RISCV, CS_MODE_RISCV32

def read_section(file_path, section_name):
    with open(file_path, 'rb') as f:
        elf = ELFFile(f)
        
        # Get the specified section
        section = elf.get_section_by_name(section_name)
        if section is None:
            print(f"Error: {section_name} section not found in the ELF file.")
            return None, None, None
        
        # Get the starting address, raw bytes, and size of the section
        section_addr = section['sh_addr']
        section_data = section.data()
        section_size = section['sh_size']
        
        print(f"Starting address of {section_name} section: {hex(section_addr)}")
        print(f"Size of {section_name} section: {section_size} bytes")
        return section_addr, section_data, section_size

def disassemble_instructions(start_addr, code):
    # Initialize the Capstone disassembler for RISC-V (32-bit)
    md = Cs(CS_ARCH_RISCV, CS_MODE_RISCV32)
    
    # Array to store each instruction as a 32-bit binary string
    instructions = []
    
    # Disassemble each instruction, store it in the array, and print it
    print("Disassembled instructions:")
    for instruction in md.disasm(code, start_addr):
        print(f"0x{instruction.address:x}:\t{instruction.mnemonic}\t{instruction.op_str}")
        # Convert instruction bytes to 32-bit binary string and append to the list
        binary_string = ''.join(f"{byte:08b}" for byte in instruction.bytes)
        instructions.append(binary_string)
    
    return instructions

# Define arrays to store each section's instructions or data
init_section = []
text_section = []
data_section = []

# Example usage
elf_file_path = "../../../programs/bins/5-matmul.r5o"

# Read and disassemble the .text.init section
print("\n=== .text.init Section ===")
text_init_addr, text_init_data, text_init_size = read_section(elf_file_path, '.text.init')
if text_init_data:
    print(f".text.init section size: {text_init_size} bytes")
    init_section = disassemble_instructions(text_init_addr, text_init_data)

# Read and disassemble the .text section
print("\n=== .text Section ===")
text_addr, text_data, text_size = read_section(elf_file_path, '.text')
if text_data:
    print(f".text section size: {text_size} bytes")
    text_section = disassemble_instructions(text_addr, text_data)

# Read and print the .data section
print("\n=== .data Section ===")
data_addr, data_data, data_size = read_section(elf_file_path, '.data')
if data_data:
    print(f".data section size: {data_size} bytes")
    # Store each 32-bit chunk in the data section array
    for i in range(0, len(data_data), 4):
        # Convert to binary string (padding to 32 bits if necessary)
        binary_string = ''.join(f"{byte:08b}" for byte in data_data[i:i+4])
        data_section.append(binary_string)

# Print stored arrays for verification
print("\nStored .text.init section instructions (as binary strings):", init_section)
print("Stored .text section instructions (as binary strings):", text_section)
print("Stored .data section chunks (as binary strings):", data_section)
