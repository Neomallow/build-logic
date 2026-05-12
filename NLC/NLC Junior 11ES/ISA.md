# Junior 11ES
## Instructions
Each instruction is 16 bits wide. The PC (Program Counter) is 12 bits wide. There are 16 registers where each is 16 bits wide. However, for many instructions, only the lower 8 bits of registers can be used, such as for ALU instructions, as the ALU is only 8 bits wide.

For every ALU instruction, the carry (CF) and zero (ZF) flags are automatically set to the corresponding value. The carry flag will always feed into ADD (A + B + CF) and SUB (A - B - CF). The zero flag does not have any impact on the ALU.
<table>
    <tr>
        <th>Opcode [decimal equivalent]</th>
        <th>Name</th>
        <th>Operand [n bits]</th>
        <th>Operand [n bits]</th>
        <th>Information</th>
    </tr>
    <tr>
      <td>0000 [0]</td>
      <td>NOP</td>
      <td>-</td>
      <td>-</td>
      <td>Wait for one clock cycle.</td>
    </tr>
    <tr>
      <td>0001 [1]</td>
      <td>JZ</td>
      <td>ADDR [12]</td>
      <td>-</td>
      <td>Set the PC to ADDR if ZF == 1.</td>
    </tr>
    <tr>
      <td>0010 [2]</td>
      <td>JNZ</td>
      <td>ADDR [12]</td>
      <td>-</td>
      <td>Set the PC to ADDR if ZF == 0.</td>
    </tr>
    <tr>
      <td>0011 [3]</td>
      <td>LOAD</td>
      <td>A [4]</td>          
      <td>IMM [8]</td>
      <td>Set value of register with address A to IMM.</td>
    </tr>
    <tr>
      <td>0100 [4]</td>
      <td>ADD</td>
      <td>A [4] <i>OR</i> IMM [8]</td>
      <td>B [4]</td>
      <td>Add the lower 8 bits of register A <i>OR</i> an immediate value to the value of register B. The result is stored in register B. B = A + B</td>
    </tr>
    <tr>
      <td>0101 [5]</td>
      <td>SUB</td>
      <td>A [4] <i>OR</i> IMM [8]</td>
      <td>B [4]</td>
      <td>Subtract the value of register B from the lower 8 bits of register A <i>OR</i> an immediate value. The result is stored in register B. B = A - B</td>
    </tr>
    <tr>
      <td>0110 [6]</td>
      <td>MUL</td>
      <td>A [4] <i>OR</i> IMM [8]</td>
      <td>B [4]</td>
      <td>Multiply the lower 8 bits of register A <i>OR</i> an immediate value with the value of register B. The result is stored in register B. B = A * B</td>
    </tr>
    <tr>
      <td>0111 [7]</td>
      <td>DIV</td>
      <td>A [4] <i>OR</i> IMM [8]</td>
      <td>B [4]</td>
      <td>Divide the lower 8 bits of register A <i>OR</i> an immediate value by the value of register B. The result is stored in register B. B = A / B</td>
    </tr>
    <tr>
      <td>1000 [8]</td>
      <td>AND</td>
      <td>A [4] <i>OR</i> IMM [8]</td>
      <td>B [4]</td>
      <td>Performs bitwise AND on the lower 8 bits of register A <i>OR</i> an immediate value and the value of register B. The result is stored in register B. B = A & B</td>
    </tr>
    <tr>
      <td>1001 [9]</td>
      <td>OR</td>
      <td>A [4] <i>OR</i> IMM [8]</td>
      <td>B [4]</td>
      <td>Performs bitwise OR on the lower 8 bits of register A <i>OR</i> an immediate value and the value of register B. The result is stored in register B. B = A | B</td>
    </tr>
    <tr>
      <td>1010 [10]</td>
      <td>MOV</td>
      <td>A [4]</td>          
      <td>B [4]</td>
      <td>Move value of register with address B to register A. Register B keeps its value.</td>
    </tr>
    <tr>
      <td>1011 [11]</td>
      <td>JC</td>
      <td>ADDR [12]</td>
      <td>-</td>
      <td>Set the PC to ADDR if CF == 1.</td>
    </tr>
    <tr>
      <td>1100 [12]</td>
      <td>STF</td>
      <td>ADDR [1]</td>
      <td>VAL [1]</td>
      <td>Set the value of the flag with the address ADDR to the value VAL.</td>
    </tr>
    <tr>
      <td>1101 [13]</td>
      <td>END</td>
      <td>-</td>
      <td>-</td>
      <td>Stop the program.</td>
    </tr>
    <tr>
      <td>1110 [14]</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
    </tr>
    <tr>
      <td>1111 [15]</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
    </tr>
</table>
