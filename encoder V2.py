linhas=[]
while(True):
    print("Digite o tipo da instrução")
    print("1 - W.M.")
    print("2 - W.R.")
    print("3- A.L.O.")
    print("4- M.M.")
    print("5- M.R.")
    print("6- M.R.M.")
    print("7- M.M.R.")
    print("8- Sair")
    tipo =int(input("Digite o numero da instrução: "))
    if(tipo == 1):
        addr1 = int(input("Digite o endereço da memória: "))
        value = int(input("Digite o valor para escrever na memória: "))
        linhas.append('000'+str(format(addr1, 'b').zfill(8))+str(format(value, 'b').zfill(8))+'0000000000000\n')
    if(tipo == 2):
        addr1 = int(input("Digite o endereço do registrador: "))
        value = int(input("Digite o valor para escrever no registrador: "))
        linhas.append('001'+str(format(addr1, 'b').zfill(5))+str(format(value, 'b').zfill(8))+'0000000000000000\n')
    if(tipo == 3):
        num1 = int(input("Digite o endereço do numero no registrador: "))
        print("0- (+)")
        print("1- (-)")
        print("2- (*)")
        print("3- (/)")
        print("4- (**)")
        print("5- (%)")
        print("6- AND")
        print("7- OR")
        print("8- NAND")
        print("9- NOR")
        print("10- XOR")
        print("11- XNOR")
        print("12- NOT")
        operation= int(input("Digite o numero da operação: "))
        num2 = int(input("Digite o endereço do numero no registrador: "))
        result = int(input("Digite o endereço no qual o resultado será salvo: "))
        linhas.append('010'+str(format(num1, 'b').zfill(5))+str(format(operation, 'b').zfill(5))+str(format(num2, 'b').zfill(5))+str(format(result, 'b').zfill(5))+'000000000\n')
    if(tipo == 4):
        addr1 = int(input("Digite o endereço da memoria de base: "))
        aux = int(input("Digite o endereço da memoria do auxiliar: "))
        addr2 = int(input("Digite o endereço da memoria do destino: "))
        linhas.append('011'+str(format(addr1, 'b').zfill(8))+str(format(aux, 'b').zfill(8))+str(format(addr2, 'b').zfill(8))+'00000\n')
    if(tipo == 5):
        addr1 = int(input("Digite o endereço do registrador de base: "))
        aux = int(input("Digite o endereço do registrador do auxiliar: "))
        addr2 = int(input("Digite o endereço do registrador do destino: "))
        linhas.append('100'+str(format(addr1, 'b').zfill(5))+str(format(aux, 'b').zfill(5))+str(format(addr2, 'b').zfill(5))+'00000000000000\n')
    if(tipo == 6):
       addr1 = int(input("Digite o endereço do registrador de base: "))
       addr2 = int(input("Digite o endereço da memória de destino: "))
       linhas.append('101'+str(format(addr1, 'b').zfill(5))+str(format(addr2, 'b').zfill(8))+'0000000000000000\n')
    if(tipo == 7):
       addr1 = int(input("Digite o endereço da memória de base: "))
       addr2 = int(input("Digite o endereço do registrador de destino: "))
       linhas.append('110'+str(format(addr1, 'b').zfill(8))+str(format(addr2, 'b').zfill(5))+'0000000000000000\n')
    if(tipo == 8):
        addr1 = int(input("Digite o endereço do registrador que deseja limpar: "))
        linhas.append('111'+str(format(addr1, 'b').zfill(5))+'000000000000000000000\n')
    if(tipo ==9):
        break
    print(linhas)
with open("bits.txt", "w") as arquivo:
    arquivo.writelines(linhas)

    