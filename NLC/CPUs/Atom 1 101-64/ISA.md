# PREFIXES
A prefix is used to easily modify an instruction's behavior. You can only use **one** prefix per instruction.

## N
### NF - No Flag Update
0x01  
NF prohibits an instruction from updating the flags register.  
Example:
```asm
ADD 0x05, 0x06
NF ADD 0x01, 255
ADC 0x02, 0x01
```
Here, assuming `ADD 0x01, 0xFF` sets CF=1, `ADC 0x02, 0x01` would not behave as intended if you need to preserve carry from a previous instruction like `ADD 0x05, 0x06`.

### NH - No High Update
0x02  
NH prohibits an instruction like MUL or DIV from updating the dedicated register at 0xFF.  
Example:
```asm
MUL 0x05, 65535
NH MUL 0x04, 0x03
```
This will preserve the high 64 bits of `MUL 0x05, 65535` in register 0xFF.

## R
### REPx - Repeat
0x03  
REPx repeats an instruction until the condition x is false, where x is a flag in the flag register.  
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
| 0x0410 | DIV r₁, r₂ | Divide r₁ by r₂ . | r₁ | r₂
| 0x0411 | DIV r, imm64 | Divide r by imm64. | r | imm64₁ | imm64₂ | imm64₃ | imm64₄ | imm64₅ | imm64₆ | imm64₇ | imm64₈
| 0x0412 | DIV r, imm32 | Divide r by imm32. | r | imm32₁ | imm32₂ | imm32₃ | imm32₄
| 0x0413 | DIV r, imm16 | Divide r by imm16. | r | imm16₁ | imm16₂
| 0x0414 | DIV r, imm8 | Divide r by imm8. | r | imm8

The remainder of the result will be stored in dedicated register at 0xFF.

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
