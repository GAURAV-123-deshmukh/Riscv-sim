.section .data
    .align 2
n:  .word 6

.section .text
.global fact
fact:
	beqz a0, base_case
	add	sp, sp, -12
	sw ra, 8(sp)
	sw s0, 4(sp)
	addi s0, sp, 12
    sw a0, -12(s0)
    addi a0, a0, -1
    jal fact
    lw t1, -12(s0)
    mul a0, a0, t1
    lw ra, 8(sp)
	lw s0, 4(sp)
    addi sp, sp, 12
    ret

base_case:
    li a0, 1
    ret

.globl main
main:
	addi sp, sp, -8
	sw ra, 4(sp)
	sw s0, 0(sp)
	addi s0, sp, 8
    lw a0, n     
    jal fact
    lw ra, 4(sp)
	lw s0, 0(sp)
	addi sp, sp, 8

halt:
    j halt
