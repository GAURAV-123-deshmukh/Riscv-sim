.section .text

matmul:
	li a4, 1
	li t0, 12
	li t1, 3
    li t2, 0  # loop variable i         
row:
	beq t2, t1, done
    li t3, 0 	# loop variable j
col:
	beq t3, t1, next_row
    li t4, 0          # sum c[i][j] = 0
    li t5, 0          # loop variable k
    
loop_k:
	beq t5, t1, next_col
	
    mul t6, t2, t0
    slli a3, t5, 2
    add t6, t6, a3
    add t6, t6, a0
    lw a5, 0(t6)      # load A[i][k] into a5

	
	mul t6, t5, t0
    slli a3, t3, 2
    add t6, t6, a3
    add t6, t6, a1
    lw a6, 0(t6)	 # load B[k][j] into a6

    mul a5, a5, a6
    add t4, t4, a5    # t4 += A[i][k] * B[k][j]
    
    addi t5, t5, 1
    j loop_k
    

next_col:
	mul t6, t2, t0
    slli a3, t3, 2
    add t6, t6, a3
    add t6, t6, a2
    sw t4, 0(t6)      # store t4 into C[i][j]
    addi t3, t3, 1
    beqz t4, found
    j col

found:
	li a4, 0
	j col
	
    
next_row:
	addi t2, t2, 1
    j row

done:
	mv a0, a4
	ret


.globl main
main:
    addi sp, sp, -128   
    sw ra, 4(sp)
    sw s0, 0(sp)
    sw a0, 8(sp)
    sw a1, 12(sp)
    sw a2, 16(sp)
    addi s0, sp, 128

    # array a 3x3
    li a0, 1
    sw a0, -72(s0)
    li a0, 2
    sw a0, -68(s0)
    li a0, 3
    sw a0, -64(s0)

    li a0, 4
    sw a0, -60(s0)
    li a0, 5
    sw a0, -56(s0)
    li a0, 6
    sw a0, -52(s0)

    li a0, 0
    sw a0, -48(s0)
    li a0, 0
    sw a0, -44(s0)
    li a0, 0
    sw a0, -40(s0)

    # array b 3x3
    li a0, 9              
    sw a0, -36(s0)        
    li a0, 8              
    sw a0, -32(s0)
    li a0, 7
    sw a0, -28(s0)

    li a0, 6
    sw a0, -24(s0)
    li a0, 5
    sw a0, -20(s0)
    li a0, 4
    sw a0, -16(s0)

    li a0, 3
    sw a0, -12(s0)
    li a0, 2
    sw a0, -8(s0)
    li a0, 1
    sw a0, -4(s0)
    
    addi a0, s0, -72  # address of matrix A
    addi a1, s0, -36  # address of matrix B
    addi a2, s0, -108 # address of matrix C
    
    jal matmul
    
    lw a2, 16(sp)
    lw a1, 12(sp)
    lw a0, 8(sp)
    lw ra, 4(sp)
	lw s0, 0(sp)
	addi sp, sp, 116

halt:
    j halt
