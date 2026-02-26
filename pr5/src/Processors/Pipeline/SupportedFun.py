def convert_bin_dec(binary_val):
    return int(int(binary_val, 2))

def twos_complement_to_int(bin_data):
    bits = len(bin_data)  # Determine the number of bits
    if bin_data[0] == '1':  # Check if the number is negative (MSB is 1)
        # Apply two's complement conversion for negative numbers
        integer_value = -((1 << bits) - int(bin_data, 2))
        # print(f"ingert val {integer_value}")
    else:
        # Directly convert if the number is positive
        integer_value = int(bin_data, 2)
    return integer_value

