from myhdl import block, Signal, always_comb, Simulation, delay, traceSignals, instance, always,intbv
from random import randrange

bits = []

with open('bits.txt','r') as file:
   for linha in file:
       bits.append(linha.strip())
       
print(bits)

@block 
def register(clk, reg_write, regWrite_addr, regRead_addr, write_data, read_data):
    regs = [Signal(intbv(0)[32:]) for i in range(32)]
    
    @always(clk.posedge)
    def write_regs():
        if(reg_write):
            regs[regWrite_addr].next = write_data
    
    @always_comb
    def read_regs():
        read_data.next = regs[regRead_addr]
    return write_regs,read_regs
        

@block 
def memory(clk, addr, data_in, data_out, write_enable):
    mem_size = 256
    mem = [Signal(intbv(0)[10:]) for i in range(mem_size)]
    
    @always(clk.posedge)
    def write():
        if write_enable:
            mem[addr].next = data_in
    @always_comb
    def read():
        if write_enable == 0:
            data_out.next = mem[addr]
    return write, read

@block 
def mux(bit,clk,out,addr):
    @always(clk.posedge)
    def mux_logic():
        out.next=bit[addr]
    return mux_logic

@block 
def ALU(operation,num1,num2,result,clk):
    
    out = Signal(0)
    bit = Signal(intbv(0)[8:])
    addr = Signal(intbv(0)[3:])

    mux_inst = mux(bit, clk, out, addr)
    
    
    @always(clk.posedge)
    def alu_logic():
        if(operation == 0):
            result.next = num1 + num2
        elif(operation == 1):
            result.next = num1 - num2
        elif(operation == 2):
            result.next = num1 * num2
        elif(operation == 3):
            result.next = num1 / num2 
        elif(operation == 4):
            result.next = num1 ** num2
        elif(operation == 5):
            result.next = num1 % num2
        elif(operation == 6):
            result.next = num1 & num2
        elif(operation == 7):
            result.next = num1 | num2
        elif(operation == 8):
            result.next = ~(num1 & num2)
        elif(operation == 9):
            result.next = ~(num1 | num2)
        elif(operation == 10):
            result.next = num1 ^ num2
        elif(operation == 11):
            result.next = ~(num1 ^ num2)
        elif(operation == 12):
            result.next = ~(num1)
      
    return alu_logic,mux_inst

