from SupportedFun import *
def alu(ops, operand1, operand2):
    result = 0
    zero_flag = 0  

    # Perform the ALU operation based on `ops`
    if ops == 'add':
        result = operand1 + operand2
        # result = twos_complement_to_int(bin(result))
        # print(bin(result))
    elif ops == 'sub':
        result = operand1 - operand2
        zero_flag = 1 if result == 0 else 0
    elif ops == 'and':
        # print(f"pc is {}")
        result = operand1 & operand2
    elif ops == 'or':
        result = operand1 | operand2
    elif ops == 'xor':
        result = operand1 ^ operand2
        zero_flag = 1 if result != 0 else 0
    elif ops == 'sll':  # Shift left logical
        result = operand1 << operand2
        # print(f"hex is {hex(result)} and oopes2 -   = {operand2} and op1 = {operand1}")
        if operand2 >= 31:
            result = twos_complement_to_int(f'{result:b}')
            # print(f"result is {result}")
    elif ops == 'srl':  # Shift right logical
        result = operand1 >> operand2
        result = twos_complement_to_int(f'{result:b}')
    elif ops == 'sra':  # Shift right arithmetic
        result = (operand1 >> operand2) | ((operand1 & 0x80000000) * (operand2 > 0))
    elif ops == 'slt':  # Set Less Than (signed)
        # print(f"oper1: {hex(operand1)} and oper2 {operand2}-------------------------->")
        result = 1 if operand1 < operand2 else 0
        zero_flag = 1 if result == 1 else 0
    elif ops == 'sltu':  # Set Less Than (unsigned)
        result = 1 if (operand1 & 0xFFFFFFFF) < (operand2 & 0xFFFFFFFF) else 0
    elif ops == 'mul':
        result = operand1 * operand2
    elif ops == 'div':
        result = operand1 / operand2
    elif ops == 'divu':
        result = operand1/operand2
    elif ops == 'rem':
        result = operand1 % operand2
    elif ops == 'remu':
        result = operand1%operand2
    elif ops == 'sgt':
        result = 1 if operand2 < operand1 else 0
        zero_flag = 1 if result == 1 else 0
    elif ops == 'mulh':
        result = operand1 * operand1
        result = result >> 32
    elif ops == 'mulu' or 'mulsu':
        result = operand1 * operand2
        result = result >> 32
    else:
        # print(f"Unknown operation '{ops}'")
        return 0, 0  # Return zero result and zero_flag if operation is unknown

    return result, zero_flag

    
def control_unit(opcode):
    control_signals = {
        'RegWrite': 0,
        'ALUSrc': 0,
        'MemWrite': 0,
        'MemRead': 0,
        'Branch': 0,
        'MemtoReg': 0,
        'ALUOp': None,  # ALUOp will be used to select the ALU operation
        'Jump': 0,      # New signal for jump instructions
        'JALR': 0,
        'LUI':0,
        'AUIPC':0,
        'UnKnown':0
    }

    # Decoding based on the opcode
    if opcode == '0110011':  # R-type (e.g., add, sub, and, or)
        control_signals['RegWrite'] = 1  # Writes result to rd
        control_signals['ALUOp'] = '10'  # ALUOp = '10' means R-type operation
        

    elif opcode == '0010011':  # I-type (e.g., addi, slli)
        control_signals['RegWrite'] = 1  # Writes result to rd
        control_signals['ALUSrc'] = 1    # Use immediate (imm) as the second ALU operand
        control_signals['ALUOp'] = '11'  # ALUOp = '00' means I-type operation

    elif opcode == '0000011':  # Load (e.g., lw)
        control_signals['RegWrite'] = 1  # Write to rd
        control_signals['ALUSrc'] = 1    # Use immediate (imm) as the second ALU operand
        control_signals['MemRead'] = 1   # Read from memory
        control_signals['MemtoReg'] = 1  # Write memory result to rd
        control_signals['ALUOp'] = '00'  # ALU computes the effective address

    elif opcode == '0100011':  # Store (e.g., sw)
        control_signals['ALUSrc'] = 1    # Use immediate (imm) as the second ALU operand
        control_signals['MemWrite'] = 1  # Write to memory
        control_signals['ALUOp'] = '00'  # ALU computes the effective address

    elif opcode == '1100011':  # Branch (e.g., beq)
        control_signals['Branch'] = 1    # Perform a branch
        control_signals['ALUSrc'] = 0    # Use rs2 as the second ALU operand
        control_signals['ALUOp'] = '01'  # ALU performs a subtraction to compare

    elif opcode == '1101111':  # J-type (e.g., jal)
        control_signals['RegWrite'] = 1  # Writes to rd (for jal, stores PC+4 in rd)
        control_signals['ALUSrc'] = 1    # ALU uses immediate for address calculation
        control_signals['Jump'] = 1      # Enable jump
        control_signals['ALUOp'] = '00'  # ALU computes the target address
        # print(f"value od ALUOp is {control_signals['ALUOp']}")

    elif opcode == '1100111':
        control_signals['JALR'] = 1
        control_signals['ALUOp'] = '00'
        control_signals['ALUSrc'] = 1
        control_signals['RegWrite'] = 1

    elif opcode == '0010111':  # U-type (e.g., auipc)
        control_signals['RegWrite'] = 1  # Write result to rd
        control_signals['ALUSrc'] = 1    # Use immediate for ALU source
        control_signals['AUIPC'] = 1  # Perform address calculation

    elif opcode == '0110111':  # U-type (e.g., lui)
        control_signals['RegWrite'] = 1  # Writes immediate value to rd
        control_signals['ALUSrc'] = 1    # Use immediate (imm) as the operand
        control_signals['ALUOp'] = None  # Unique ALU operation for lui
        control_signals['LUI'] = 1

    elif opcode == '0010111':  # U-type (e.g., auipc)
        control_signals['RegWrite'] = 1  # Writes immediate value to rd
        control_signals['ALUSrc'] = 1    # Use immediate (imm) as the operand
        control_signals['ALUOp'] = None  # Unique ALU operation for lui
        control_signals['AUIPC'] = 1

    elif opcode == '1100111':            # for jalr-0I-type
        control_signals['RegWrite'] = 1  # Writes to rd (for jal, stores PC+4 in rd)
        control_signals['ALUSrc'] = 1    # ALU uses immediate for address calculation
        control_signals['JALR'] = 1      # Enable jump
        control_signals['ALUOp'] = '00'  # ALU computes the target address

    else:
        control_signals['UnKnown'] = 1
    #     # print(f"XXXXXXXXXX  Warning: Unknown opcode {opcode} XXXXXXXXX")

    # Return the control signals to be used in the pipeline
    return control_signals




