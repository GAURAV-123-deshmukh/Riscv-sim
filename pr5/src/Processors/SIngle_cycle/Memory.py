# from file import class
class SimulatedRam:
    instructionMem = []
    dataMem = []
    data_size = None
    init_size = None
    text_size = None
    init_start_add = None
    text_start_add = None
    data_start_add = None
    init_last_add = None
    text_last_add = None
    data_last_add = None
    stack_start_add = None
    stack_size = None
    stack_last_add = None

    @classmethod
    def initialize_memory(cls,data_size):
        cls.dataMem = cls.dataMem + [0] * data_size

    @classmethod
    def readInstrMem(cls,add):
        # print(f"first {cls.init_start_add} and last add is {cls.init_last_add} and add is {add}")
        if add >= cls.init_start_add and add < cls.init_last_add :
            arr_ind = (add - cls.init_start_add) // 4
            return cls.instructionMem[arr_ind]
        elif add < cls.text_last_add:
            arr_ind = (add - cls.text_start_add) // 4
            arr_ind = arr_ind + (cls.init_size)
            # print(f"arr ind :{arr_ind}: data is {cls.instructionMem[arr_ind]}------------------- and add is {hex(add)}")
            return cls.instructionMem[arr_ind]
        else:
            raise ValueError(f"Invalid InstructionMemory address - {hex(add)}")

    @classmethod 
    def readDataMem(cls,add):
        last_add_data = cls.data_start_add + (4*cls.data_size)
        if add>=  cls.data_start_add and add<last_add_data:
            arr_ind = (add - cls.data_start_add)//4
            # print(f"data sec: reading at index for add -. {hex(add)}, index is {arr_ind}")
            return cls.dataMem[arr_ind]
        elif add < cls.stack_start_add :
            arr_ind = cls.data_size + (cls.stack_start_add - add)//4
            # print(f"arr ind is {arr_ind}")
            return cls.dataMem[arr_ind]

        else:
            pass
            #raise ValueError(f"Invalid data memory address - {hex(add)}")

    @classmethod
    def writeInstrMem(cls,add,value):
        last_add_init = cls.init_start_add + (4*cls.init_size)
        last_add_text = cls.text_start_add + (4*cls.text_size)
        if add>= cls.init_start_add and add < last_add_init :
            arr_ind = (add - cls.init_start_add) // 4
            cls.instructionMem[arr_ind] = value
        elif add < last_add_text :
            arr_ind = (add - cls.text_start_add) // 4
            arr_ind = arr_ind + (cls.init_size//4)
            cls.instructionMem[arr_ind] = value
        else:
            pass
            #raise ValueError(f"Invalid InstructionMemory address - {hex(add)}")

    @classmethod 
    def writeDataMem(cls,add,value):
        last_add_data = cls.data_start_add + (4*cls.data_size)
        if add>=  cls.data_start_add and add<last_add_data:
            arr_ind = (add - cls.data_start_add)//4
            cls.dataMem[arr_ind] = value
        elif add < cls.stack_start_add :
            arr_ind = cls.data_size + (cls.stack_start_add - add)//4
            cls.dataMem[arr_ind] = value
        else:
            pass
            #raise ValueError(f"Invalid data memory address - {hex(add)} and {hex(cls.stack_start_add)}")

    @classmethod
    def printInstMem(cls):
        add = cls.init_start_add
        flag = 0
        count = 0
        for i in range(0,len(cls.instructionMem)):
            count+=1
            # print(f"{hex(add)}:\t {cls.readInstrMem(add)}")
            add+=4
            if add>= cls.init_last_add and flag == 0:
                add = cls.text_start_add
                flag = 1
                # print(f"init section has total {count} instructions -----------------------------------")
                count = 0
                
        print(f"text section has total {count} instructions -----------------------------------")
                
    
    @classmethod
    def printDataMem(cls):
        add = cls.data_start_add
        for i in range(0,len(cls.dataMem)):
            # print(f"add in data sec is {hex(add)}")
            print(f"{hex(add)}:\t {cls.readDataMem(add)}")
            add+=4
            


            
        

       

