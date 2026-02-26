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
    lw x6,4(x9)
	blt x6,x0,odd
	li x12,21
odd:
    li x13,13
    
halt:
	j halt
    
    
