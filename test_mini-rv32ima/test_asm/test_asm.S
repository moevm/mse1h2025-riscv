
.section .initial_jump
.global _start
.global asm_demo_func

.align 4
_start:
	la	sp, _sstack
	addi	sp,sp,-16
	sw	ra,12(sp)
	jal	ra, main


.section .data

.align 4
new_line:
	.ascii "\n"
	.byte 0

.section .text

.align 4
asm_demo_func:
	addi sp, sp, -16
	sw t0, 12(sp)
	
	li t0, 10
	li t1, 5
	la t6, new_line
	csrw 0x138, t6
	
	add t2, t1, t0	# сложение 5 и 10
	csrw 0x137, t2
			# результат
		
	la t6, new_line
	csrw 0x138, t6
	
	sub t2, t1, t0	# вычитание из 5 числа 10
	csrw 0x137, t2
			#
	
	la t6, new_line
	csrw 0x138, t6
	
	mul t2, t1, t0	# умножение 5 на 10
	csrw 0x137, t2
			#
	
	la t6, new_line
	csrw 0x138, t6
	
	div t2, t0, t1	# деление 10 на 5
	csrw 0x137, t2
			#
	
	la t6, new_line
	csrw 0x138, t6
	
	li      t0, 0x12345678   # число 305419896
	srl     t1, t0, 2        # сдвигаем вправо на 2 бита
                         # результат: 0x048d591e (78195662)
	csrw 0x137, t1
	
	la t6, new_line
	csrw 0x138, t6
	
	li      t0, 0xFF123456   # отрицательное число
	sra     t1, t0, 2        # арифметический сдвиг вправо
                         # результат: 0xFF48D591 (-1073741820)
	csrw 0x137, t1
	
	la t6, new_line
	csrw 0x138, t6
	
	li      t0, 0x12345678   # число 305419896
	sll     t1, t0, 2        # cдвигаем влево на 2 бита
                         # результат: 0x48d195e0 
	csrw 0x137, t1
	
	la t6, new_line
	csrw 0x138, t6
	
	test_branches:
        # Пример сравнения с нулем
        li      t0, 5           # Загружаем число 5
        beqz    t0, zero_case   # Переходим к zero_case, если t0 = 0
        bnez    t0, non_zero    # Переходим к non_zero, если t0 != 0

    zero_case:
        # Код для случая, когда число равно нулю
        li      t1, 0
        csrw 0x137, t1
        j       end_test        # Переходим к концу теста

    non_zero:
        # Код для случая, когда число не равно нулю
        li      t1, 1
        csrw 0x137, t1
        j       end_test        # Переходим к концу теста

    end_test:
        la t6, new_line
        csrw 0x138, t6
    	
    	lw t0, 12(sp)
	addi sp, sp, 16
	ret

