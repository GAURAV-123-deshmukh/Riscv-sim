.section .text
.globl main
main:
    li x1,5
    li x2,6
    beq x1,x2,next
    li x4,5
    add x3,x1,x2
    addi x3,x3,2
next:
    li x3,1
  
halt:
	j halt
