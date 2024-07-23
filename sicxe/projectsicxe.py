OPTAB = {
    "fix": [1, "c4"],
    "FLOAT": [1, "C0"],
    "HIO": [1, "F4"],
    "NORM": [1, "C8"],
    "SIO": [1, "F0"],
    "TIO": [1, "F8"],
    "ADDR": [2, "90"],
    "CLEAR": [2, "B4"],
    "COMPR": [2, "A0"],
    "DIVR": [2, "9C"],
    "MULR": [2, "98"],
    "RMO": [2, "AC"],
    "SHIFTL": [2, "A4"],
    "SHIFTR": [2, "A8"],
    "SUBR": [2, "94"],
    "SVC": [2, "B0"],
    "TIXR": [2, "B8"],
    "ADD": [3, "18"],
    "ADDF": [3, "58"],
    "AND": [3, "40"],
    "COMP": [3, "28"],
    "COMPF": [3, "88"],
    "DIV": [3, "24"],
    "DIVF": [3, "64"],
    "J": [3, "3C"],
    "JEQ": [3, "30"],
    "JGT": [3, "34"],
    "JLT": [3, "38"],
    "JSUB": [3, "48"],
    "LDA": [3, "00"],
    "LDB": [3, "68"],
    "LDCH": [3, "50"],
    "LDF": [3, "70"],
    "LDL": [3, "08"],
    "LDS": [3, "6C"],
    "LDT": [3, "74"],
    "LDX": [3, "04"],
    "LPS": [3, "D0"],
    "MUL": [3, "20"],
    "MULF": [3, "60"],
    "OR": [3, "44"],
    "RD": [3, "D8"],
    "RSUB": [3, "4C"],
    "SSK": [3, "EC"],
    "STA": [3, "0C"],
    "STB": [3, "78"],
    "STCH": [3, "54"],
    "STF": [3, "80"],
    "STI": [3, "D4"],
    "STL": [3, "14"],
    "STS": [3, "7C"],
    "STSW": [3, "E8"],
    "STT": [3, "84"],
    "STX": [3, "10"],
    "SUB": [3, "1C"],
    "SUBF": [3, "5C"],
    "TD": [3, "E0"],
    "TIX": [3, "2C"],
    "WD": [3, "DC"],
}
register = {
    "A": 0,
    "X": 1,
    "B": 4,
    "S": 5,
    "T": 6,
    "F": 7
}

# declare arrays
label = []
inst = []
ref = []
loc = []
loc_hex = []
obj = []
obj_hex = []

Format = ["ADDR", "CLEAR", "COMPR", "DIVR", "MULR", "RMO", "SHIFTL", "SHIFTR", "SUBR", "SVC", "TIXR"]

# read file
with open('C:\\Users\lap store\Desktop\project system\project.txt') as file:
    data = file.readlines()

for j in range(len(data)):
    arr = data[j].split(" ")
    if len(arr) == 3:
        label.append(arr[0].strip())
        inst.append(arr[1].strip())
        ref.append(arr[2].strip())
    elif len(arr) == 2:
        label.append("^")
        inst.append(arr[0].strip())
        ref.append(arr[1].strip())
    elif len(arr) == 1:
        label.append("^")
        inst.append(arr[0].strip())
        ref.append("^")

# location counter 1 = start
loc.append(0)
loc.append(int(ref[0]))
# pass-one
for i in range(1, len(data) - 1):
    if inst[i][0] == "+":
        number = int(loc[i]) + 4
        loc.append(int(number))
    elif inst[i] == "WORD":
        number = int(loc[i]) + 3
        loc.append(int(number))
    elif inst[i] == "BYTE":
        if ref[i][0] == "X":
            number = int((len(ref[i]) - 3) / 2)
            loc.append(int(loc[i]) + int(number))
        elif ref[i][0] == "C":
            number = int(len(ref[i]) - 3)
            loc.append(int(loc[i]) + int(number))
    elif inst[i] in Format:
        number = int(loc[i]) + 2
        loc.append(int(number))
    elif inst[i] == "RESW":
        number = int(ref[i]) * 3
        loc.append(int(loc[i]) + int(number))
    elif inst[i] == "RESB":
        number = int(ref[i])
        loc.append(int(loc[i]) + int(number))
    elif inst[i] == "BASE":
        loc.append(int(loc[i]))
    else:
        number = int(loc[i]) + 3
        loc.append(int(number))

# loc-hex
for number in loc:
    num = hex(number).lstrip("0x").zfill(4)
    loc_hex.append(num)

# print pass-one
for i in range(len(inst) - 1):
    print(f"{loc_hex[i]} : {label[i]} : {inst[i]} : {ref[i]}")

# symbol-table
print("symbol table")
for i in range(len(inst) - 1):
    if label[i] != "^":
        print(f"{loc_hex[i]} : {label[i]} ")

# location and labels in symbol table
x = []
y = []
for i in range(len(inst) - 1):
    if label[i] != "^":
        x.append(label[i])
        y.append(loc[i])

