class ExecuteMemReg:
    pc = None
    rd_ind = None
    MemWrite = 0
    MemRead = 0
    Branch = 0
    RegWrite = 0
    MemtoReg = 0
    JAL = 0
    JALR = 0
    Zero = None
    rs2_val = None
    alu_out = None
    instr_type = None
    instr = None
    targetAdd = None
    stall = 0
    rs1_ind = None
    rs2_ind = None

