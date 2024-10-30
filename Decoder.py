def parse_instruction(instruction):
    """Parse a 32-bit binary string and identify the type of instruction."""
    func = instruction[:2]
    result = {}
    
    if func == '00':
        # Write in Memory (W.M.)
        result['type'] = 'Write in Memory (W.M.)'
        result['address1'] = int(instruction[2:10], 2)
        result['data'] = int(instruction[10:20], 2)
    
    elif func == '01':
        # Arithmetic and Logic Operations (A.L.O.)
        result['type'] = 'Arithmetic and Logic Operations (A.L.O.)'
        result['address1'] = int(instruction[2:10], 2)
        operation_code = int(instruction[10:14], 2)
        result['operation'] = interpret_operation(operation_code)
        result['address2'] = int(instruction[14:22], 2)
        result['result'] = int(instruction[22:32], 2)
    
    elif func == '10':
        # Move in Memory (M.M.)
        result['type'] = 'Move in Memory (M.M.)'
        result['address1'] = int(instruction[2:10], 2)
        result['aux'] = int(instruction[10:17], 2)
        result['address2'] = int(instruction[17:23], 2)
    
    return result

def interpret_operation(op_code):
    """Map the 4-bit operation code to a human-readable operation name."""
    operation_map = {
        0: 'Plus',
        1: 'Subtraction',
        2: 'Times',
        3: 'Division',
        4: 'Potentiation',
        5: 'Integer Subtraction',
        6: 'AND Gate',
        7: 'OR Gate',
        8: 'XOR Gate',
        9: 'NOT Gate',
        10: 'XNOR Gate'
    }
    return operation_map.get(op_code, "Unknown Operation")

def parse_file(filename="bits.txt"):
    """Parse the file and identify instructions for each line."""
    instructions = []
    with open(filename, 'r') as file:
        for line in file:
            instruction = line.strip()
            if len(instruction) == 32:  # Check if it's a valid 32-bit instruction
                parsed_instruction = parse_instruction(instruction)
                instructions.append(parsed_instruction)
            else:
                print(f"Skipping invalid instruction: {instruction}")
    return instructions

def main():
    """Main function to read the file and display parsed instructions."""
    instructions = parse_file("bits.txt")
    for i, instr in enumerate(instructions):
        print(f"Instruction {i+1}:")
        for key, value in instr.items():
            print(f"  {key}: {value}")
        print()

if __name__ == "__main__":
    main()
