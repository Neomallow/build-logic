# Atom o1L
Please note this is an asynchronous CPU. Instead of a set clock cycle the CPU uses a handshaking protocol to move on to the next instruction as soon as the previous one is finished. This makes a NOP operation useless and sometimes even dangerous.
There is a hardware timer which you can change to a specific interval with the minimum being 0.05s and the maximum 300s. The default is 0.5s.

## Registers
There are 65536 registers in total, each being 64 bits wide. If a value were to exceed 64 bits, everything exceeding the 64 bits would be lost.
They are usually addressed by 16 bits and 8 bit offset or 16 bits and 16 bit offset.
Why so many? Build Logic (on Roblox) has a 16 bit EEPROM block, and 4 of those chained together is the simplest (and fastest) way to make a 64 bit register. Silly? Yes. Efficient? Also yes. So don't complain.
R0, the register with address 0, is hardwired to 0.

## RAM
RAM is not integrated into the CPU. Hence here only theoretical limits will be defined.
RAM can have a maximum of 2^32 (4294967296) cells.

## Instructions
Instructions are formatted in [ OPCODE [8] | OPERAND [8] | OPERAND [16] | OPERAND [16] | OPERAND [16] ]

In case an operand is not fully used, the lower bits will be used, for example JMP's 2nd operand. Here a 2 (0b10) would look like 00000000000**00010** instead of **00010**00000000000.
<table>
    <tr>
        <th>Opcode</th>
        <th>Name</th>
        <th>Operand [bits]</th>
        <th>Operand [bits]</th>
        <th>Operand [bits]</th>
        <th>Operand [bits]</th>
        <th>Information</th>
    </tr>
    <tr>
      <td>00000000 [0]</td>
      <td>HLT</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
      <td>Stops the instruction-fetch cycle until an external interrupt is fired.</td>
    </tr>
    <tr>
      <td>00000001 [1]</td>
      <td>MOV</td>
      <td>-</td>
      <td>R1 [16]</td>
      <td>R2 [16]</td>
      <td>OFFSET [16]</td>
      <td>Copies the data in R2 into R1 left-shifted by the <i>word</i> offset.</td>
    </tr>
    <tr>
      <td>00000010 [2]</td>
      <td>MOVI</td>
      <td>OFFSET [8]</td>
      <td>R1 [16]</td>
      <td>IMM [16]</td>
      <td>IMM [16]</td>
      <td>Overwrites the data in R1 with the immediate left-shifted by the <i>word</i> offset.</td>
    </tr>
    <tr>
      <td>00000011 [3]</td>
      <td>LOADB</td>
      <td>OFFSET [8]</td>
      <td>R1 [16]</td>
      <td>RAM [16]</td>
      <td>RAM [16]</td>
      <td>Moves the <i>bit</i>-addressed value in RAM + <i>bit</i> offset into the register.</td>
    </tr>
    <tr>
      <td>00000100 [4]</td>
      <td>LOADW</td>
      <td>OFFSET [8]</td>
      <td>R1 [16]</td>
      <td>RAM [13]</td>
      <td>RAM [16]</td>
      <td>Moves the <i>byte</i>-addressed value in RAM + <i>byte</i> offset into the register.</td>
    </tr>
    <tr>
      <td>00000101 [5]</td>
      <td>SETB</td>
      <td>OFFSET [8]</td>
      <td>R1 [16]</td>
      <td>RAM [16]</td>
      <td>RAM [16]</td>
      <td>Moves the value in R1 into the <i>bit</i>-addressed + <i>bit</i> offset RAM.</td>
    </tr>
    <tr>
      <td>00000110 [6]</td>
      <td>SETW</td>
      <td>OFFSET [8]</td>
      <td>R1 [16]</td>
      <td>RAM [13]</td>
      <td>RAM [16]</td>
      <td>Moves the value in R1 into the <i>byte</i>-addressed + <i>byte</i> offset RAM.</td>
    </tr>
    <tr>
      <td>00000111 [7]</td>
      <td>JMP</td>
      <td>-</td>
      <td>ADDR [5]</td>
      <td>ADDR [16]</td>
      <td>-</td>
      <td>Sets the program counter to ADDR unconditionally.</td>
    </tr>
</table>
