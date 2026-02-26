# Write a simple RISC-V assembly program to find the maximum of three numbers. Assume
# that these numbers are available in the registers x1, x2 and x3.

.section .text
	.globl main
main:
	li x1,3
	li x2,4
	li x3,5
	bgeu x1,x2, grx1
	bgeu x2,x3, grx2

grx1: 
	bleu x1,x3, grx3
	mv x4,x1
	j halt
grx2:
	bleu x2,x3, grx3
	mv x3,x2
	j halt

grx3:
	mv x4,x3
	
halt:
	j halt

