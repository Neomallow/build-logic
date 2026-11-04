# PREFIXES
A prefix is used to easily modify an instruction's behavior. You can only use **one** prefix per instruction.

## N
### NF
NF prohibits an instruction from updating the flags register.  
Example:
```asm
ADD 0x05, 0x06
NF ADD 0x01, 255
ADC 0x02, 0x01
```
Here, assuming `ADD 0x01, 0xFF` sets CF=1, `ADC 0x02, 0x01` would not behave as intended if you need to preserve carry from a previous instruction like `ADD 0x05, 0x06`.

## R
### REPx
REPx repeats an instruction until the condition x is false. The condition can either be a number or a flag.  
Example:
```asm
REP5 ADD 0x01, 16113
```
This will repeat `ADD 0x01, 16113` 5 times.
```asm
CMP 0x05, 103
REPNZ SUB 0x05, 1
```
This will repeat `SUB 0x05, 1` until `CMP 0x05, 103` is zero.

# INSTRUCTIONS
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
