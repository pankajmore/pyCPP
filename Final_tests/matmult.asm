global:
	sw $ra 0($gp)
	li $t0 4
	sub $t0 $gp $t0
	move $s1 $t0
	lw $ra 0($gp)
	jr $ra
main:
	sw $ra, 0($sp)
	sw $fp, -4($sp)
	sw $sp, -8($sp)
	li $t0 12
	sub $sp $sp $t0
	move $fp $sp
	jal global
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -4($fp)
	li $t0 4 
	sub $sp $sp $t0
	li $t0 12
	sub $t0  $fp $t0
	sw $t0  -8($fp)
	li $t0 16
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -32($fp)
	li $t0 4 
	sub $sp $sp $t0
	li $t0 40
	sub $t0  $fp $t0
	sw $t0  -36($fp)
	li $t0 16
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -60($fp)
	li $t0 4 
	sub $sp $sp $t0
	li $t0 68
	sub $t0  $fp $t0
	sw $t0  -64($fp)
	li $t0 16
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -92($fp)
	lw $t0,  -92($fp)
	sw $t0,  -96($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -100($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -100($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -104($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -108($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -104($fp)
	lw $t1  -108($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -112($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -116($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -120($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -120($fp)
	lw $t1, -116($fp)
	sw $t0, 0($t1)
	sw $t0,  -124($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -128($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -128($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -132($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -136($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -132($fp)
	lw $t1  -136($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -140($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -144($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -148($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -148($fp)
	lw $t1, -144($fp)
	sw $t0, 0($t1)
	sw $t0,  -152($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -156($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -156($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -160($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -164($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -160($fp)
	lw $t1  -164($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -168($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -172($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 3
	sw $t0  -176($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -176($fp)
	lw $t1, -172($fp)
	sw $t0, 0($t1)
	sw $t0,  -180($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -184($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -184($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -188($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -192($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -188($fp)
	lw $t1  -192($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -196($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -200($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sw $t0  -204($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -204($fp)
	lw $t1, -200($fp)
	sw $t0, 0($t1)
	sw $t0,  -208($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -212($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -36($fp)
	lw $t1  -212($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -216($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -220($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -216($fp)
	lw $t1  -220($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -224($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -228($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -232($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -232($fp)
	lw $t1, -228($fp)
	sw $t0, 0($t1)
	sw $t0,  -236($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -240($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -36($fp)
	lw $t1  -240($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -244($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -248($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -244($fp)
	lw $t1  -248($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -252($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -256($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -260($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -260($fp)
	lw $t1, -256($fp)
	sw $t0, 0($t1)
	sw $t0,  -264($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -268($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -36($fp)
	lw $t1  -268($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -272($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -276($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -272($fp)
	lw $t1  -276($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -280($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -284($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 3
	sw $t0  -288($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -288($fp)
	lw $t1, -284($fp)
	sw $t0, 0($t1)
	sw $t0,  -292($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -296($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -36($fp)
	lw $t1  -296($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -300($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -304($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -300($fp)
	lw $t1  -304($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -308($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -312($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sw $t0  -316($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -316($fp)
	lw $t1, -312($fp)
	sw $t0, 0($t1)
	sw $t0,  -320($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -324($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -324($fp)
	sw $t0,  -84($fp)
	sw $t0,  -328($fp)
	L10:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -84($fp)
	lw $t1  -96($fp)
	slt $t2, $t0, $t1
	sw $t2  -332($fp)
	lw $t0,  -332($fp)
	beq $t0, $0, L11
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -340($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -340($fp)
	sw $t0,  -88($fp)
	sw $t0,  -344($fp)
	L7:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -88($fp)
	lw $t1  -96($fp)
	slt $t2, $t0, $t1
	sw $t2  -348($fp)
	lw $t0,  -348($fp)
	beq $t0, $0, L8
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -64($fp)
	lw $t1  -84($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -356($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -356($fp)
	lw $t1  -88($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -360($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -364($fp)
	lw $t0  -360($fp)
	move $a0 $t0 
	li $v0 1 
	syscall 
	la $a0 L6
	li $v0 4 
	syscall 
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -88($fp)
	sw $t0  -352($fp)
	addi $t0 $t0 1
	sw $t0  -88($fp)
	j L7
	L8:
	la $a0 L9
	li $v0 4 
	syscall 
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -84($fp)
	sw $t0  -336($fp)
	addi $t0 $t0 1
	sw $t0  -84($fp)
	j L10
	L11:
	lw $sp, 4($fp)
	lw $ra 12($fp)
	lw $fp 8($fp)
	jr $ra
L12:
	sw $ra, 0($sp)
	sw $fp, -4($sp)
	sw $sp, -8($sp)
	li $t0 12
	sub $sp $sp $t0
	move $fp $sp
	lw $t0 28($fp)
	sw $t0 -0($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 24($fp)
	sw $t0 -4($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 20($fp)
	sw $t0 -8($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 16($fp)
	sw $t0 -12($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -36($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -36($fp)
	sw $t0,  -28($fp)
	sw $t0,  -40($fp)
	L23:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -28($fp)
	lw $t1  -12($fp)
	slt $t2, $t0, $t1
	sw $t2  -44($fp)
	lw $t0,  -44($fp)
	beq $t0, $0, L24
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -52($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -52($fp)
	sw $t0,  -32($fp)
	sw $t0,  -56($fp)
	L20:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -32($fp)
	lw $t1  -12($fp)
	slt $t2, $t0, $t1
	sw $t2  -60($fp)
	lw $t0,  -60($fp)
	beq $t0, $0, L21
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -0($fp)
	lw $t1  -28($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -68($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -68($fp)
	lw $t1  -32($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -72($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -76($fp)
	lw $t0  -72($fp)
	move $a0 $t0 
	li $v0 1 
	syscall 
	la $a0 L19
	li $v0 4 
	syscall 
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -32($fp)
	sw $t0  -64($fp)
	addi $t0 $t0 1
	sw $t0  -32($fp)
	j L20
	L21:
	la $a0 L22
	li $v0 4 
	syscall 
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -28($fp)
	sw $t0  -48($fp)
	addi $t0 $t0 1
	sw $t0  -28($fp)
	j L23
	L24:
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -88($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -88($fp)
	sw $t0,  -16($fp)
	sw $t0,  -92($fp)
	L33:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -16($fp)
	lw $t1  -12($fp)
	slt $t2, $t0, $t1
	sw $t2  -96($fp)
	lw $t0,  -96($fp)
	beq $t0, $0, L34
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -104($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -104($fp)
	sw $t0,  -20($fp)
	sw $t0,  -108($fp)
	L31:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -20($fp)
	lw $t1  -12($fp)
	slt $t2, $t0, $t1
	sw $t2  -112($fp)
	lw $t0,  -112($fp)
	beq $t0, $0, L32
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -16($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -120($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -120($fp)
	lw $t1  -20($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -124($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -128($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -132($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -132($fp)
	lw $t1, -128($fp)
	sw $t0, 0($t1)
	sw $t0,  -136($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -140($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -140($fp)
	sw $t0,  -24($fp)
	sw $t0,  -144($fp)
	L29:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -24($fp)
	lw $t1  -12($fp)
	slt $t2, $t0, $t1
	sw $t2  -148($fp)
	lw $t0,  -148($fp)
	beq $t0, $0, L30
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -16($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -156($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -156($fp)
	lw $t1  -20($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -160($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -164($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -0($fp)
	lw $t1  -16($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -168($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -168($fp)
	lw $t1  -24($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -172($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -176($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -4($fp)
	lw $t1  -24($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -180($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -180($fp)
	lw $t1  -20($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -184($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -188($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -172($fp)
	lw $t1  -184($fp)
	mul $t2, $t0, $t1
	sw $t2  -192($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -192($fp)
	lw $t3,  -160($fp)
	lw $t1, -164($fp)
	add $t0, $t3, $t0
	sw $t0, 0($t1)
	sw $t0,  -196($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -24($fp)
	sw $t0  -152($fp)
	addi $t0 $t0 1
	sw $t0  -24($fp)
	j L29
	L30:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -20($fp)
	sw $t0  -116($fp)
	addi $t0 $t0 1
	sw $t0  -20($fp)
	j L31
	L32:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -16($fp)
	sw $t0  -100($fp)
	addi $t0 $t0 1
	sw $t0  -16($fp)
	j L33
	L34:
	lw $sp, 4($fp)
	lw $ra 12($fp)
	lw $fp 8($fp)
	jr $ra

.data
L6: .ascii " "
	.byte 0
L22: .ascii "\n"
	.byte 0
L19: .ascii " "
	.byte 0
L9: .ascii "\n"
	.byte 0
