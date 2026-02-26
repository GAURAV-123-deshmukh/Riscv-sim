.section .text

.globl fact
fact:
		blt    a0,zero,return_st
		addi   sp,sp,-20
		sw     fp,16(sp)
		addi   fp,sp,20
		beq    a0,zero,return_value
		sw     a0,4(fp)
		addi   a0,a0,-1
		sw     ra,8(fp)
		jal    ra,fact
		
restoring_reg:
		lw     t0,4(fp)
		mul    t1,a0,t0
		add    a0,t1,zero
		lw     ra,8(fp)
		lw     fp,16(sp)
		addi   sp,sp,20
		jalr   zero,0(ra)
				
return_value:
		li     a0,1
		lw     fp,16(sp)
		addi   sp,sp,20
		
return_st:
		jalr   zero,0(ra)
		
.globl main
main:
		addi   sp,sp,-16
		sw     fp,12(sp)
		addi   fp,sp,16
		li     a0,5
		sw     ra,4(fp)
		jal    ra,fact
		
retstoring_main_reg:
		lw     ra,4(fp)
		lw     fp,12(sp)
		addi   sp,sp,16
		
halt:
		j      halt
		
		
		
		
		
		
