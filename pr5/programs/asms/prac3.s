#Write a simple RISC-V assembly program that adds the values stored in two registers, x1 and x2, and #stores the result in a global variable named sum


.section .data

sum:
	.word 0xc000 


.section .text
	.globl main
main:
	li x1,5
	li x2,9
	add x3,x1,x2
	la x4,sum
	sw x3,0(x4)

halt:
	j halt

	
	