def imm_generation(instruction):
     # If instruction is a string, convert it to an integer
     # If instruction is a string, assume it's a binary string and convert to integer
    if isinstance(instruction, str):
        if instruction.isdigit():  # If the string is pure digits, treat it as binary
            instruction = int(instruction, 2)
        else:
            raise ValueError("Instruction must be a binary string of 32 digits")
        
    # Extract the opcode (bits [6:0])
    opcode = instruction & 0x7F

    # Initialize the immediate value
    immediate = 0

    # I-Type instructions (e.g., addi, load)
    if opcode in [0x03, 0x13, 0x67]:  # Load, I-type ALU, JALR
        imm_11_0 = (instruction >> 20) & 0xFFF  # Bits [31:20]
        immediate = sign_extend(imm_11_0, 12)
        # immediate = twos_complement(immediate)
    
    

    # S-Type instructions (e.g., store)
    elif opcode == 0x23:  # Store
        imm_11_5 = (instruction >> 25) & 0x7F   # Bits [31:25]
        imm_4_0 = (instruction >> 7) & 0x1F     # Bits [11:7]
        imm_combined = (imm_11_5 << 5) | imm_4_0  # Combine into 12-bit immediate
        immediate = sign_extend(imm_combined, 12) # Sign extend to 32 bits
        #print(f"s : {immediate}")

    # B-Type instructions (e.g., branch)
    elif opcode == 0x63:  # Branch
        imm_12 = (instruction >> 31) & 0x1      # Bit [31]
        imm_10_5 = (instruction >> 25) & 0x3F   # Bits [30:25]
        imm_4_1 = (instruction >> 8) & 0xF      # Bits [11:8]
        imm_11 = (instruction >> 7) & 0x1       # Bit [7]
        imm_combined = (imm_12 << 12) | (imm_11 << 11) | (imm_10_5 << 5) | (imm_4_1 << 1)
        immediate = sign_extend(imm_combined, 13)  # Sign extend 13-bit immediate
        # immediate = twos_complement(immediate)
        #print(f"B : {immediate}")

    # U-Type instructions (e.g., lui, auipc)
    elif opcode in [0x37, 0x17]:  # LUI, AUIPC
        imm_31_12 = instruction & 0xFFFFF000  # Bits [31:12]
        immediate = imm_31_12  # No need to sign extend, already 32 bits
        

    # J-Type instructions (e.g., jal)
    elif opcode == 0x6F:  # JAL
        # print(f"instr is {bin(instruction)}")
        imm_20 = (instruction >> 31) & 0x1       # Bit [31]
        imm_10_1 = (instruction >> 21) & 0x3FF   # Bits [30:21]
        # print(f"bits from 30:20 means 10:1 is {bin(imm_10_1)}")
        imm_11 = (instruction >> 20) & 0x1       # Bit [20]
        imm_19_12 = (instruction >> 12) & 0xFF   # Bits [19:12]
        imm_combined = (imm_20 << 20) | (imm_19_12 << 12) | (imm_11 << 11) | (imm_10_1 << 1)
        # print(f"imm_combined is {bin(imm_combined)}")
        immediate = sign_extend(imm_combined, 21)  # Sign extend 21-bit immediate
        # print(f"immediate is : {bin(immediate)}")
        # immediate = twos_complement(immediate)
        # print(f"immemdiate is after 2's comple: {bin(immediate)}")
    

    #print(immediate)

    return immediate