@block
def system():
    
    addr = Signal(intbv(0)[8:])
    data_in = Signal(intbv(0)[8:])
    data_out = Signal(intbv(0)[8:])
    write_enable = Signal(bool(0))
    clk = Signal(bool(0))

    operation = Signal(intbv(0)[5:])
    num1 = Signal(intbv(0)[8:])
    num2 = Signal(intbv(0)[8:])
    result = Signal(intbv(0)[14:])
    
    reg_write = Signal(0)
    regWrite_addr = Signal(intbv(0)[5:])
    regRead_addr = Signal(intbv(0)[5:])
    write_data = Signal(intbv(0)[8:])
    read_data = Signal(intbv(0)[8:])
    
    aux = Signal(intbv(0)[8:])
    aux1 = Signal(intbv(0)[8:])
    
    alu_inst = ALU(operation, num1,num2,result,clk)
    memory_inst = memory(clk, addr, data_in,data_out, write_enable)
    register_inst = register(clk, reg_write, regWrite_addr, regRead_addr, write_data, read_data)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance  
    def UC():
        for linha in bits:
            if len(linha) < 32:
                raise ValueError("Todas as intruções tem que ter no mínimo 32 bits")
        while(len(bits) > 0):            
            
            #Write in Memory
            if(int(bits[0][0:3],2) == 0):
                yield clk.posedge
                write_enable.next = True
                addr.next = intbv(int(bits[0][4:11],2))
                yield clk.posedge
                data_in.next = intbv(int(bits[0][12:19],2))     
           
            #Write in Registers
            if(int(bits[0][0:3],2) == 1):
                yield clk.posedge
                reg_write.next = True
                regWrite_addr.next = intbv(int(bits[0][4:8],2))
                yield clk.posedge
                write_data.next = intbv(int(bits[0][9:16],2))        
            
            #Do Func
            if(int(bits[0][0:3],2) == 2):
      
                yield clk.posedge
                reg_write.next = False
                regRead_addr.next = intbv(int(bits[0][4:8], 2)) 
                yield clk.posedge  
                num1.next = read_data
                yield clk.posedge
                regRead_addr.next = intbv(int(bits[0][14:18], 2))  
                yield clk.posedge  
                num2.next = read_data
                yield clk.posedge
                operation.next = intbv(int(bits[0][9:13], 2))
                yield clk.posedge 
                reg_write.next = True
                regWrite_addr.next = intbv(int(bits[0][19:23], 2)) 
                yield clk.posedge 
                write_data.next = result
                
            #Move in memory
            if(int(bits[0][0:3],2) == 3):
                
                yield clk.posedge 
                write_enable.next = False
                addr.next = intbv(int(bits[0][9:13],2))
                yield clk.posedge
                aux1.next = data_out
                yield clk.posedge 
                write_enable.next = False
                addr.next = intbv(int(bits[0][4:8],2))
                yield clk.posedge
                aux.next = data_out
                yield clk.posedge
                addr.next = intbv(int(bits[0][9:13],2))
                write_enable.next = True
                data_in.next = aux
                yield clk.posedge
                write_enable.next = False
                addr.next = intbv(int(bits[0][14:18],2))
                yield clk.posedge
                aux.next = data_out
                yield clk.posedge
                addr.next = intbv(int(bits[0][4:8],2))
                write_enable.next = True
                data_in.next = aux
                yield clk.posedge
                write_enable.next = False
                addr.next = intbv(int(bits[0][9:13],2))
                yield clk.posedge
                aux.next = data_out
                yield clk.posedge
                addr.next = intbv(int(bits[0][14:18],2))
                write_enable.next = True
                data_in.next = aux
                yield clk.posedge
                addr.next = intbv(int(bits[0][9:13],2))
                write_enable.next = True
                data_in.next = aux1
            
            #Move in registers
            if(int(bits[0][0:3],2) == 4):
                
                yield clk.posedge 
                reg_write.next = False
                regRead_addr.next = intbv(int(bits[0][9:13],2))
                yield clk.posedge
                aux1.next = read_data
                yield clk.posedge 
                reg_write.next = False
                regRead_addr.next = intbv(int(bits[0][4:8],2))
                yield clk.posedge
                aux.next = read_data
                yield clk.posedge
                regWrite_addr.next = intbv(int(bits[0][9:13],2))
                reg_write.next = True
                write_data.next = aux
                yield clk.posedge
                reg_write.next = False
                regRead_addr.next = intbv(int(bits[0][14:18],2))
                yield clk.posedge
                aux.next = read_data
                yield clk.posedge
                regWrite_addr.next = intbv(int(bits[0][4:8],2))
                reg_write.next = True
                write_data.next = aux
                yield clk.posedge
                reg_write.next = False
                regRead_addr.next = intbv(int(bits[0][9:13],2))
                yield clk.posedge
                aux.next = read_data
                yield clk.posedge
                regWrite_addr.next = intbv(int(bits[0][14:18],2))
                reg_write.next = True
                write_data.next = aux
                yield clk.posedge
                regWrite_addr.next = intbv(int(bits[0][9:13],2))
                reg_write.next = True
                write_data.next = aux1
                
            #Move Registers to Memory
            if(int(bits[0][0:3],2) == 5):
        
                yield clk.posedge
                reg_write.next = False
                regRead_addr.next = intbv(int(bits[0][4:8],2))
                yield clk.posedge
                write_enable.next = True
                addr.next = intbv(int(bits[0][9:16],2))
                yield clk.posedge
                data_in.next = read_data
            
            #Move Memory to Register
            if(int(bits[0][0:3],2) == 6):
                
                yield clk.posedge
                write_enable.next = False
                addr.next = intbv(int(bits[0][4:11],2))
                yield clk.posedge
                reg_write.next = True
                regWrite_addr.next = intbv(int(bits[0][12:16],2))
                yield clk.posedge
                write_data.next = data_out
            
            #Remove Register
            if(int(bits[0][0:3],2) == 7):
                
                yield clk.posedge
                reg_write.next = True
                regWrite_addr.next = intbv(int(bits[0][4:8],2))
                yield clk.posedge
                write_data.next = 0
                               
            del(bits[0])
            yield clk.posedge
        yield clk.posedge
        
        write_enable.next = False
        reg_write.next = False
        
        print("\nConteúdo dos Registradores:")
        for i in range(32):  
            regRead_addr.next = i
            yield clk.posedge  
            print(f"Registrador {i:04b}: {read_data}")
        
        print("\nConteúdo da Memória:")
        for i in range(16):  
            addr.next = i
            yield clk.posedge  
            print(f"Endereço {i:04b}: {data_out}")
            
    return clkgen, UC, memory_inst, alu_inst, register_inst

if __name__ == "__main__":
    # Cria os arquivos para simular no gtkwave
    tb = system()
    tb.config_sim(trace=True)
    print("Iniciou a simulação")
    try:
        tb.run_sim(5000)
    finally:
        print("Terminou a simulação")
        tb.quit_sim()