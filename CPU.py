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
        if(reg_write == False):
            read_data.next = regs[regRead_addr]
    return write_regs,read_regs
        

@block 
def memory(clk, addr, data_in, data_out, write_enable):
    mem_size = 16
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
def and_gate(a, b, out):
    @always_comb
    def logic():    
        out.next = a & b
    return logic

@block 
def or_gate(a, b, out):
    @always_comb 
    def logic():
        out.next = a | b
    return logic

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
    
    a = Signal(0)
    b = Signal(0)
    c = Signal(0)
    d = Signal(0)
    outOR = Signal(0)
    outAND = Signal(0)
    
    and_inst = and_gate(a,b,outAND)
    or_inst = or_gate(c,d,outOR)
    mux_inst = mux(bit, clk, out, addr)
    
    
    @always(clk.posedge)
    def alu_logic():
        if(operation == 0):
            result.next = num1 + num2   
        if(operation == 1):
            result.next = num1 - num2
        if(operation == 2):
            result.next = num1 * num2
        if(operation == 3):
            result.next = num1 / num2 
        if(operation == 4):
            result.next = num1 ** num2
        if(operation == 5):
            result.next = num1 % num2
      
    return alu_logic, and_inst, mux_inst, or_inst

@block
def system():
    
    addr = Signal(intbv(0)[8:])
    data_in = Signal(intbv(0)[8:])
    data_out = Signal(intbv(0)[8:])
    write_enable = Signal(bool(0))
    clk = Signal(bool(0))

    operation = Signal(intbv(0)[4:])
    num1 = Signal(intbv(0)[8:])
    num2 = Signal(intbv(0)[8:])
    result = Signal(intbv(0)[10:])
    
    reg_write = Signal(0)
    regWrite_addr = Signal(intbv(0)[5:])
    regRead_addr = Signal(intbv(0)[5:])
    write_data = Signal(intbv(0)[8:])
    read_data = Signal(intbv(0)[8:])
    
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
            print(int(bits[0][0:2],2))
          
            if(int(bits[0][0:2],2) == 0):
                yield clk.posedge
                write_enable.next = True
                addr.next = intbv(int(bits[0][3:10],2))
                yield clk.posedge
                data_in.next = intbv(int(bits[0][11:18],2))              
            
            if(int(bits[0][0:2],2) == 1):
                yield clk.posedge
                write_enable.next = False
                regRead_addr.next = intbv(int(bits[0][3:10],2))
                yield clk.posedge
                num1.next = data_out
                operation.next = intbv(int(bits[0][11:14],2))
                yield clk.posedge 
                regRead_addr.next = intbv(int(bits[0][15:22],2))
                yield clk.posedge
                num2.next = data_out
                yield clk.posedges
                regRead_addr.next = intbv(int(bits[0][23:32],2))
                yield clk.posedge
                reg_write.next = True
                write_data.next = result
                
            del(bits[0])
            yield clk.posedge
        yield clk.posedge
        write_enable.next = False
        print("\nConteúdo da Memória:")
        for i in range(16):  # mem_size = 16
            addr.next = i
            yield clk.posedge  # Sincroniza com o clock para garantir a leitura correta
            print(f"Endereço {i:04b}: {data_out}")
    return clkgen, UC,memory_inst, alu_inst, register_inst

if __name__ == "__main__":
    # Cria os arquivos para simular no gtkwave
    tb = system()
    tb.config_sim(trace=True)
    print("Iniciou a simulação")
    try:
        tb.run_sim(1200)
    finally:
        print("Terminou a simulação")
        tb.quit_sim()