def sign_extend(value, bits):
    if (value >> (bits - 1)) & 1:  # If the sign bit is set
        # Extend with 1s for negative values
        result = value | (~((1 << bits) - 1))
    else:
        result = value  # Positive values remain unchanged

    return result

       
# Inside Hardware.py module
def alu_control(AluOp, funct3, funct7=None):
    # Initialize ALU control signal to None
    alu_control_signal = None

    # AluOp values based on instruction type
    if AluOp == '00':  # Load/Store
        alu_control_signal = 'add'  # ALU should perform addition

    elif AluOp == '01':  # Branch
        if funct3 == '000':
            alu_control_signal = 'sub'  # Subtract for BEQ
        elif funct3 == '001':
            alu_control_signal = 'xor'  # Use XOR for BNE
        elif funct3 == '100':
            alu_control_signal = 'slt'
        elif funct3 == '101':
            alu_control_signal = 'sgt'

    elif AluOp == '10':  # R-type instruction
        # Examine funct3 and funct7 to decide operation
        funct3 = hex(int(funct3,2))
        funct7  = hex(int(funct7,2))
        if funct3 == "0x0":
            if funct7 == "0x0":
                alu_control_signal = 'add'
            elif funct7 == "0x20":
                alu_control_signal = 'sub'
            elif funct7 == '0x1':
                alu_control_signal = 'mul'
            else:
                raise ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x4":
            if funct7 == '0x0':
                alu_control_signal = "xor"
            elif funct7 == '0x1':
                alu_control_signal = 'div'
            else:
                raise ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x6":
            if funct7 == '0x0':
                alu_control_signal = "or"
            elif funct7 == '0x1':
                alu_control_signal = 'rem'
            else:
                raise ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x7":
            if funct7 == '0x0':
                alu_control_signal = "and"
            elif funct7 == '0x1':
                alu_control_signal = 'remu'
            else:
                raise ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x1":
            if funct7 == "0x0":
                alu_control_signal = "sll"
            elif funct7 == "0x1":
                alu_control_signal = 'mulh'
            else:
                raise ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x5":
            if funct7 == '0x0':
                alu_control_signal = "srl" 
            elif funct7 == "0x20" :
                alu_control_signal = "sra"
            elif funct7 == '0x1':
                alu_control_signal = 'divu'
            else:
                raise ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x2":
            if funct7 == '0x0':
                alu_control_signal = "slt"
            elif funct7 == '0x1':
                alu_control_signal = 'mulsu'
            else:
                raise ValueError(f"funct7 field is undefined --> {hex(funct7)}")

        elif funct3 == "0x3":
            if funct7 == '0x0':
                alu_control_signal = "sltu"
                alu_control_signal = "slt"
            elif funct7 == '0x1':
                alu_control_signal = 'mulu'
            else:
                raise ValueError(f"funct7 field is undefined --> {hex(funct7)}")

    elif AluOp == '11':  # Immediate instructions (I-type)
        if funct3 == '000':
            alu_control_signal = 'add'  # ADDI
        elif funct3 == '001' and funct7 == '0000000':
            alu_control_signal = 'sll'  # SLLI
        elif funct3 == '010':
            alu_control_signal = 'slt'  # SLTI (Set Less Than Immediate)
        elif funct3 == '011':
            alu_control_signal = 'sltu'  # SLTIU (Set Less Than Unsigned Immediate)
        elif funct3 == '100':
            alu_control_signal = 'xor'  # XORI
        elif funct3 == '101':
            if funct7 == '0000000':
                alu_control_signal = 'srl'  # SRLI (Shift Right Logical Immediate)
            elif funct7 == '0100000':
                alu_control_signal = 'sra'  # SRAI (Shift Right Arithmetic Immediate)
        elif funct3 == '110':
            alu_control_signal = 'or'  # ORI
        elif funct3 == '111':
            alu_control_signal = 'and'  # ANDI
    
    return alu_control_signal



def forwardingUnit(rs1,rs2,ExMemRd,MemWbRd):
    fowrdUnitSig = {
        'ForwardRs1Ex':0,
        'ForwardRs1Mem':0,
        'ForwardRs2Ex':0,
        'ForwardRs2Mem':0
    }

    if rs2==ExMemRd and rs2!=0:
        fowrdUnitSig['ForwardRs2Ex']=1
    elif rs2==MemWbRd and rs2!=0:
        fowrdUnitSig['ForwardRs2Mem']=1

    if rs1==ExMemRd and rs1!=0:
        fowrdUnitSig['ForwardRs1Ex']=1
    elif rs1==MemWbRd and rs1!=0:
        fowrdUnitSig['ForwardRs1Mem']=1

    return fowrdUnitSig








