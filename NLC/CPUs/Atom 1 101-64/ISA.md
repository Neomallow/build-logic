# REGISTERS
There are 256 general purpose registers from 0x00 to 0xFF, where 0xFF is the dedicated high ALU output register.
Separately, there is a flag register, a program counter and a call stack.

## FLAGS
- Carry CF - 0x00
- Borrow BF - 0x01
- Zero ZF - 0x02
- Overflow OF - 0x03
- Parity PF - 0x04
- Sign SF - 0x05

# PREFIXES
A prefix is used to easily modify an instruction's behavior. You can only use **one** prefix per instruction.

## N
### NF - No Flag Update
0x00  
NF prohibits an instruction from updating the flags register.  
Example:
```asm
ADD 0x05, 0x06
NF ADD 0x01, 255
ADC 0x02, 0x01
```
Here, assuming `ADD 0x01, 0xFF` sets CF=1, `ADC 0x02, 0x01` would not behave as intended if you need to preserve carry from a previous instruction like `ADD 0x05, 0x06`.

### NH - No High Update
0x01  
NH prohibits an instruction like MUL or DIV from updating the dedicated register at 0xFF.  
Example:
```asm
MUL 0x05, 65535
NH MUL 0x04, 0x03
```
This will preserve the high 64 bits of `MUL 0x05, 65535` in register 0xFF.

## R
### REPc - Repeat
0x1c  
REPx repeats an instruction until the condition c is false, where c is a flag in the flag register.  
Example:
```asm
CMP 0x05, 103
REPNZ SUB 0x05, 1
```
This will repeat both `CMP 0x05, 103` and `SUB 0x05, 1` until `CMP 0x05, 103` is zero.  
1. Execute `CMP 0x05, 103`.
2. Update flags.
3. Execute `SUB 0x05, 1` if NZ==1, jump past if not.
4. Update flags.
5. Repeat.

# INSTRUCTIONS
All immediates are **unsigned**. If you want to do signed math, you will have to do it manually.

## FORMAT
| Prefix | Opcode | Operand 1 | Operand 2 | Operand 3 | Operand 4 | Operand 5 | Operand 6 | Operand 7 | Operand 8 | Operand 9
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 95:88 | 87:72 | 71:64 | 63:56 | 55:48 | 47:40 | 39:32 | 31:24 | 23:16 | 15:8 | 7:0 

## A
### ADC - Add With Carry
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 | Operand 5 | Operand 6 | Operand 7 | Operand 8 | Operand 9
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0105 | ADC r₁, r₂ | Add with carry r₂ to r₁. | r₁ | r₂
| 0x0106 | ADC r, imm64 | Add with carry imm64 to r. | r | imm64₁ | imm64₂ | imm64₃ | imm64₄ | imm64₅ | imm64₆ | imm64₇ | imm64₈
| 0x0107 | ADC r, imm32 | Add with carry imm32 to r. | r | imm32₁ | imm32₂ | imm32₃ | imm32₄
| 0x0108 | ADC r, imm16 | Add with carry imm16 to r. | r | imm16₁ | imm16₂
| 0x0109 | ADC r, imm8 | Add with carry imm8 to r. | r | imm8

### ADD - Add
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 | Operand 5 | Operand 6 | Operand 7 | Operand 8 | Operand 9
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0100 | ADD r₁, r₂ | Add r₂ to r₁. | r₁ | r₂
| 0x0101 | ADD r, imm64 | Add imm64 to r. | r | imm64₁ | imm64₂ | imm64₃ | imm64₄ | imm64₅ | imm64₆ | imm64₇ | imm64₈
| 0x0102 | ADD r, imm32 | Add imm32 to r. | r | imm32₁ | imm32₂ | imm32₃ | imm32₄
| 0x0103 | ADD r, imm16 | Add imm16 to r. | r | imm16₁ | imm16₂
| 0x0104 | ADD r, imm8 | Add imm8 to r. | r | imm8

## D
### DIV - Divide
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 | Operand 5 | Operand 6 | Operand 7 | Operand 8 | Operand 9
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0410 | DIV r₁, r₂ | Divide r₁ by r₂. | r₁ | r₂
| 0x0411 | DIV r, imm64 | Divide r by imm64. | r | imm64₁ | imm64₂ | imm64₃ | imm64₄ | imm64₅ | imm64₆ | imm64₇ | imm64₈
| 0x0412 | DIV r, imm32 | Divide r by imm32. | r | imm32₁ | imm32₂ | imm32₃ | imm32₄
| 0x0413 | DIV r, imm16 | Divide r by imm16. | r | imm16₁ | imm16₂
| 0x0414 | DIV r, imm8 | Divide r by imm8. | r | imm8

