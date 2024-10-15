import random

def set_write_mode(binary, sub_mode):
    """Set the first 3 bits to '000' for Write to Memory or '001' for Write to Registry."""
    return sub_mode + binary[3:]

def set_read_mode(binary, sub_mode):
    """Set the first 3 bits to '010' for Move in Memory or '011' for Move in Registry."""
    return sub_mode + binary[3:]

def set_alu_mode(binary, alu_operation):
    """Set the first 3 bits to '100' for ALU mode, and insert the operation in bits 11-14."""
    return '100' + binary[3:10] + alu_operation + binary[15:32]

def generate_32bit_binaries(count, mode, sub_mode=None, alu_operation=None):
    binaries = []
    for _ in range(count):
        # Generate a random 32-bit integer and convert it to a binary string with padding to 32 bits
        binary_number = f'{random.getrandbits(32):032b}'
        
        # Set mode based on user input: write/read/alu
        if mode == 'write':
            binary_number = set_write_mode(binary_number, sub_mode)
        elif mode == 'read':
            binary_number = set_read_mode(binary_number, sub_mode)
        elif mode == 'alu':
            binary_number = set_alu_mode(binary_number, alu_operation)
        
        binaries.append(binary_number)
    return binaries

def save_to_file(binaries, filename="bits.txt"):
    """Save the generated binaries to a file."""
    with open(filename, 'w') as file:
        for binary in binaries:
            file.write(f"{binary}\n")

def choose_alu_operation():
    """Prompt the user to choose an ALU operation and return the corresponding 4-bit binary."""
    print("Choose an ALU operation:")
    print("0: Addition")
    print("1: Subtraction")
    print("2: Multiplication")
    print("3: Division")
    print("4: AND")
    print("5: OR")
    print("6: XOR")
    print("7: NOT")
    
    choice = input("Enter the number of the ALU operation (0-7): ").strip()
    
    operation_map = {
        '0': '0000',  # Addition
        '1': '0001',  # Subtraction
        '2': '0010',  # Multiplication
        '3': '0011',  # Division
        '4': '0100',  # AND
        '5': '0101',  # OR
        '6': '0110',  # XOR
        '7': '0111'   # NOT
    }
    
    if choice in operation_map:
        return operation_map[choice]
    else:
        print("Invalid operation. Defaulting to Addition (0000).")
        return '0000'  # Default to addition if invalid input

def main():
    """Main function to handle user input and generate the appropriate 32-bit binaries."""
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
        
        # Generate ALU instructions
        if alu_count > 0:
            alu_operation = choose_alu_operation()  # Ask user to choose ALU operation
            binaries += generate_32bit_binaries(alu_count, mode='alu', alu_operation=alu_operation)
        
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