# lenght of program
lenght = loc[-1] - loc[0]
print("length of program", hex(lenght).lstrip("0x").zfill(4))

# pass-two
no_object_code = ["START", "END", "RESW", "RESB", "BASE", "RSUB\n"]
for i in range(len(data)):
    if inst[i] in no_object_code:
        obj.append("_")

    elif inst[i] == "BYTE":
        if ref[i][0] == "C":
            obj.append("ASCII")
        else:
            obj.append(ref[i][2:-1])

    # format 4
    elif inst[i][0] == "+":
        code = ""
        # opcode 6 bits
        opcode = OPTAB[inst[i][1:]][1]
        opcode1 = opcode[0]
        opcode2 = opcode[1]
        opcode1_bin = bin(int(opcode1, 16)).lstrip("0b").zfill(4)
        opcode2_bin = bin(int(opcode2, 16)).lstrip("0b").zfill(4)[:2]
        code += opcode1_bin
        code += opcode2_bin
        if ref[i][0] == "#":
            if ref[i][-1] == "X":
                # flags 6 bits
                flag_bit = "011001"
                code += flag_bit
            else:
                # flags 6 bits
                flag_bit = "010001"
                code += flag_bit
            if ref[i][1:] in x:
                index_of_ref = x.index(ref[i][1:])
                address = bin(y[index_of_ref]).lstrip("0b").zfill(20)
                code += address
            else:
                address = int(ref[i][1:])
                address_bin = bin(address).lstrip("0b").zfill(20)
                code += address_bin

        elif ref[i][0] == "@":
            if ref[i][-1] == "X":
                flag_bit = "101010"
                code += flag_bit
            else:
                flag_bit = "100010"
                code += flag_bit
            # address
        else:
            flag_bit = "110001"
            code += flag_bit
            # address
            if ref[i] in x:
                index_of_ref = x.index(ref[i])
                address = bin(y[index_of_ref]).lstrip("0b").zfill(20)
                code += address
        code_hex = hex(int(code, 2)).lstrip("0x").zfill(8)
        obj.append(code_hex)
    # format 3
    elif OPTAB[inst[i]][0] == 3:
        code = ""
        # BASE

        if inst[i] == "BASE":
            index_of_ref = x.index(ref[i])
            B = (y[index_of_ref])
        elif inst[i] == "LDB":
            index_of_ref = x.index(ref[i][1:])
            B = (y[index_of_ref])

        # opcode 6 bits
        opcode = OPTAB[inst[i]][1]
        opcode1 = opcode[0]
        opcode2 = opcode[1]
        opcode1_bin = bin(int(opcode1, 16)).lstrip("0b").zfill(4)
        opcode2_bin = bin(int(opcode2, 16)).lstrip("0b").zfill(4)[:2].zfill(2)
        code += opcode1_bin
        code += opcode2_bin

        # flags 6 bits
        if inst[i] == "RSUB":
            flag_bit = "110000"
            code += flag_bit
            # address
            address = "000000000000"
            code += address

        elif ref[i][0] == "#":
            # disp
            if ref[i][1:] in x:
                index_of_ref = x.index(ref[i][1:])
                target_address = y[index_of_ref]
                pc = loc[i + 1]
                disp = (int(target_address) - int(pc))
                if -2048 <= disp <= 2047:
                    # flags 6 bits
                    flag_bit = "010010"
                    code += flag_bit
                    if str(disp)[0] == "-":
                        disp_hex = hex(disp & (2**32-1)).lstrip("0x")[-3:]
                        disp_bin = bin(int(disp_hex, 16)).lstrip("0b")
                        code += disp_bin
                    else:
                        disp_bin = bin(disp).lstrip("0b").zfill(12)
                        code += disp_bin
                else:
                    # flags 6 bits
                    flag_bit = "010100"
                    code += flag_bit
                    disp = (int(target_address) - int(B))
                    if str(disp)[0] == "-":
                        disp_hex = hex(disp & (2 ** 32 - 1)).lstrip("0x")[-3:]
                        disp_bin = bin(int(disp_hex, 16)).lstrip("0b")
                        code += disp_bin
                    else:
                        disp_bin = bin(disp).lstrip("0b").zfill(12)
                        code += disp_bin
            else:
                # flags 6 bits
                flag_bit = "010000"
                code += flag_bit
                # address for number
                address = int(ref[i][1:])
                address_bin = bin(address).lstrip("0b").zfill(12)
                code += address_bin

        elif ref[i][0] == "@":
            # disp
            index_of_ref = x.index(ref[i][1:])
            target_address = y[index_of_ref]
            pc = loc[i + 1]
            disp = (int(target_address) - int(pc))
            if -2048 <= disp <= 2047:
                # flags 6 bits
                flag_bit = "100010"
                code += flag_bit
                if str(disp)[0] == "-":
                    disp_hex = hex(disp & (2 ** 32 - 1)).lstrip("0x")[-3:]
                    disp_bin = bin(int(disp_hex, 16)).lstrip("0b")
                    code += disp_bin
                else:
                    disp_bin = bin(disp).lstrip("0b").zfill(12)
                    code += disp_bin
            else:
                # flags 6 bits
                flag_bit = "100100"
                code += flag_bit
                disp = (int(target_address) - int(B))
                if str(disp)[0] == "-":
                    disp_hex = hex(disp & (2 ** 32 - 1)).lstrip("0x")[-3:]
                    disp_bin = bin(int(disp_hex, 16)).lstrip("0b")
                    code += disp_bin
                else:
                    disp_bin = bin(disp).lstrip("0b").zfill(12)
                    code += disp_bin
        else:
            if ref[i][-1] == "X":
                # disp
                index_of_ref = x.index(ref[i][:-2])
                target_address = y[index_of_ref]
                pc = loc[i + 1]
                disp = int(target_address) - int(pc)
                if -2048 <= disp <= 2047:
                    # flags 6 bits
                    flag_bit = "111010"
                    code += flag_bit
                    if str(disp)[0] == "-":
                        disp_hex = hex(disp & (2 ** 32 - 1)).lstrip("0x")[-3:]
                        disp_bin = bin(int(disp_hex, 16)).lstrip("0b").zfill(12)
                        code += disp_bin
                    else:
                        disp_bin = bin(disp).lstrip("0b").zfill(12)
                        code += disp_bin
                else:
                    # flags 6 bits
                    flag_bit = "111100"
                    code += flag_bit
                    disp = int(target_address) - int(B)
                    if str(disp)[0] == "-":
                        disp_hex = hex(disp & (2 ** 32 - 1)).lstrip("0x")[-3:]
                        disp_bin = bin(int(disp_hex, 16)).lstrip("0b")
                        code += disp_bin
                    else:
                        disp_bin = bin(disp).lstrip("0b").zfill(12)
                        code += disp_bin

            else:
                # disp
                index_of_ref = x.index(ref[i])
                target_address = y[index_of_ref]
                pc = loc[i + 1]
                disp = (int(target_address) - int(pc))
                if -2048 <= disp <= 2047:
                    # flags 6 bits
                    flag_bit = "110010"
                    code += flag_bit
                    if str(disp)[0] == "-":
                        disp_hex = hex(disp & (2 ** 32 - 1)).lstrip("0x")[-3:]
                        disp_bin = bin(int(disp_hex, 16)).lstrip("0b")
                        code += disp_bin
                    else:
                        disp_bin = bin(disp).lstrip("0b").zfill(12)
                        code += disp_bin
                else:
                    # flags 6 bits
                    flag_bit = "110100"
                    code += flag_bit
                    disp = (int(target_address) - int(B))
                    if str(disp)[0] == "-":
                        disp_hex = hex(disp & (2 ** 32 - 1)).lstrip("0x")[-3:]
                        disp_bin = bin(int(disp_hex, 16)).lstrip("0b")
                        code += disp_bin
                    else:
                        disp_bin = bin(disp).lstrip("0b").zfill(12)
                        code += disp_bin

        code_hex = hex(int(code, 2)).lstrip("0x").zfill(6)
        obj.append(code_hex)
    # format 2
    elif ref[i][0] != "#" and ref[i][0] != "@" and inst[i] not in no_object_code:
        code = ""
        if OPTAB[inst[i]][0] == 2:
            # opcode 8 bits
            opcode = OPTAB[inst[i]][1]
            opcode1 = opcode[0]
            opcode2 = opcode[1]
            opcode1_bin = bin(int(opcode1, 16)).lstrip("0b").zfill(4)
            opcode2_bin = bin(int(opcode2, 16)).lstrip("0b").zfill(4)
            code += opcode1_bin
            code += opcode2_bin
            # register 4 bits
            if len(ref[i]) == 3:
                first = ref[i][0]
                second = ref[i][-1]
                # register number
                register_1 = register[first]
                register_2 = register[second]
                # convert to binary
                register_1_binary = bin(register_1).lstrip("0b").zfill(4)
                register_2_binary = bin(register_2).lstrip("0b").zfill(4)
                code += register_1_binary
                code += register_2_binary
            else:
                first = ref[i][0]
                second = "0000"
                register_1 = register[first]
                register_1_binary = bin(register_1).lstrip("0b").zfill(4)
                code += register_1_binary
                code += second
        code_hex = hex(int(code, 2)).lstrip("0x")
        obj.append(code_hex)

# print pass-two
for i in range(len(inst) - 1):
    print(f" {loc_hex[i]} : {inst[i]} : {ref[i]} : {obj[i]} ")

# HTE RECORD
prog_name = label[0].zfill(6)
start = ref[0].zfill(6)
print("H", prog_name, start, hex(lenght).lstrip("0x").zfill(6))

print("E", start)





