

.section .data
	.align 2
count:
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
	.word 0
marks:
	.word 2
	.word 3
	.word 0
	.word 5
	.word 10
	.word 7
	.word 1
	.word 10
	.word 10
	.word 8
	.word 9
	.word 6
	.word 7
	.word 8
	.word 2
	.word 4
	.word 5
	.word 0
	.word 9
	.word 1
n:
	.word 20

.section .text
.globl main
main:
	# your code here
	# you may change the numbers in the marks array. 
	# Change the size of the array n suitably; 
	# The histogram should be in count.
	# the name of the arrays to remain unchanged
	# remove these comments!

	lw x20,n
	la x1,marks
	la x2,count
	li x3,0
	li x4,4
loop:
	beq x3,x20, halt
	lw x5,0(x1)
	mul x10,x5,x4
	add x7,x2,x10
	lw x6,0(x7)
	addi x6,x6,1
	sw x6,0(x7)
	addi x3,x3,1
	addi x1,x1,4
	j loop

halt:
	j halt
