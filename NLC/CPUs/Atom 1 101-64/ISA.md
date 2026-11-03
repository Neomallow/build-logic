# INSTRUCTIONS
## A
## ADC
| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0100 | ADC r₁, r₂ | Add with CF r₂ to r₁. | r₁ | r₂
| 0x0101 | ADC r, imm64 | Add with CF imm64 to r. | r | imm64
| 0x0102 | ADC r, imm32 | Add with CF imm32 to r. | r | imm32
| 0x0103 | ADC r, imm16 | Add with CF imm16 to r. | r | imm16
| 0x0104 | ADC r, imm8 | Add with CF imm8 to r. | r | imm8

### ADD

| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x0100 | ADD r₁, r₂ | Add r₂ to r₁. | r₁ | r₂
| 0x0101 | ADD r, imm64 | Add imm64 to r. | r | imm64
| 0x0102 | ADD r, imm32 | Add imm32 to r. | r | imm32
| 0x0103 | ADD r, imm16 | Add imm16 to r. | r | imm16
| 0x0104 | ADD r, imm8 | Add imm8 to r. | r | imm8




## N
### NOP

| Opcode | Instruction | Description | Operand 1 | Operand 2 | Operand 3 | Operand 4 |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| 0x00 | NOP | Do nothing for one cycle.
