.section .data
	.align 2
n:	
	.word 5
l:
	.word 2
	.word -1
	.word 7
	.word 5
	.word 3

.section .text
.globl main
main:
    la x9,l
	li x8,0
	li x3,1
	li x4,4
	li x5,5

loop: 
	beq x8,x5,halt
	lw x6,0(x9)
	blt x6,x0,odd
	add x8,x8,x3
	add x9,x9,x4
	j loop
	
odd:
	add x8,x8,x3
	add x9,x9,x4
	j loop
    
halt:
	j halt