The remainder of the result will be stored in dedicated register at 0xFF.

### DRC - Draw Character
| Opcode | Instruction | Description | Operand 1 | Operand 2 
| ----------- | ----------- | ----------- | ----------- | ----------- 
| 0x0500 | DRC r₁, r₂ | Draw character r₁ at screen position r₂. | r₁ | r₂
| 0x0501 | DRC r, imm16 | Draw character r at screen position imm16. | r | imm16₁ | imm16₂
| 0x0502 | DRC imm8, r | Draw character imm8 at screen position r. | imm8 | r
| 0x0503 | DRC imm8, imm16 | Draw character imm8 at screen position imm16. | imm8 | imm16₁ | imm16₂

#### Character Encoding
The lower 7 bits of the register or immediate are used.

0000000 =   
0000001 = a  
0000010 = b  
0000011 = c  
0000100 = d  
0000101 = e  
0000110 = f  
0000111 = g  
0001000 = h  
0001001 = i  
0001010 = j  
0001011 = k  
0001100 = l  
0001101 = m  
0001110 = n  
0001111 = o  
0010000 = p  
0010001 = q  
0010010 = r  
0010011 = s  
0010100 = t  
0010101 = u  
0010110 = v  
0010111 = w  
0011000 = x  
0011001 = y  
0011010 = z  
0011011 = 1  
0011100 = 2  
0011101 = 3  
0011110 = 4  
0011111 = 5  

0100000 = 6  
0100001 = 7  
0100010 = 8  
0100011 = 9  
0100100 = 0  
0100101 = -  
0100110 = =  
0100111 = .  
0101000 = ,  
0101001 = ;  
0101010 = /  
0101011 = à  
0101100 = â  
0101101 = ç  
0101110 = è  
0101111 = é   
0110000 = ê    
0110001 = î  
0110010 = ï  
0110011 = û  
0110100 = |  
0110101 = \[  
0110110 = ]  
0110111 = "  
0111000 = 🟧  
0111001 = 🟨  
0111010 = 🟩  
0111011 = 🟦  
0111100 = 🟪  
0111101 = ⬜  
0111110 = ▶  
0111111 =   

1000000 =   
1000001 = A   
1000010 = B   
1000011 = C  
1000100 = D  
1000101 = E  
1000110 = F  
1000111 = G  
1001000 = H  
1001001 = I  
1001010 = J  
1001011 = K  
1001100 = L  
1001101 = M  
1001110 = N  
1001111 = O  
1010000 = P  
1010001 = Q  
1010010 = R  
1010011 = S  
1010100 = T  
1010101 = U  
1010110 = V  
1010111 = W  
1011000 = X  
1011001 = Y  
1011010 = Z  
1011011 = !  
1011100 = @  
1011101 = #  
1011110 = $  
1011111 = %  

1100000 = ?  
1100001 = &  
1100010 = *  
1100011 = (  
1100100 = )  
1100101 = _  
1100110 = +  
1100111 = .  
1101000 = '  
1101001 = :  
1101010 = ~  
1101011 = À  
1101100 = Â  
1101101 = Ç  
1101110 = È  
1101111 = É  
1110000 = Ê  
1110001 = Ì  
1110010 = Ï  
1110011 = Û  
1110100 = ¦  
1110101 = {  
1110110 = }  
1110111 = ^  
1111000 = >   
1111001 = <  
1111010 = █  
1111011 = ➡  
1111100 = ⬅  
1111101 = ⬆  
1111110 = ⬇  
1111111 =  

#### Screen Coordinates
0-6: x  
8-15: y

## J
### JMP - Jump
| Opcode | Instruction | Description | Operand 1 | Operand 2
| ----------- | ----------- | ----------- | ----------- | -----------
| 0x0300 | JMP r | Jump indirect to program counter address r. | r
| 0x0301 | JMP imm8 | Jump short direct to program counter address imm8. | imm8
| 0x0302 | JMP imm16 | Jump far direct to program counter address imm16. | imm16₁ | imm16₂
| 0x0310 | JMP r | Jump relative indirect to program counter address += signed r. | r
| 0x0311 | JMP imm8 | Jump relative short direct to program counter address += signed imm8. | imm8
| 0x0312 | JMP imm16 | Jump relative far direct to program counter address += signed imm16. | imm16₁ | imm16₂

