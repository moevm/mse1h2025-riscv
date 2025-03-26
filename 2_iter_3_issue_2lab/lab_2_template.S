.data
msg: .string "result "

.text
.globl _start

_start:
    jal ra, main
    j exit

main:
    addi sp, sp, -16
    sw ra, 12(sp)

    # Вывод результата
    la a0, msg
    jal ra, print_string
    
    # Вызов функции add_numbers с аргументами 5 и 10
    li a0, 5
    li a1, 10
    jal ra, add_numbers
    jal ra, print_digit

    # Завершение функции main
    lw ra, 12(sp)
    addi sp, sp, 16
    ret


add_numbers:
    add a0, a0, a1
    ret 

print_string:
    li a7, 4
    ecall
    ret

print_digit:
    li a7, 1
    ecall
    ret

exit:
    li a7, 93
    li a0, 0
    ecall
