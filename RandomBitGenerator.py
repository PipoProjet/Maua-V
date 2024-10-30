import random

def set_write_mode(binary, sub_mode):
    """Set the first 3 bits to '000' for Write to Memory or '001' for Write to Registry."""
    return sub_mode + binary[3:]

def set_read_mode(binary, sub_mode):
    """Set the first 3 bits to '010' for Move in Memory or '011' for Move in Registry."""
    return sub_mode + binary[3:]

def set_alu_mode(binary, funct3, funct7):
    """
    Set the RISC-V ALU mode.
    - First 3 bits '100' for ALU instructions.
    - Insert funct3 (3 bits) and funct7 (7 bits) for ALU operations.
    """
    return '100' + binary[3:10] + funct3.zfill(3) + binary[13:25] + funct7.zfill(7)

def random_alu_operation():
    """
    Selects a random ALU operation and returns the corresponding funct3 and funct7 values.
    """
    operation_map = [
        ('000', '0000000'),  # Addition
        ('000', '0100000'),  # Subtraction
        ('001', '0000000'),  # Multiplication
        ('001', '0100000'),  # Division
        ('111', '0000000'),  # AND
        ('110', '0000000'),  # OR
        ('100', '0000000'),  # XOR
        ('101', '0000000')   # NOT
    ]
    return random.choice(operation_map)

def generate_32bit_binaries(count, mode, sub_mode=None):
    """
    Generate 32-bit binary instructions based on mode.
    Supports RISC-V-like encoding for ALU, memory, and registry instructions.
    """
    binaries = []
    for _ in range(count):
        # Generate a random 32-bit integer and convert it to binary string with padding to 32 bits
        binary_number = f'{random.getrandbits(32):032b}'
        
        # Set mode based on user input
        if mode == 'write':
            binary_number = set_write_mode(binary_number, sub_mode)
        elif mode == 'read':
            binary_number = set_read_mode(binary_number, sub_mode)
        elif mode == 'alu':
            funct3, funct7 = random_alu_operation()  # Randomly select ALU operation
            binary_number = set_alu_mode(binary_number, funct3, funct7)
        
        binaries.append(binary_number)
    return binaries

def save_to_file(binaries, filename="bits.txt"):
    """Save the generated binaries to a file."""
    with open(filename, 'w') as file:
        for binary in binaries:
            file.write(f"{binary}\n")

def main():
    """Main function to handle user input and generate appropriate 32-bit binaries."""
    try:
        # Input for number of write instructions
        write_mem_count = int(input("Enter the number of write to memory instructions: "))
        write_reg_count = int(input("Enter the number of write to registry instructions: "))
        
        # Input for number of read instructions
        read_mem_count = int(input("Enter the number of move in memory instructions: "))
        read_reg_count = int(input("Enter the number of move in registry instructions: "))
        
        # Input for number of ALU instructions
        alu_count = int(input("Enter the number of ALU instructions: "))
        
        binaries = []
        
        # Generate write to memory instructions
        if write_mem_count > 0:
            binaries += generate_32bit_binaries(write_mem_count, mode='write', sub_mode='000')
        
        # Generate write to registry instructions
        if write_reg_count > 0:
            binaries += generate_32bit_binaries(write_reg_count, mode='write', sub_mode='001')
        
        # Generate move in memory instructions
        if read_mem_count > 0:
            binaries += generate_32bit_binaries(read_mem_count, mode='read', sub_mode='010')
        
        # Generate move in registry instructions
        if read_reg_count > 0:
            binaries += generate_32bit_binaries(read_reg_count, mode='read', sub_mode='011')
        
        # Generate ALU instructions with random operations
        if alu_count > 0:
            binaries += generate_32bit_binaries(alu_count, mode='alu')
        
        # Check if at least one instruction was provided
        if not binaries:
            print("No instructions generated. Please enter a positive number for at least one instruction type.")
            return
        
        # Save all the instructions to the file
        save_to_file(binaries)
        print(f"Generated {write_mem_count + write_reg_count + read_mem_count + read_reg_count + alu_count} 32-bit binary numbers and saved to bits.txt.")
    
    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
