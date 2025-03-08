.data
    prompt: .asciz "Enter password: "
    error:  .asciz "Access denied!"
    flag:   .asciz "SUCCESS"

.text
.globl _start

_start:
    # Вывод приглашения
    li a0, 1
    la a1, prompt
    li a2, 16
    li a7, 64
    ecall

    # Чтение ввода (8 символов)
    li a0, 0
    la a1, 0x11000
    li a2, 8
    li a7, 63
    ecall

    # Секретная проверка
    la t0, 0x11000
    lw t1, 0(t0)
    li t1, 0x30427a4e    # Правильный пароль
    li t2, 0x1337CAFE    # Секретный ключ
    xor t3, t1, t2
    li t4, 0x2375B0B0    # Замаскированное значение
    bne t3, t4, fail
    j success

fail:
    # Вывод ошибки
    li a0, 1
    la a1, error
    li a2, 13
    li a7, 64
    ecall
    j exit

success:
    # Вывод флага
    li a0, 1
    la a1, flag
    li a2, 13
    li a7, 64
    ecall

exit:
    # Завершение программы
    li a7, 93
    li a0, 0
    ecall