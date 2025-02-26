    .section .data
msg:
    .asciz "Hello, SPIKE!\n"  # Сообщение для вывода

    .section .text
    .globl _start  # Объявляем точку входа

_start:
    # Выводим сообщение на экран
    li a0, 1          # Файловый дескриптор (1 = stdout)
    la a1, msg        # Адрес строки для вывода
    li a2, 14         # Длина строки (14 символов, включая '\n')
    li a7, 64         # Номер системного вызова write (64)
    ecall             # Вызов системы

    # Завершаем программу с кодом 0
    li a7, 93         # Номер системного вызова exit (93)
    li a0, 0          # Код завершения 0 (успех)
    ecall             # Вызов системы
