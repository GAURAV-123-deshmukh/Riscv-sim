from elftools.elf.elffile import ELFFile

def read_section(file_path, section_name):
    with open(file_path, 'rb') as f:
        elf = ELFFile(f)

        section = elf.get_section_by_name(section_name)
        if section is None:
            # print(f"Error: {section_name} section not found in the ELF file.")
            return 0x80008000, None, 0
        
        # Get the starting address, raw bytes, and size of the section
        section_addr = section['sh_addr']
        section_data = section.data()
        section_size = section['sh_size']
        
        return section_addr, section_data, section_size
    