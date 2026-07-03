
    ADDI t0, x0, 0
    ADDI t1, x0, 1
    BNE  a0, x0, L1
    ADDI a0, x0, 0
    RET
L1:
    
    ADDI t2, x0, 1
    BNE  a0, t2, L2
    ADDI a0, x0, 1
    RET
L2:
    
    ADDI t3, x0, 2
loop:
    
    BLT  a0, t3, done
    ADD  t4, t0, t1
    ADD  t0, t1, x0
    ADD  t1, t4, x0
    ADDI t3, t3, 1
    JAL  x0, loop
done:
    
    ADD  a0, t1, x0
    RET
