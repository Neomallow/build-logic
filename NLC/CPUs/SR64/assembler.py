# used to turn fibonacci.md into binary

regs = {
    'zero':0,'ra':1,'sp':2,'gp':3,'tp':4,'t0':5,'t1':6,'t2':7,'fp':8,'s1':9,
    'a0':10,'a1':11,'a2':12,'a3':13,'a4':14,'a5':15,'a6':16,'a7':17,
    's2':18,'s3':19,'s4':20,'s5':21,'s6':22,'s7':23,'s8':24,'s9':25,'s10':26,'s11':27,
    't3':28,'t4':29,'t5':30,'t6':31,'x0':0
}
def r(name):
    name = name.strip(',')
    return regs[name]

def b(v, bits):
    if v < 0:
        v = (1 << bits) + v
    return format(v, f'0{bits}b')

OPC = {
 'R':'0110011','I':'0010011','L':'0000011','S':'0100011',
 'B':'1100011','JAL':'1101111','JALR':'1100111','LUI':'0110111',
 'AUIPC':'0010111','SYS':'1110011'
}

def r_type(funct7, rs2, rs1, funct3, rd):
    return funct7 + b(rs2,5) + b(rs1,5) + funct3 + b(rd,5) + OPC['R']

def i_type(imm, rs1, funct3, rd, opcode):
    return b(imm,12) + b(rs1,5) + funct3 + b(rd,5) + opcode

def s_type(imm, rs2, rs1, funct3, opcode):
    immb = b(imm,12)
    return immb[0:7] + b(rs2,5) + b(rs1,5) + funct3 + immb[7:12] + opcode

def u_type(imm20, rd, opcode):
    return b(imm20,20) + b(rd,5) + opcode

lines = [
 ('ADDI','t0','zero','0'),
 ('ADDI','t1','zero','1'),
 ('BNE','a0','zero','L1'),
 ('ADDI','a0','zero','0'),
 ('RET',),
 ('L1',),
 ('ADDI','t2','zero','1'),
 ('BNE','a0','t2','L2'),
 ('ADDI','a0','zero','1'),
 ('RET',),
 ('L2',),
 ('ADDI','t3','zero','2'),
 ('loop',),
 ('BLT','a0','t3','done'),
 ('ADD','t4','t0','t1'),
 ('ADD','t0','t1','zero'),
 ('ADD','t1','t4','zero'),
 ('ADDI','t3','t3','1'),
 ('JAL','zero','loop'),
 ('done',),
 ('ADD','a0','t1','zero'),
 ('RET',),
]

addr = 0
labels = {}
instrs = []
for l in lines:
    if len(l) == 1 and l[0] not in ('RET',):
        labels[l[0]] = addr
    else:
        instrs.append((addr, l))
        addr += 4

def encode(addr, l):
    op = l[0]
    if op == 'ADDI':
        rd, rs1, imm = l[1], l[2], l[3]
        imm = int(imm)
        return i_type(imm, r(rs1), '000', r(rd), OPC['I'])
    if op == 'ADD':
        rd, rs1, rs2 = l[1], l[2], l[3]
        return r_type('0000000', r(rs2), r(rs1), '000', r(rd))
    if op == 'BNE':
        rs1, rs2, label = l[1], l[2], l[3]
        target = labels[label]
        offset = target - addr
        imm12 = offset >> 1
        return s_type(imm12, r(rs2), r(rs1), '001', OPC['B'])
    if op == 'BLT':
        rs1, rs2, label = l[1], l[2], l[3]
        target = labels[label]
        offset = target - addr
        imm12 = offset >> 1
        return s_type(imm12, r(rs2), r(rs1), '010', OPC['B'])
    if op == 'JAL':
        rd, label = l[1], l[2]
        target = labels[label]
        offset = target - addr
        imm20 = offset >> 1
        return u_type(imm20, r(rd), OPC['JAL'])
    if op == 'RET':
        return i_type(0, r('ra'), '000', r('zero'), OPC['JALR'])
    raise Exception("unknown "+str(l))

print(f"{'Addr':>6}  {'Label':<6} {'Instruction':<24} {'Binary':<34} {'Hex'}")
label_at = {v:k for k,v in labels.items()}
for addr, l in instrs:
    bits = encode(addr, l)
    hexv = format(int(bits,2), '08x')
    lbl = label_at.get(addr, '')
    text = ' '.join(l)
    print(f"0x{addr:04x}  {lbl:<6} {text:<24} {bits:<34} 0x{hexv}")
