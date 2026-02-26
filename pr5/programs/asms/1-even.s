
#1. Write a RISC-V assembly program to count the number of positive (>= 0), even numbers
#in a given array l. The size of the array is n (n > 0). Place the result in register x10. Use
#the template in asms/1-even.s.



.section .data
	.align 2
n:	
	.word 5
l:
	.word 2
	.word -1
	.word 7
	.word 6
	.word 2

.section .text
.globl main
main:
	# your code here
	# remove these comments!

    la x9,l
	li x8,0
	li x3,1
	li x4,4
	li x5,5
	li x6,2
	li x10,0


loop: 
	beq x8,x5,halt
	lw x6,0(x9)
	blt x6,x0,odd
	andi x7,x6,1
	beq x7,x0,even

odd:
	add x8,x8,x3
	add x9,x9,x4
	j loop

even:
	add x10,x10,x3
	j odd
	

halt:
	j halt
