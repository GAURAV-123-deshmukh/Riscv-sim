from Disassemble import disassemble 
from Memory import SimulatedRam
from Hardware import *
from RegisterFile import RegisterFile
from FetchDecodeReg import FetchDecodereg
from DecodeExecuteReg import DecodeExecuteReg
from ExecuteMemReg import ExecuteMemReg
from MemWbReg import MemWbReg
from Clock import Clock


class Processor:
    pc = None  # Class variable for Program Counter (shared across all instances)
    stall = 0


    @classmethod
    def fetch_instruction(cls):
        if cls.pc is not None and cls.pc < SimulatedRam.text_last_add:
            FetchDecodereg.instruction = SimulatedRam.readInstrMem(cls.pc)
            FetchDecodereg.pc = cls.pc
            FetchDecodereg.stall = 0
            # print(f"{Clock.cycle_count}: fetching from pc {hex(cls.pc)}")
        else:
            FetchDecodereg.instruction = None
            FetchDecodereg.pc = None
            # print(f"{Clock.cycle_count}: {hex(cls.pc)}  afetr if None pc ----- in fetching")
            return
        cls.pc+=4

        # print(f"{Clock.cycle_count}:\t{hex(FetchDecodereg.pc)}: \t doing fetching\n")
    

    @classmethod
    def decode_instruction(cls):
        DecodeExecuteReg.pc = FetchDecodereg.pc
        
        if FetchDecodereg.instruction == None:
            # print(f"{Clock.cycle_count}: decode Pc none")
            return
        
        elif FetchDecodereg.stall :
            DecodeExecuteReg.stall = FetchDecodereg.stall
            FetchDecodereg.stall = 0
            return

        if FetchDecodereg.instruction == '00000000010000010000000100110011':
            SimulatedRam.stack_start_add = RegisterFile.read(2)
            extra_size = (SimulatedRam.stack_start_add-0x80008000)//4
            SimulatedRam.dataMem = SimulatedRam.dataMem + [0]*(extra_size - SimulatedRam.data_size)


        control_signals = control_unit(FetchDecodereg.instruction[-7:])

    # Assign control signals individually using dictionary keys
        DecodeExecuteReg.RegWrite = control_signals['RegWrite']
        DecodeExecuteReg.ALUSrc = control_signals['ALUSrc']
        DecodeExecuteReg.MemWrite = control_signals['MemWrite']
        DecodeExecuteReg.MemRead = control_signals['MemRead']
        DecodeExecuteReg.Branch = control_signals['Branch']
        DecodeExecuteReg.MemtoReg = control_signals['MemtoReg']
        DecodeExecuteReg.ALUOp = control_signals['ALUOp']
        DecodeExecuteReg.JAL = control_signals['Jump']
        DecodeExecuteReg.JALR = control_signals['JALR']
        DecodeExecuteReg.LUI = control_signals['LUI']
        DecodeExecuteReg.AUIPC = control_signals['AUIPC']
        DecodeExecuteReg.Unknown = control_signals['UnKnown']

        # calling disassemby function for rs1_ind ,rs2_ind, rd_ind etc.
        DecodeExecuteReg.instr_type,DecodeExecuteReg.instr,DecodeExecuteReg.rd_ind,DecodeExecuteReg.rs1_ind,DecodeExecuteReg.rs2_ind = disassemble(FetchDecodereg.instruction,FetchDecodereg.pc)

        

        #calling refister file for getting rs1 value and rs2 value
        DecodeExecuteReg.rs1_val = RegisterFile.read(DecodeExecuteReg.rs1_ind)
        
        if DecodeExecuteReg.rs2_ind is not None:
            DecodeExecuteReg.rs2_val = RegisterFile.read(DecodeExecuteReg.rs2_ind)

        # print
        DecodeExecuteReg.imm = imm_generation(FetchDecodereg.instruction)
        # print(f"imm is {DecodeExecuteReg.imm}")
        DecodeExecuteReg.funct3 = FetchDecodereg.instruction[-15:-12]
        DecodeExecuteReg.funct7 = FetchDecodereg.instruction[-32:-25]
        DecodeExecuteReg.stall = FetchDecodereg.stall
        # print(f"---------------- imm is {cls.imm}--------------------------->")
        # print(f"{Clock.cycle_count}:\t {hex(DecodeExecuteReg.pc)}: \tdecoding the instruction -dddddddddddddddddddddddd\t{DecodeExecuteReg.instr}\n")

        # if DecodeExecuteReg.instr_type  != 'IL':
        forwardUnitSig=forwardingUnit(DecodeExecuteReg.rs1_ind,DecodeExecuteReg.rs2_ind,ExecuteMemReg.rd_ind,MemWbReg.rd_ind)
        # print(f"fow sig is {forwardUnitSig}")
        ForwardRs1Ex=forwardUnitSig['ForwardRs1Ex']
        ForwardRs1Mem=forwardUnitSig['ForwardRs1Mem']
        ForwardRs2Ex=forwardUnitSig['ForwardRs2Ex']
        ForwardRs2Mem=forwardUnitSig['ForwardRs2Mem']
    

        if ForwardRs1Ex: 
            DecodeExecuteReg.rs1_val=ExecuteMemReg.alu_out
            # print(f"############################ rs1 val ex dr matcg  is {(ExecuteMemReg.alu_out)}")
        elif ForwardRs1Mem:
            # print(True)
            # print(f"********************####### rs1 val mem rd match is {(ExecuteMemReg.alu_out)}")
            DecodeExecuteReg.rs1_val=MemWbReg.alu_out
        if ForwardRs2Ex:
            DecodeExecuteReg.rs2_val=ExecuteMemReg.alu_out
        elif ForwardRs2Mem:
            DecodeExecuteReg.rs2_val=MemWbReg.alu_out
            # print(f"DecodiEx rs2 is {DecodeExecuteReg.rs2_val}")

        if MemWbReg.instr_type == 'IL' or ExecuteMemReg.instr_type == 'IL':
            # print(f"####### calling handler ----------------- ")
            # print(f"{hex(DecodeExecuteReg.pc)} and {ExecuteMemReg.instr_type} and mem type iis {MemWbReg.instr_type}")
            cls.handle_lw_dependecy()

        # if DecodeExecuteReg.pc is not None and DecodeExecuteReg.rs1_val is not None and DecodeExecuteReg.rs2_val is not None:
        #     print(f" last pc is {hex(DecodeExecuteReg.pc)} ################ ind is {DecodeExecuteReg.rs2_ind} and rs2 val is {DecodeExecuteReg.rs2_val}")
        

    @classmethod
    def execute_instruction(cls):
        ExecuteMemReg.pc = DecodeExecuteReg.pc
        if ExecuteMemReg.pc == None:
            # print(f"{Clock.cycle_count} pc is none in execute pxpxpxpx")
            return
        elif DecodeExecuteReg.stall:
            ExecuteMemReg.stall = DecodeExecuteReg.stall
            # print(f"{Clock.cycle_count}: stall in execute xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            return
        
        # print(f"{hex(DecodeExecuteReg.pc)}: rd_ind is  {MemWbReg.rd_ind} and rs2_ind is {DecodeExecuteReg.rs2_ind} and ex rd is {ExecuteMemReg.rd_ind} ")
        # print(f"{hex(DecodeExecuteReg.pc)}: rs1_ind decode {DecodeExecuteReg.rs1_ind} and rs2 decode {DecodeExecuteReg.rs2_ind}")
        
        # choosing value between rs2 and immediate
        alu_op2 = DecodeExecuteReg.imm if DecodeExecuteReg.ALUSrc == 1 else DecodeExecuteReg.rs2_val

        if DecodeExecuteReg.AUIPC == 1:
            ExecuteMemReg.alu_out,ExecuteMemReg.Zero = alu('add',DecodeExecuteReg.pc,DecodeExecuteReg.imm)
           
        elif DecodeExecuteReg.LUI ==1:
            ExecuteMemReg.alu_out,ExecuteMemReg.Zero = (DecodeExecuteReg.imm,0)
            
        elif DecodeExecuteReg.JAL == 1 or DecodeExecuteReg.JALR==1:
            ExecuteMemReg.alu_out,ExecuteMemReg.Zero = alu('add',DecodeExecuteReg.pc,4)

        else: 
            ops = alu_control(DecodeExecuteReg.ALUOp,DecodeExecuteReg.funct3,DecodeExecuteReg.funct7)
            if DecodeExecuteReg.rs1_val is not None and alu_op2 is not None:
                # print(f"\t ############# ind is {DecodeExecuteReg.rs1_ind}   {hex(DecodeExecuteReg.pc)} op1 is : {hex(DecodeExecuteReg.rs1_val)} op2 is {alu_op2} and instrype is {DecodeExecuteReg.instr_type}")
                # print(f"{hex(ExecuteMemReg.pc)}:  operd one is {hex(DecodeExecuteReg.rs1_val)} and op2 is {alu_op2} and ops is {ops}")
                # print(f"###  {hex(ExecuteMemReg.pc)} ops is {ops}")
                ExecuteMemReg.alu_out,ExecuteMemReg.Zero = alu(ops,DecodeExecuteReg.rs1_val,alu_op2)
                # print(f"execute alu out is {hex(ExecuteMemReg.alu_out)}")

        cls.calculageTargetAdd()
        
        ExecuteMemReg.rs2_val  = DecodeExecuteReg.rs2_val
        ExecuteMemReg.RegWrite = DecodeExecuteReg.RegWrite
        ExecuteMemReg.Branch = DecodeExecuteReg.Branch
        ExecuteMemReg.JAL = DecodeExecuteReg.JAL
        ExecuteMemReg.JALR = DecodeExecuteReg.JALR
        ExecuteMemReg.MemRead = DecodeExecuteReg.MemRead
        ExecuteMemReg.MemWrite = DecodeExecuteReg.MemWrite
        ExecuteMemReg.rd_ind = DecodeExecuteReg.rd_ind
        ExecuteMemReg.MemtoReg = DecodeExecuteReg.MemtoReg
        ExecuteMemReg.instr = DecodeExecuteReg.instr
        ExecuteMemReg.instr_type = DecodeExecuteReg.instr_type
        ExecuteMemReg.stall = DecodeExecuteReg.stall
        ExecuteMemReg.rs1_ind = DecodeExecuteReg.rs1_ind
        ExecuteMemReg.rs2_ind = DecodeExecuteReg.rs2_ind
        # print(f"{hex(ExecuteMemReg.pc)}: \tExecutuing the instruction  rs2 val is {ExecuteMemReg.rs2_val}")
        

    @classmethod
    def memory(cls):
        MemWbReg.pc = ExecuteMemReg.pc
        
        
        if MemWbReg.pc == None:
            return
        elif ExecuteMemReg.stall :
            MemWbReg.stall = ExecuteMemReg.stall
            return
        cls.updatePC()
        if ExecuteMemReg.MemRead == 1 :
            # print(f"{hex(ExecuteMemReg.pc)}: inde ins {hex(ExecuteMemReg.alu_out)}")
            MemWbReg.mem_out = SimulatedRam.readDataMem(ExecuteMemReg.alu_out)
        elif ExecuteMemReg.MemWrite == 1 :
            SimulatedRam.writeDataMem(ExecuteMemReg.alu_out,ExecuteMemReg.rs2_val)

        MemWbReg.rd_ind = ExecuteMemReg.rd_ind
        MemWbReg.MemtoReg = ExecuteMemReg.MemtoReg
        MemWbReg.RegWrite = ExecuteMemReg.RegWrite
        MemWbReg.alu_out = ExecuteMemReg.alu_out
        MemWbReg.instr = ExecuteMemReg.instr
        MemWbReg.instr_type = ExecuteMemReg.instr_type
        MemWbReg.stall = ExecuteMemReg.stall
        MemWbReg.rs2_val = ExecuteMemReg.rs2_val
        # print(f"{Clock.cycle_count}:\t {hex(MemWbReg.pc)}: \tmemory the instruction\n")
            

    @classmethod
    def writeBack(cls):
        # print(f"{Clock.cycle_count}:\t{(MemWbReg.pc)} doing the writeback")
        
        
        if MemWbReg.pc == None:
            print(f"{Clock.cycle_count}:\t\t  ################# stall #################\n")
            cls.stall+=1
            return
        elif MemWbReg.stall:
            print(f"\n{Clock.cycle_count}:\t{hex(MemWbReg.pc)}\t########## Stall ############\n")
            cls.stall+=1
            return
        
        if MemWbReg.RegWrite == 1 :
            rd_val = MemWbReg.mem_out if MemWbReg.MemtoReg else MemWbReg.alu_out
            # print(f"rd val is {hex(MemWbReg.alu_out)}")
            RegisterFile.write(MemWbReg.rd_ind,rd_val)
            # print(f"value is write is {hex(rd_val)} and ind is {MemWbReg.rd_ind}")
            # print(f"{Clock.cycle_count}:{hex(MemWbReg.pc)}  witre back phase reg is {RegisterFile.read(MemWbReg.rd_ind)}")

        if MemWbReg.pc == 0x800000d4:
            SimulatedRam.stack_start_add = RegisterFile.read(2)
            # print(hex(SimulatedRam.stack_start_add))
            extra_size = (SimulatedRam.stack_start_add-0x80008000)//4
            SimulatedRam.dataMem = SimulatedRam.dataMem + [0]*(extra_size - SimulatedRam.data_size)
        
        cls.printOut()

    @classmethod
    def calculageTargetAdd(cls):
        if DecodeExecuteReg.JALR == 1:
            ExecuteMemReg.targetAdd = DecodeExecuteReg.rs1_val + DecodeExecuteReg.imm
            print(f"value of jalr {ExecuteMemReg.targetAdd}")
            return
        
        ExecuteMemReg.targetAdd = DecodeExecuteReg.pc + DecodeExecuteReg.imm


    @classmethod
    def updatePC(cls) :
        if (ExecuteMemReg.Branch and ExecuteMemReg.Zero) or (ExecuteMemReg.JAL) or (ExecuteMemReg.JALR):
            cls.pc = ExecuteMemReg.targetAdd
            FetchDecodereg.stall = 1
            DecodeExecuteReg.stall = 1
            # ExecuteMemReg.stall = 1
            # print(f"{Clock.cycle_count} my pc is {hex(cls.pc)} and UPCUPCUPCUPCUPC")

    @classmethod
    def handle_lw_dependecy(cls):
        # print(f"calling hanlder _----------------")
        if MemWbReg.instr_type == 'IL':
            if DecodeExecuteReg.rs1_ind == MemWbReg.rd_ind and DecodeExecuteReg.rs1_ind != None:
                DecodeExecuteReg.rs1_val = MemWbReg.mem_out
                # print(f"in handler rs1_val is {DecodeExecuteReg.rs1_val}")
            if DecodeExecuteReg.rs2_ind == MemWbReg.rd_ind and DecodeExecuteReg.rs2_ind != None:
                DecodeExecuteReg.rs2_val  = MemWbReg.mem_out
        if ExecuteMemReg.instr_type == 'IL':
            if DecodeExecuteReg.rs1_ind == ExecuteMemReg.rd_ind and DecodeExecuteReg.rs1_ind != None:
                # print(f"alu out isd {hex(SimulatedRam.readDataMem(ExecuteMemReg.alu_out))}")
                DecodeExecuteReg.rs1_val = SimulatedRam.readDataMem(ExecuteMemReg.alu_out)
            
            if DecodeExecuteReg.rs2_ind == ExecuteMemReg.rd_ind and DecodeExecuteReg.rs2_ind != None:
                # print(f"I am running {DecodeExecuteReg.rs2_ind}")
                DecodeExecuteReg.rs2_val = SimulatedRam.readDataMem(ExecuteMemReg.alu_out)
        
    


    @classmethod
    def printOut(cls):
        # file  = open("mat.txt", "w")
        if DecodeExecuteReg.Unknown == 1:
            output = f"{Clock.cycle_count}: \t{hex(MemWbReg.pc)}: \t ###################### Unknown instruction ####################\n"
        elif MemWbReg.instr_type == 'R':
            output = f"{Clock.cycle_count}: \t{hex(MemWbReg.pc)}: \t{MemWbReg.instr.ljust(20)}: \t\tX{MemWbReg.rd_ind} - {hex(RegisterFile.read(MemWbReg.rd_ind))}\n"
        elif MemWbReg.instr_type == 'I':
            output = f"{Clock.cycle_count}: \t{hex(MemWbReg.pc)}: \t{MemWbReg.instr.ljust(20)}: \t\tX{MemWbReg.rd_ind} - {hex(RegisterFile.read(MemWbReg.rd_ind))}\n"
        elif MemWbReg.instr_type == 'IL':
            output = f"{Clock.cycle_count}: \t{hex(MemWbReg.pc)}: \t{MemWbReg.instr.ljust(20)}: \t\tX{MemWbReg.rd_ind} - {hex(RegisterFile.read(MemWbReg.rd_ind))}, \tmem - {hex(MemWbReg.alu_out)}\n"
        elif MemWbReg.instr_type == 'S':
            output = f"{Clock.cycle_count}: \t{hex(MemWbReg.pc)}: \t{MemWbReg.instr.ljust(20)}: \t\t{hex(MemWbReg.alu_out)} - {hex(MemWbReg.rs2_val)}, \tmem - {hex(MemWbReg.alu_out)}\n"
        elif MemWbReg.instr_type == 'B':
            output = f"{Clock.cycle_count}: \t{hex(MemWbReg.pc)}: \t{MemWbReg.instr.ljust(20)}\n"
        elif MemWbReg.instr_type == 'J':
            output = f"{Clock.cycle_count}: \t{hex(MemWbReg.pc)}: \t{MemWbReg.instr.ljust(20)}: \t\tX{MemWbReg.rd_ind} - {hex(RegisterFile.read(MemWbReg.rd_ind))}\n"
        elif MemWbReg.instr_type == 'U':
            output = f"{Clock.cycle_count}: \t{hex(MemWbReg.pc)}: \t{MemWbReg.instr.ljust(20)}: \t\tX{MemWbReg.rd_ind} - {hex(RegisterFile.read(MemWbReg.rd_ind))}\n"
        else:
            raise ValueError(f"check your instuction {cls.instruction}")
        
            # Print to console
        print(output)
        # file.write(output)

    
                    
    
    @classmethod
    def run(cls,cyc_count):
        while True:
                Clock.posEdgeClk()
                if Clock.cycle_count == 1:
                    cls.fetch_instruction()
                    print(f"{Clock.cycle_count}:\t########## NOP ##############\n")
                elif Clock.cycle_count == 2 :
                    cls.decode_instruction()
                    cls.fetch_instruction()
                    print(f"{Clock.cycle_count}:\t########## NOP ##############\n")
                elif Clock.cycle_count == 3 :
                    cls.execute_instruction()
                    cls.decode_instruction()
                    cls.fetch_instruction()
                    print(f"{Clock.cycle_count}:\t########## NOP ##############\n")
                elif Clock.cycle_count == 4 :
                    cls.memory()
                    cls.execute_instruction()
                    cls.decode_instruction()
                    cls.fetch_instruction()
                    print(f"{Clock.cycle_count}:\t########## NOP ##############\n")
                else :
                    cls.writeBack()
                    cls.memory()
                    cls.execute_instruction()
                    cls.decode_instruction()
                    cls.fetch_instruction()
                    
                
                if Clock.cycle_count >= cyc_count:
                    break
            
        print(f"\n+++++++++++++++++++++ dump  cyle count {Clock.cycle_count}: {RegisterFile.dump_registers()} ++++++++++")
        print(f"++++++++++++++++++ stalls are {cls.stall} ++++++++++++++++++++++++++++++++++\n")