## M
### MOV - Move
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 | Operand 5 | Operand 6 | Operand 7 | Operand 8 | Operand 9
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0200 | MOV r₁, r₂ | Move r₂ to r₁. | r₁ | r₂
| 0x0201 | MOV r, imm64 | Move imm64 to r. | r | imm64₁ | imm64₂ | imm64₃ | imm64₄ | imm64₅ | imm64₆ | imm64₇ | imm64₈
| 0x0202 | MOV r, imm32 | Move imm32 to r. | r | imm32₁ | imm32₂ | imm32₃ | imm32₄
| 0x0203 | MOV r, imm16 | Move imm16 to r. | r | imm16₁ | imm16₂
| 0x0204 | MOV r, imm8 | Move imm8 to r. | r | imm8

### MUL - Multiply
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 | Operand 5 | Operand 6 | Operand 7 | Operand 8 | Operand 9
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0400 | MUL r₁, r₂ | Multiply r₂ with r₁ and store in r₁. | r₁ | r₂
| 0x0401 | MUL r, imm64 | Multiply imm64 with r and store in r. | r | imm64₁ | imm64₂ | imm64₃ | imm64₄ | imm64₅ | imm64₆ | imm64₇ | imm64₈
| 0x0402 | MUL r, imm32 | Multiply imm32 with r and store in r. | r | imm32₁ | imm32₂ | imm32₃ | imm32₄
| 0x0403 | MUL r, imm16 | Multiply imm16 with r and store in r. | r | imm16₁ | imm16₂
| 0x0404 | MUL r, imm8 | Multiply imm8 with r and store in r. | r | imm8

The higher 64 bits of the result will be stored in the dedicated register at 0xFF.

## N
### NOP - No Operation
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 | Operand 5 | Operand 6 | Operand 7 | Operand 8
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x00 | NOP | Single-byte no operation.
| 0xFF00 | NOP | Double-byte no operation.
| 0xFFFF | NOP | Multi-byte no operation. | 0xFF *OR* 0x00 (terminator) | 0xFF *OR* 0x00 (terminator) | 0xFF *OR* 0x00 (terminator) | 0xFF *OR* 0x00 (terminator) | 0xFF *OR* 0x00 (terminator) | 0xFF *OR* 0x00 (terminator) | 0xFF *OR* 0x00 (terminator) | 0xFF *OR* 0x00 (terminator)

## S
### SBB - Subtract With Borrow
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 | Operand 5 | Operand 6 | Operand 7 | Operand 8 | Operand 9
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0115 | SBB r₁, r₂ | Subtract with borrow r₂ from r₁. | r₁ | r₂
| 0x0116 | SBB r, imm64 | Subtract with borrow imm64 from r. | r | imm64₁ | imm64₂ | imm64₃ | imm64₄ | imm64₅ | imm64₆ | imm64₇ | imm64₈
| 0x0117 | SBB r, imm32 | Subtract with borrow imm32 from r. | r | imm32₁ | imm32₂ | imm32₃ | imm32₄
| 0x0118 | SBB r, imm16 | Subtract with borrow imm16 from r. | r | imm16₁ | imm16₂
| 0x0119 | SBB r, imm8 | Subtract with borrow imm8 from r. | r | imm8

### SUB - Subtract
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 | Operand 5 | Operand 6 | Operand 7 | Operand 8 | Operand 9
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0110 | SUB r₁, r₂ | Subtract r₂ from r₁. | r₁ | r₂
| 0x0111 | SUB r, imm64 | Subtract imm64 from r. | r | imm64₁ | imm64₂ | imm64₃ | imm64₄ | imm64₅ | imm64₆ | imm64₇ | imm64₈
| 0x0112 | SUB r, imm32 | Subtract imm32 from r. | r | imm32₁ | imm32₂ | imm32₃ | imm32₄
| 0x0113 | SUB r, imm16 | Subtract imm16 from r. | r | imm16₁ | imm16₂
| 0x0114 | SUB r, imm8 | Subtract imm8 from r. | r | imm8
