from SupportedFun import *
from Hardware import *


def disassemble(binary_instr,pc):
    opcode = {
        "0110011": 'R', "0010011": 'I', "0000011": 'I', "0100011": 'S',
        "1100011": 'B', "1101111": 'J', "1100111": 'I', "0110111": 'U',
        "1110011": 'I', "0010111": 'U'
    }

    least_significant_7_bits = binary_instr[-7:]  # Slice the last 7 characters
   
    # R-type decoding
    if opcode.get(least_significant_7_bits) == 'R':
        rs1_ind = convert_bin_dec(binary_instr[-20:-15])
        rs2_ind = convert_bin_dec(binary_instr[-25:-20])
        rd_ind = convert_bin_dec(binary_instr[-12:-7])
        rd = "x" + str(rd_ind)
        rs1 = "x" + str(rs1_ind)
        rs2 = "x" + str(rs2_ind)
        op_str = ""
        type = 'R'
        funct3 = hex(int(binary_instr[-15:-12], 2))
        funct7 = hex(int(binary_instr[-32:-25], 2))

        if funct3 == "0x0":
            if funct7 == "0x0":
                op_str = 'add'
            elif funct7 == "0x20":
                op_str = 'sub'
            elif funct7 == '0x1':
                op_str = 'mul'
            else:
                ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x4":
            if funct7 == '0x0':
                op_str = "xor"
            elif funct7 == '0x1':
                op_str = 'div'
            else:
                ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x6":
            if funct7 == '0x0':
                op_str = "or"
            elif funct7 == '0x1':
                op_str = 'rem'
            else:
                ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x7":
            if funct7 == '0x0':
                op_str = "and"
            elif funct7 == '0x1':
                op_str = 'remu'
            else:
                ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x1":
            if funct7 == "0x0":
                op_str = "sll"
            elif funct7 == "0x1":
                op_str = 'mulh'
            else:
                ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x5":
            if funct7 == '0x0':
                op_str = "srl" 
            elif funct7 == "0x20" :
                op_str = "sra"
            elif funct7 == '0x1':
                op_str = 'divu'
            else:
                ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x2":
            if funct7 == '0x0':
                op_str = "slt"
            elif funct7 == '0x1':
                op_str = 'mulsu'
            else:
                ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x3":
            if funct7 == '0x0':
                op_str = "sltu"
                op_str = "slt"
            elif funct7 == '0x1':
                op_str = 'mulu'
            else:
                ValueError(f"funct7 field is undefined --> {hex(funct7)}")
                
        disassem_instr =  f"{op_str.ljust(8)}{rd}, {rs1}, {rs2}"
        return (type,disassem_instr,rd_ind, rs1_ind, rs2_ind)

    # I-type decoding
    if opcode.get(least_significant_7_bits) == 'I':
        rs1_ind  = convert_bin_dec(binary_instr[-20:-15])
        rd_ind = convert_bin_dec(binary_instr[-12:-7])
        rd = "x" + str(rd_ind)
        rs1 = "x" + str(rs1_ind)
        # print(f"binary instr is {binary_instr}")
        imm = int(imm_generation(binary_instr))
        op_str = ""
        funct3 = hex(int(binary_instr[-15:-12], 2))

        if least_significant_7_bits == "0010011":
            type = 'I'
            if funct3 == "0x0":
                op_str = "addi"
            elif funct3 == "0x4":
                op_str = "xori"
            elif funct3 == "0x6":
                op_str = "ori"
            elif funct3 == "0x7":
                op_str = "andi"
            elif funct3 == "0x1":
                op_str = "slli"
            elif funct3 == "0x2":
                op_str = "slti"
            elif funct3 == "0x5":
                funct7 = hex(int(binary_instr[-12:-5], 2))
                op_str = "srli" if funct7 == "0x0" else "srai"
            elif funct3 == "0x3":
                op_str = "sltui"
            #return (rd_ind, rs1_ind,None,imm)
            #return f"{op_str}      {rd},{rs1},{imm}"
            disassem_instr =  f"{op_str.ljust(8)}{rd}, {rs1}, {imm}"
            return (type,disassem_instr,rd_ind, rs1_ind,None)
        
        elif least_significant_7_bits == "0000011":
            type = 'IL'
            if funct3 == "0x0":
                op_str = "lb"
            elif funct3 == "0x1":
                op_str = "lh"
            elif funct3 == "0x2":
                op_str = "lw"
            elif funct3 == "0x4":
                op_str = "lbu"
            elif funct3 == "0x5":
                op_str = "lhu"
            #return f"{op_str}      {rd},{rs1},{imm}"
            disassem_instr =  f"{op_str.ljust(8)}{rd},({imm}){rs1}"
            return (type,disassem_instr,rd_ind, rs1_ind,None)
        
        elif least_significant_7_bits == "1100111":
            op_str = "jalr"
            type = 'I'
            #return f"{op_str}      {rd},{rs1},{imm}"
        
        elif least_significant_7_bits == "1110011":
            imm_hex = hex(imm)
            
            if imm_hex == "0x0":
                op_str = "ecall"
            else:
                op_str = "ebreak"

            type = 'I'
            #return f"{op_str}      {rs1},{rs1},{imm}"
        #alu("I",op_str,rd_ind,rs1_ind,imm)
        disassem_instr =  f"{op_str.ljust(8)}{rd},{rs1},{imm}"
        return (type,disassem_instr,rd_ind, rs1_ind,None)

    # S-type decoding
    if opcode.get(least_significant_7_bits) == 'S':
        rs1_ind = convert_bin_dec(binary_instr[-20:-15])
        rs2_ind = convert_bin_dec(binary_instr[-25:-20])
        rs1 = "x" + str(rs1_ind)
        rs2 = "x" + str(rs2_ind)
        imm = int(imm_generation(binary_instr))
        funct3 = hex(int(binary_instr[-15:-12], 2))
        op_str = ""
        type = 'S'

        if funct3 == "0x0":
            op_str = "sb"
        elif funct3 == "0x1":
            op_str = "sh"
        elif funct3 == "0x2":
            op_str = "sw"

        disassem_instr = f"{op_str.ljust(8)}{rs2}, {imm}({rs1})"
        return (type,disassem_instr,None,rs1_ind,rs2_ind)
        #return f"{op_str.ljust(8)}{rs2}, {imm_decimal}({rs1})"
        
        
    # B-type decoding
    
    if opcode.get(least_significant_7_bits) == 'B':
        rs1_ind = convert_bin_dec(binary_instr[-20:-15])
        rs2_ind = convert_bin_dec(binary_instr[-25:-20])
        rs1 = "x" + str(rs1_ind)
        rs2 = "x" + str(rs2_ind)
        imm = int(imm_generation(binary_instr))
        target_address = pc + imm
        funct3 = hex(int(binary_instr[-15:-12], 2))
        op_str = ""
        type = 'B'
        
        if funct3 == "0x0":
            op_str = "beq"
        elif funct3 == "0x1":
            op_str = "bne"
        elif funct3 == "0x4":
            op_str = "blt"
        elif funct3 == "0x5":
            op_str = "bge"
        elif funct3 == "0x6":
            op_str = "bltu"
        elif funct3 == "0x7":
            op_str = "bgeu"

        disassem_instr =  f"{op_str.ljust(8)}{rs1}, {rs2}, {hex(target_address)[2:].zfill(8)}"
        return (type,disassem_instr,None,rs1_ind,rs2_ind)
        
    # U-type decoding
    
    if opcode.get(least_significant_7_bits) == 'U':
        rd_ind = convert_bin_dec(binary_instr[-12:-7])
        rd = "x" + str(rd_ind)
        imm  = int(imm_generation(binary_instr))
        op_str = ""
        type = 'U'
        if least_significant_7_bits == "0110111":
            op_str = "lui"
            
        elif least_significant_7_bits == "0010111":
            op_str = "auipc"

        disassem_instr = f"{op_str.ljust(8)}{rd}, {imm}" 
        return (type,disassem_instr,rd_ind,None,None)  
        #return f"{op_str.ljust(8)}{rd}, {imm_decimal}"
        
    # J-type decoding
    
    if opcode.get(least_significant_7_bits) == 'J':
        rd_ind = convert_bin_dec(binary_instr[-12:-7])
        rd = "x" + str(rd_ind)

        # Extract the immediate bits in the J-type format
        imm = int(imm_generation(binary_instr))
        # Calculate the target address by adding the immediate to the program counter (PC)
        target_address = pc + imm
        op_str = "jal"  # Usually 'jal' (jump and link) is used for J-type instructions
        type = 'J'
        disassem_instr =  f"{op_str.ljust(8)}{rd}, {hex(target_address)[2:].zfill(8)}"  
        
        return (type,disassem_instr,rd_ind,None,None)  
           
    return (None,None,None,None,None)
