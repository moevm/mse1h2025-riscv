.data
    error: .asciz "Access denied!"
    flag: .asciz "SUCCESS"

.text
.globl _start
_start:
    li t1, 0x944f
    li t2, 0xf10
    li t4, 0x0  # ожидаемое значение t4
node_0:
    xor t3, t2, t1
    beqz t3, node_1
    j node_2
node_1:
    xor t3, t2, t2
    j node_7
node_2:
    li t5, 48490
    li a0, 23648
    add t2, t5, a0
    beqz t2, node_3
    j node_8
node_3:
    li t6, 20510
    and t6, t6, t1
    bnez t6, node_4
    j node_5
node_4:
    li t6, 11594
    li a1, 17115
    add t3, t6, a1
    j final
node_5:
    li t6, 42828
    xor t6, t6, t3
    j node_6
node_6:
    li a2, 27678
    sub t5, t3, a2
    j final
node_7:
    and t1, t1, t1
    j final
node_8:
    li t5, 32402
    and t3, t5, t1
    j node_9
node_9:
    li t6, 14944
    or t1, t6, t6
    j final
final:
    bne t3, t4, fail  # если t3 != t4 fail
    j success  # если t3 == t4 success
fail:
    li a0, 1
    la a1, error
    li a2, 13
    li a7, 64
    ecall
    j exit
success:
    li a0, 1
    la a1, flag
    li a2, 13
    li a7, 64
    ecall
exit:
    li a7, 93
    li a0, 0
    ecall
