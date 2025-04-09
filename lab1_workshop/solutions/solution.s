.globl solution
.text
solution:
    # здесь начинается основная логика
    xor t3, t2, t1
    beqz t3, node_1
    j node_6

node_1:
    xor t3, t2, t2
    beqz t3, node_2
    j node_3

node_2:
    li a0, 23648
    or t6, t3, a0
    j node_5

node_3:
    li t6, 20510
    add t3, t5, t6
    j node_4

node_4:
    or t1, t1, t1
    j node_8

node_5:
    li t6, 39143
    li a1, 42828
    or t1, t2, t6
    bgeu t1, a1, node_7
    j node_9

node_6:
    xor t3, t1, t3
    li t3, 0
    ret  # возвращаемся в main

node_7:
    li a2, 52344
    xor t3, t2, a2
    li t3, 0
    ret

node_8:
    li t5, 13484
    add t3, t5, t1
    li t3, 0
    ret

node_9:
    li t6, 56559
    sub t3, t1, t6
    li t3, 0
    ret
