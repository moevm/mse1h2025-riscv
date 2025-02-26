.text
.globl _start

_start:

    # Базовые арифметические операции
    li a0, 5
    li a7, 1
    ecall
    ;li a1, 3          # a1 = 3
    ;add a2, a0, a1    # a2 = a0 + a1 (5 + 3 = 8)
    ;sub a3, a0, a1    # a3 = a0 - a1 (5 - 3 = 2)
    ;mul a4, a0, a1    # a4 = a0 * a1 (5 * 3 = 15)

    li a7, 93         # Системный вызов exit
    li a0, 0
    ecall
