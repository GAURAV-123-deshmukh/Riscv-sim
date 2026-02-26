class RegisterFile:
    # Private class-level array to represent the 32 registers
    __registers = [0] * 32

    @classmethod
    def read(cls, read_reg1=None):
        if read_reg1 == None :
            return None
        if not (-1 < read_reg1 < 32):
            raise ValueError("Register numbers must be between 0 and 31")

        # Read data from the first register
        read_data1 = cls.__registers[read_reg1]

        return read_data1

    @classmethod
    def write(cls, write_reg, write_data):
        if not (-1 < write_reg < 32):
            raise ValueError("Register number must be between 0 and 31")
        if write_reg  !=0:
            cls.__registers[write_reg] = write_data

    @classmethod
    def dump_registers(cls):
        """Displays the current state of all registers."""
        for i in range(32):
            print(f"x{i}: {(cls.__registers[i])}")
