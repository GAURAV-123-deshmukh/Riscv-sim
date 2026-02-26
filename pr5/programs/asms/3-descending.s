#Write a program to sort an array of numbers in the descending order. The sorted array
#should be placed in the same addresses in memory as the initial array. Use the template
#in asms/3-descending.s.

.section .data
	.align 2
a:
	.word 70
	.word 80
	.word 40
	.word 20
	.word 10
	.word 30
	.word 50
	.word 60

n:
	.word 8

.section .text
.globl main
main:
	# your code here
	# you may change the numbers in the array, 
	# and the size of the array; but allow
	# the name of the array to remain as 'a', 
	# and size as 'n'
	# remove these comments!

	la x1,a
	la x3,n     
	lw x3,0(x3)
	li x10,0 #counter1


loop1:
	beq x10,x3, looparray
	add x6,x1,x0
	addi x5,x1,4
	addi x11,x10,1  #counter2
loop2:
	beq x11,x3,incr1
	lw x15,0(x6)
	lw x16,0(x5)
	bge x16,x15,storei

incr2:
	addi x5,x5,4
	addi x11,x11,1
	j loop2

storei:
	add x6,x0, x5
	j incr2
	

incr1:
	lw x17,0(x1)
	lw x18,0(x6)
	sw x17,0(x6)
	sw x18,0(x1)
	addi x10,x10,1
	addi x1,x1,4
	j loop1

looparray:
	la x1,a
	li x2,0
	li x3,8
printArray:
	beq x2,x3,halt
	lw x4,0(x1)
	addi x1,x1,4
	addi x2,x2,1
	j printArray


halt:
	j halt
