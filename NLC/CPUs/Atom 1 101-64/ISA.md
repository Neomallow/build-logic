# INSTRUCTIONS
## A
## ADC
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0105 | ADC r₁, r₂ | Add with carry r₂ to r₁. | r₁ | r₂
| 0x0106 | ADC r, imm64 | Add with carry imm64 to r. | r | imm64
| 0x0107 | ADC r, imm32 | Add with carry imm32 to r. | r | imm32
| 0x0108 | ADC r, imm16 | Add with carry imm16 to r. | r | imm16
| 0x0109 | ADC r, imm8 | Add with carry imm8 to r. | r | imm8

### ADD

| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0100 | ADD r₁, r₂ | Add r₂ to r₁. | r₁ | r₂
| 0x0101 | ADD r, imm64 | Add imm64 to r. | r | imm64
| 0x0102 | ADD r, imm32 | Add imm32 to r. | r | imm32
| 0x0103 | ADD r, imm16 | Add imm16 to r. | r | imm16
| 0x0104 | ADD r, imm8 | Add imm8 to r. | r | imm8

## M
### MOV
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0200 | MOV r₁, r₂ | Move r₂ to r₁. | r₁ | r₂
| 0x0201 | MOV r, imm64 | Move imm64 to r. | r | imm64
| 0x0202 | MOV r, imm32 | Move imm32 to r. | r | imm32
| 0x0203 | MOV r, imm16 | Move imm16 to r. | r | imm16
| 0x0204 | MOV r, imm8 | Move imm8 to r. | r | imm8

## N
### NOP

| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x00 | NOP | Single-byte no operation.
| 0xFF00 | NOP | Double-byte no operation.
| 0xFFFF | NOP | Multi-byte no operation. | 0xFF *OR* 0x00 (terminator) | 0xFF *OR* 0x00 (terminator) | 0xFF *OR* 0x00 (terminator) | 0xFF *OR* 0x00 (terminator)

## S
### SBB
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0115 | SBB r₁, r₂ | Subtract with borrow r₂ from r₁. | r₁ | r₂
| 0x0116 | SBB r, imm64 | Subtract with borrow imm64 from r. | r | imm64
| 0x0117 | SBB r, imm32 | Subtract with borrow imm32 from r. | r | imm32
| 0x0118 | SBB r, imm16 | Subtract with borrow imm16 from r. | r | imm16
| 0x0119 | SBB r, imm8 | Subtract with borrow imm8 from r. | r | imm8

### SUB
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0110 | SUB r₁, r₂ | Subtract r₂ from r₁. | r₁ | r₂
| 0x0111 | SUB r, imm64 | Subtract imm64 from r. | r | imm64
| 0x0112 | SUB r, imm32 | Subtract imm32 from r. | r | imm32
| 0x0113 | SUB r, imm16 | Subtract imm16 from r. | r | imm16
| 0x0114 | SUB r, imm8 | Subtract imm8 from r. | r | imm8
