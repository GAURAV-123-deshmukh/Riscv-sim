.section .text
.globl main
main:

    li x1,2
    li x2,32
    mul x3,x1,x2
    rem x4,x2,x1
    sub x9,x1,x2
    div x10,x2,x1
