.section .text

.globl matmul
matmul:
		addi   sp,sp,-40
		sw     fp,40(sp)
		addi   fp,sp,40
		sw     x5,4(fp)
		
		
		# doing the computation
		# setting numbers of rows and columns
		li     x5,-1 
		li     x23,4  
		mul    x21,x23,a6
		li     x30,1
		
loop1:
		addi   x5,x5,1
		li     x22,0  
		beq    x5,a3,setting_return_values

before_loop2:
		beq   x22,a6,loop1
		mul   x24,x5,x23   
		mul   x29,x24,a4
		add   x18,x10,x29
		mul   x24,x22,x23
		add   x19,x11,x24
		mul   x24,x28,x23
		add   x17,x12,x24
		li    x20,0
		li    x27,0
		
loop2:
		lw    x25,0(x18)  
		lw    x26,0(x19)  
		mul	  x25,x25,x26
		add   x27,x27,x25
		addi  x20,x20,1
		beq   x20,a4,store_c
		add   x19,x19,x21
		addi  x18,x18,4
		j     loop2
		
store_c:
		sw    x27,0(x17)
		beq   x27,x0,store_zero
next:
		addi  x22,x22,1
		addi  x28,x28,1
		j     before_loop2
		
setting_return_values:
		beq   x30,x0,return_values
		li    x10,1		
	
restore_callee_mat:
	lw     x5,4(fp)
	lw     fp,40(sp)
	addi   sp,sp,40
	jalr   x0,0(ra) 
	
	
store_zero:
	li    x30,0
	j     next
	
return_values:
	li   x10,1
	j    restore_callee_mat 
	   



.globl main
main:
		addi sp,sp,-128
		sw fp,4(sp)
		addi fp,sp,128
		
local_array1:
		li     t0,1
		sw     t0,0(fp)
		li     t0,2
		sw     t0,4(fp)
		li     t0,3
		sw     t0,8(fp)
		li     t0,4
		sw     t0,12(fp)
		li     t0,5
		sw     t0,16(fp)
		li     t0,6
		sw     t0,20(fp)
		li     t0,7
		sw     t0,24(fp)
		li     t0,8
		sw     t0,28(fp)
		li     t0,9
		sw     t0,32(fp)
		
local_array2:
		li     t0,10
		sw     t0,36(fp)
		li     t0,11
		sw     t0,40(fp)
		li     t0,12
		sw     t0,44(fp)
		li     t0,13
		sw     t0,48(fp)
		li     t0,14
		sw     t0,52(fp)
		li     t0,15
		sw     t0,56(fp)
		li     t0,16
		sw     t0,60(fp)
		li     t0,17
		sw     t0,64(fp)
		li     t0,18
		sw     t0,68(fp)
		
local_array3:
		li     t0,0
		sw     t0,72(fp)
		li     t0,0
		sw     t0,76(fp)
		li     t0,0
		sw     t0,80(fp)
		li     t0,0
		sw     t0,84(fp) 
		li     t0,0
		sw     t0,88(fp)
		li     t0,0
		sw     t0,92(fp)
		li     t0,0
		sw     t0,96(fp)
		li     t0,0
		sw     t0,100(fp)
		li     t0,0
		sw     t0,104(fp)
		
		
addresss_of_arr1_arr2:
		addi   a0,fp,0
		addi   a1,fp,36
		addi   a2,fp,72
		li     a3,3
		li     a4,3
		li     a5,3
		li     a6,3
		

		
calling_mat_mul:
		sw    t0,112(fp)
		sw    ra,108(fp)
		jal   ra,matmul
			

restore_callee_main:
		lw   ra,108(fp)
		lw   fp,4(sp)
		addi sp,sp,128		

		
halt:
		j halt
		
		
		
