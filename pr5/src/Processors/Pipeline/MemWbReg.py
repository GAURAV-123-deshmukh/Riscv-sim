class MemWbReg:
    pc = None
    rd_ind = None
    MemtoReg = 0
    RegWrite = 0
    mem_out = None
    alu_out = None
    instr_type = None
    instr = None
    rd_val = None
    stall = 0
    rs2_val = None
    