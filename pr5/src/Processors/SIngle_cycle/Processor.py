from Disassemble import disassemble 
from Memory import SimulatedRam
from Hardware import *
from RegisterFile import RegisterFile


class Processor:
    pc = None  # Class variable for Program Counter (shared across all instances)
    cycle_count = 1   # Class variable for cycle count

    # Class variables for instruction details
    instr_type = None
    instr = None
    rs1_ind = None
    rs2_ind = None
    rd_ind = None
    RegWrite = 0
    ALUSrc = 0
    MemWrite = 0
    MemRead = 0
    Branch = 0
    MemtoReg = 0
    ALUOp = None
    JAL = 0
    JALR = 0
    LUI = 0
    AUIPC = 0
    Unknown = 0
    Zero = 0
    imm = None
    ops = None
    rs1_val = None
    rs2_val = None
    alu_op2 = None
    rd_val = None
    mem_read_val = None
    alu_out = None
    mem_out = None
    funct3 = None
    funct7 = None
    instruction = None

    @classmethod
    def fetch_instruction(cls):
        if cls.pc is not None:
            return SimulatedRam.readInstrMem(cls.pc)
        else:
            raise ValueError("pc is None -----------------------------------")
    

    @classmethod
    def decode_instruction(cls, instruction):
        control_signals = control_unit(instruction[-7:])

    # Assign control signals individually using dictionary keys
        cls.RegWrite = control_signals['RegWrite']
        cls.ALUSrc = control_signals['ALUSrc']
        cls.MemWrite = control_signals['MemWrite']
        cls.MemRead = control_signals['MemRead']
        cls.Branch = control_signals['Branch']
        cls.MemtoReg = control_signals['MemtoReg']
        cls.ALUOp = control_signals['ALUOp']
        cls.JAL = control_signals['Jump']
        cls.JALR = control_signals['JALR']
        cls.LUI = control_signals['LUI']
        cls.AUIPC = control_signals['AUIPC']
        cls.Unknown = control_signals['UnKnown']

        # calling disassemby function for rs1_ind ,rs2_ind, rd_ind etc.
        cls.instr_type,cls.instr,cls.rd_ind, cls.rs1_ind, cls.rs2_ind = disassemble(instruction,cls.pc)

        

        #calling refister file for getting rs1 value and rs2 value
        cls.rs1_val = RegisterFile.read(cls.rs1_ind)
        if cls.rs2_ind is not None:
            cls.rs2_val = RegisterFile.read(cls.rs2_ind)

        cls.imm = imm_generation(instruction)
        cls.funct3 = instruction[-15:-12]
        cls.funct7 = instruction[-32:-25]
        # print(f"---------------- imm is {cls.imm}--------------------------->")
        

    @classmethod
    def execute_instruction(cls):
        # choosing value between rs2 and immediate
        cls.alu_op2 = cls.imm if cls.ALUSrc == 1 else cls.rs2_val

        if cls.AUIPC == 1:
            # print(f"immediate is {cls.imm}")
            cls.alu_out,cls.Zero = alu('add',cls.pc,cls.imm)
            # print(f"result is {hex(cls.alu_out)}")
        elif cls.LUI ==1:
            cls.alu_out,cls.Zero = alu('srl',cls.imm,12)
        elif cls.JAL == 1 or cls.JALR==1:
            # print(f"Immediate is {cls.imm}")
            cls.alu_out,cls.Zero = alu('add',cls.pc,4)
        else: 
            cls.ops = alu_control(cls.ALUOp,cls.funct3,cls.funct7)
            if cls.rs1_val is not None and cls.alu_op2 is not None:
                # print(f"operand one is {cls.rs1_val} + {cls.alu_op2}")
                cls.alu_out,cls.Zero = alu(cls.ops,cls.rs1_val,cls.alu_op2)
        cls.updatePC()
        
        

    @classmethod
    def memory(cls):
        if cls.MemRead == 1 :
            # print(f"{cls.alu_out}---------------------------------> alu out ")
            cls.mem_out = SimulatedRam.readDataMem(cls.alu_out)
        elif cls.MemWrite == 1 :
            SimulatedRam.writeDataMem(cls.alu_out,cls.rs2_val)
            

    @classmethod
    def writeBack(cls):
        if cls.MemtoReg == 0 :    
            cls.mem_out = cls.alu_out
        if cls.RegWrite == 1 :
            RegisterFile.write(cls.rd_ind,cls.mem_out)


    @classmethod
    def printOut(cls, type,pc_curr):
        # file  = open("mat.txt", "w")
        if cls.Unknown == 1:
            output = f"{cls.cycle_count}: \t{hex(pc_curr)}: \t ###################### Unknown instruction ####################\n"
        elif type == 'R':
            output = f"{cls.cycle_count}: \t{hex(pc_curr)}: \t{cls.instr.ljust(20)}: \t\tX{cls.rd_ind} - {hex(int(cls.mem_out))}\n"
        elif type == 'I':
            output = f"{cls.cycle_count}: \t{hex(pc_curr)}: \t{cls.instr.ljust(20)}: \t\tX{cls.rd_ind} - {hex(cls.mem_out)}\n"
        elif type == 'IL':
            # print(f"rd_ind: {cls.rd_ind}, mem_out: {(cls.mem_out)}, alu)out - ;{(hex(cls.alu_out))}")
            output = f"{cls.cycle_count}: \t{hex(pc_curr)}: \t{cls.instr.ljust(20)}: \t\tX{cls.rd_ind} - {hex(cls.mem_out)}, \tmem - {hex(cls.alu_out)}\n"
        elif type == 'S':
            output = f"{cls.cycle_count}: \t{hex(pc_curr)}: \t{cls.instr.ljust(20)}: \t\t{hex(cls.alu_out)} - {hex(cls.rs2_val)}, \tmem - {hex(cls.alu_out)}\n"
        elif type == 'B':
            output = f"{cls.cycle_count}: \t{hex(pc_curr)}: \t{cls.instr.ljust(20)}\n"
        elif type == 'J':
            output = f"{cls.cycle_count}: \t{hex(pc_curr)}: \t{cls.instr.ljust(20)}: \t\tX{cls.rd_ind} - {hex(cls.mem_out)}\n"
        elif type == 'U':
            output = f"{cls.cycle_count}: \t{hex(pc_curr)}: \t{cls.instr.ljust(20)}: \t\tX{cls.rd_ind} - {hex(cls.mem_out)}\n"
        else:
            raise ValueError(f"check your instuction {cls.instruction}")
        
            # Print to console
        print(output)
        # file.write(output)

    @classmethod
    def updatePC(cls) :
        if (cls.Branch and cls.Zero) or (cls.JAL == 1) :
            cls.pc = cls.pc + cls.imm
        elif cls.JALR == 1 :
            cls.pc = cls.rs1_val + cls.imm
        else :
            cls.pc += 4
    



    @classmethod
    def run(cls,cyc_count):
        while True:
            try:
                pc_curr = cls.pc
                #fetch instruction
                cls.instruction = cls.fetch_instruction()
                # print(instruction)
               

                # Decode the fetched instruction
                cls.decode_instruction(cls.instruction)

                # Execute the fetched instruction
                cls.execute_instruction()
                
                # #memory operations
                cls.memory()

                # # # #write back
                cls.writeBack()

                if cls.instruction == '00000000010000010000000100110011':
                    SimulatedRam.stack_start_add = RegisterFile.read(2)
                    # print(hex(SimulatedRam.stack_start_add))
                    extra_size = (SimulatedRam.stack_start_add-0x80008000)//4
                    SimulatedRam.dataMem = SimulatedRam.dataMem + [0]*(extra_size - SimulatedRam.data_size)


                # printing the output
                cls.printOut(cls.instr_type,pc_curr)

                cls.cycle_count += 1
                
                if cls.cycle_count > cyc_count:
                    break
            except IndexError:
                print(f"pc is {hex(cls.pc)} and {cls.instr}, alu_out is {hex(cls.alu_out)}")
                print("Reached end of text memory.")
                break
        print(f"dump {cls.cycle_count}: {RegisterFile.dump_registers()}")
        # print(f"Total cycles executed: {cls.cycle_count}")

