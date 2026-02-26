from FetchDecodeReg import FetchDecodereg

class DecodeExecuteReg :
    pc = None  
    ALUSrc = 0
    MemWrite = 0
    MemRead = 0
    Branch = 0
    RegWrite = 0
    MemtoReg = 0
    ALUOp = None
    JAL = 0
    JALR = 0
    LUI = 0
    AUIPC = 0
    Unknown = 0
    Zero = 0
    rs1_val = None
    rs2_val = None
    rs1_ind = None
    rs2_ind = None
    rd_ind = None
    imm = None
    instr_type = None
    instr = None
    funct3 = None
    funct7 = None
    stall = 0
