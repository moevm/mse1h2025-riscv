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
    j node_1
node_1:
    li t5, 24393
    add t3, t1, t5
    beqz t3, node_2
    j node_3
node_2:
    or t6, t3, 23648
    beqz t6, node_4
    j node_5
node_3:
    li t6, 20510
    and t6, t6, t1
    j node_8
node_4:
    li t6, 11594
    add t1, t6, 17115
    j node_9
node_5:
    li t6, 42828
    xor t6, t6, t3
    bge t6, node_6
    j node_7
node_6:
    add t5, t3, 27678
    j final
node_7:
    and t1, t1, t1
    j final
node_8:
    li t5, 32402
    and t3, t5, t1
    j final
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
