# Write a program to check if a given number is prime. If yes, place 1 in x10. If not, place -1 in x10. Use the template in asms/2-prime.s.



.section .data
	.align 2
a:
	.word 7

.section .text

.globl main
main:
	# your code here 
	# check if the number 'a' is prime.
	# If yes, write 1 to the reg x10. 
	# Else write -1 to it. 
	# you may change the value of 'a'
	# remove these comments!

	la x1,a
	lw x2,0(x1)
	li x3,1
	li x4,2
	li x10,-1
	blt x2,x4, halt
loop:
	beq x4,x2,prime
	rem x5,x2,x4
	beq x5,x0, halt
	add x4,x4,x3
	j loop

prime:
	li x10,1

halt:
	j halt
