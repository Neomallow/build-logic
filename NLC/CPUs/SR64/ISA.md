# SR64 — Simple RISC, 64-bit
 
A minimal, orthogonal load/store ISA in the RISC-V spirit, but with its own encoding and a few different design choices (fewer formats, condition-code-free compares folded into branches, and a cleaner immediate-encoding scheme).
 
---
 
## 1. Design Goals
 
- Fixed 32-bit instruction width (no compressed extension for simplicity).
- Load/store architecture: only `LD`/`ST` touch memory.
- 32 general-purpose registers, `x0` hardwired to zero.
- Only 4 instruction formats (vs RISC-V's 6) — fewer decode cases.
- No separate comparison instructions; branches compare directly (like RISC-V, but extended to all six relations without pseudo-ops).
- No condition-code register — keeps pipelines simple and avoids hidden state.
---
 
## 2. Registers
 
| Reg | ABI name | Role |
|---|---|---|
| x0 | zero | Always reads 0, writes discarded |
| x1 | ra | Return address |
| x2 | sp | Stack pointer |
| x3 | gp | Global pointer |
| x4 | tp | Thread pointer |
| x5–x7 | t0–t2 | Temporaries |
| x8 | fp | Frame pointer |
| x9 | s1 | Saved |
| x10–x11 | a0–a1 | Args / return values |
| x12–x17 | a2–a7 | Args |
| x18–x27 | s2–s11 | Saved |
| x28–x31 | t3–t6 | Temporaries |
 
All registers are 64 bits (XLEN = 64). `pc` is a separate 64-bit program counter, not a GPR.
 
Optional `F0`–`F31` 64-bit float registers exist under the **F** extension (§7).
 
---
 
## 3. Instruction Formats (32-bit fixed width)
 
Only four formats. Opcode is always bits [6:0] (7 bits → 128 groups, plenty of room to grow).
 
```
R-type:  [ funct7 | rs2 | rs1 | funct3 | rd | opcode ]   -- reg-reg ALU
           31:25    24:20 19:15  14:12  11:7   6:0
 
I-type:  [ imm[20:9] | rs1 | funct3 | rd | opcode ]      -- imm ALU, loads, jumps
           31:20        19:15  14:12  11:7   6:0
           (12-bit signed immediate, bits 31:20)
 
S-type:  [ imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode ] -- stores, branches
           31:25         24:20 19:15  14:12   11:7      6:0
           (12-bit signed immediate, split like RISC-V's S/B, but SR64
            uses ONE split layout for both stores and branches — the
            funct3 field picks the six branch relations or the store width)
 
U-type:  [ imm[31:12] | rd | opcode ]                    -- upper-immediate, long jumps
           31:12          11:7   6:0
```
 
Rationale for merging RISC-V's S and B formats: since SR64 has no separate compare instructions, branches need the same "two source registers + signed offset" shape as stores, so one format serves both.
 
---
 
## 4. Base Integer Instructions (SR64I)
 
### Arithmetic / Logic — R-type (`opcode = 0110011`)
 
| funct3 | funct7 | Mnemonic | Operation |
|---|---|---|---|
| 000 | 0000000 | `ADD`  | rd = rs1 + rs2 |
| 000 | 0100000 | `SUB`  | rd = rs1 − rs2 |
| 001 | 0000000 | `SLL`  | rd = rs1 << rs2[5:0] |
| 010 | 0000000 | `SLT`  | rd = (rs1 < rs2) signed |
| 011 | 0000000 | `SLTU` | rd = (rs1 < rs2) unsigned |
| 100 | 0000000 | `XOR`  | rd = rs1 ^ rs2 |
| 101 | 0000000 | `SRL`  | rd = rs1 >> rs2[5:0] logical |
| 101 | 0100000 | `SRA`  | rd = rs1 >> rs2[5:0] arithmetic |
| 110 | 0000000 | `OR`   | rd = rs1 \| rs2 |
| 111 | 0000000 | `AND`  | rd = rs1 & rs2 |
 
### Immediate ALU — I-type (`opcode = 0010011`)
 
Same funct3 codes as above (`ADDI`, `SLTI`, `SLTIU`, `XORI`, `ORI`, `ANDI`, `SLLI`, `SRLI`, `SRAI` — shifts use imm[5:0] as shamt, top bits pick logical/arithmetic like R-type funct7).
 
`ADDI rd, x0, imm` is the canonical way to load a small constant (`LI` pseudo-op). `ADDI x0, x0, 0` is `NOP`.
 
### Loads — I-type (`opcode = 0000011`)
 
| funct3 | Mnemonic | Width |
|---|---|---|
| 000 | `LB`  | byte, sign-extend |
| 001 | `LH`  | halfword, sign-extend |
| 010 | `LW`  | word, sign-extend |
| 011 | `LD`  | doubleword |
| 100 | `LBU` | byte, zero-extend |
| 101 | `LHU` | halfword, zero-extend |
| 110 | `LWU` | word, zero-extend |
 
`addr = rs1 + sign_extend(imm12)`
 
### Stores — S-type (`opcode = 0100011`)
 
| funct3 | Mnemonic | Width |
|---|---|---|
| 000 | `SB` | byte |
| 001 | `SH` | halfword |
| 010 | `SW` | word |
| 011 | `SD` | doubleword |
 
`addr = rs1 + sign_extend(imm12)`, stores rs2.
 
### Branches — S-type (`opcode = 1100011`)
 
All six relations, no pseudo-instructions needed:
 
| funct3 | Mnemonic | Taken if |
|---|---|---|
| 000 | `BEQ`  | rs1 == rs2 |
| 001 | `BNE`  | rs1 != rs2 |
| 010 | `BLT`  | rs1 < rs2 (signed) |
| 011 | `BGE`  | rs1 >= rs2 (signed) |
| 100 | `BLTU` | rs1 < rs2 (unsigned) |
| 101 | `BGEU` | rs1 >= rs2 (unsigned) |
 
`target = pc + sign_extend(imm12) << 1` (±4KB range; imm12 is packed the same way as S-type stores, giving 13-bit effective reach since bit 0 is implicit 0 — same trick as RISC-V's B-type).
 
### Jumps
 
- `JAL rd, imm20` (U-type, `opcode = 1101111`): `rd = pc+4; pc = pc + sign_extend(imm20)<<1` — ±1MB range.
- `JALR rd, rs1, imm12` (I-type, `opcode = 1100111`): `rd = pc+4; pc = (rs1 + sign_extend(imm12)) & ~1` — enables indirect calls/returns and, combined with `LUI`, arbitrary 64-bit jumps.
- `RET` = pseudo-op for `JALR x0, ra, 0`.
- `CALL` = pseudo-op for `JAL ra, imm20` (or `AUIPC`+`JALR` pair for far calls).
### Upper Immediate — U-type
 
- `LUI rd, imm20` (`opcode = 0110111`): `rd = sign_extend(imm20 << 12)` — sets top bits, cleared bottom 12.
- `AUIPC rd, imm20` (`opcode = 0010111`): `rd = pc + sign_extend(imm20 << 12)` — PC-relative addressing for globals/far calls without a linker-relocatable absolute load.
Any 64-bit constant is built with a short `LUI`/`AUIPC` + `ADDI` + shift sequence (identical technique to RISC-V, e.g. `li64` macro of ~4-6 instructions).
 
### System (`opcode = 1110011`)
 
| Mnemonic | Function |
|---|---|
| `ECALL`  | Environment call (syscall trap) |
| `EBREAK` | Debugger breakpoint trap |
| `FENCE`  | Memory ordering barrier |
 
That's the entire base — **~45 instructions**, comparable to RV64I.
 
---
 
## 5. Extensions (optional, detected via a feature-ID CSR)
 
- **M** — Integer multiply/divide: `MUL`, `MULH`, `MULHU`, `MULHSU`, `DIV`, `DIVU`, `REM`, `REMU` (R-type, new funct7).
- **A** — Atomics: `LR`/`SC` (load-reserved/store-conditional) plus `AMOSWAP`, `AMOADD`, `AMOAND`, `AMOOR`, `AMOXOR`, `AMOMIN(U)`, `AMOMAX(U)`.
- **F/D** — IEEE-754 single/double float, separate register file, standard `FADD`, `FSUB`, `FMUL`, `FDIV`, `FSQRT`, `FCVT`, `FMADD`-style fused ops, and float branches via `FEQ`/`FLT`/`FLE` writing to a GPR (kept out of the base to avoid forcing float hardware on microcontrollers).
- **C** — Optional 16-bit compressed encoding for common instructions (`ADDI`, `LD`, `SD`, branches, `MV`), mixed with 32-bit ones like RISC-V's C extension, for code-density-sensitive targets.
This mirrors RISC-V's modular philosophy: a compliant "SR64G" (general-purpose) core is IMAFD, while embedded cores can ship base-only.
 
---
 
## 6. Why these deviations from RISC-V
 
| Choice | Reason |
|---|---|
| 4 formats instead of 6 | Simpler decoder; S-type reused for both stores and branches since SR64 has no compare-and-set instructions competing for that shape. |
| No `SLTI`-style condition codes feeding branches | Branches compare directly, so common `if`/`while` code is 1 instruction instead of 2 (compare-then-branch), at the cost of a slightly wider branch-comparator in hardware — a good trade for a simple pipeline. |
| Feature-ID CSR for extension discovery | Software can probe capabilities at boot without needing separate ISA-string parsing. |
| Kept opcode field at 7 bits | Same headroom as RISC-V for future growth, without over-engineering a 6-format spec for a "simple" ISA. |
 
---
 
## 7. Example: Loop Summing an Array
 
```asm
    # a0 = pointer, a1 = count, a2 = accumulator (return value)
    ADDI a2, x0, 0        # sum = 0
    ADDI t0, x0, 0        # i = 0
loop:
    BGE  t0, a1, done      # if i >= count, exit
    SLLI t1, t0, 3         # t1 = i * 8
    ADD  t2, a0, t1        # t2 = &arr[i]
    LD   t3, 0(t2)         # t3 = arr[i]
    ADD  a2, a2, t3        # sum += arr[i]
    ADDI t0, t0, 1         # i++
    JAL  x0, loop
done:
    RET
```
 
Eight instructions, no compare-then-branch overhead, register-only loop control — same density class as RV64I.
 
