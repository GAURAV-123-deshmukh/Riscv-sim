.section .data
	.align 2
n:	
	.word 6
	
.section .text
.globl main
main:
    li x9,2
halt:
	j halt
