    .section .text
    .globl _start

_start:
    # Тестирование ветвлений
    li a0, 10         # a0 = 10
    li a1, 20         # a1 = 20
    bge a1, a0, branch_label  # Если a1 >= a0, переходим к branch_label

    # Этот блок не выполнится
    li a2, 0xDEADBEEF # a2 = 0xDEADBEEF

branch_label:
    # Этот блок выполнится
    li a3, 0xCAFEBABE # a3 = 0xCAFEBABE

    # Завершаем программу
    li a7, 93         # Системный вызов exit
    li a0, 0          # Код завершения 0
    ecall
