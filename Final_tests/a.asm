global:
	sw $ra 0($gp)
	li $t0 4
	sub $t0 $gp $t0
	move $s1 $t0
	lw $ra 0($gp)
	jr $ra
L0:
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
	la $a0 L3
	li $v0 4 
	syscall 
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -40($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -40($fp)
	sw $t0,  -28($fp)
	sw $t0,  -44($fp)
	L12:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -28($fp)
	lw $t1  -12($fp)
	slt $t2, $t0, $t1
	sw $t2  -48($fp)
	lw $t0,  -48($fp)
	beq $t0, $0, L13
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -56($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -56($fp)
	sw $t0,  -32($fp)
	sw $t0,  -60($fp)
	L9:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -32($fp)
	lw $t1  -12($fp)
	slt $t2, $t0, $t1
	sw $t2  -64($fp)
	lw $t0,  -64($fp)
	beq $t0, $0, L10
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -76($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -28($fp)
	lw $t1  -76($fp)
	mul $t2, $t0, $t1
	sw $t2  -80($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -0($fp)
	lw $t2  -80($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -84($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -84($fp)
	lw $t2  -32($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -88($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -88($fp)
	sw $t0 -92($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -92($fp)
	lw $t1 0($t0)
	sw $t1 -96($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -100($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -96($fp)
	sw $t0,  -72($fp)
	sw $t0,  -104($fp)
	lw $t0  -72($fp)
	move $a0 $t0 
	li $v0 1 
	syscall 
	la $a0 L8
	li $v0 4 
	syscall 
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -32($fp)
	sw $t0  -68($fp)
	addi $t0 $t0 1
	sw $t0  -32($fp)
	j L9
	L10:
	la $a0 L11
	li $v0 4 
	syscall 
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -28($fp)
	sw $t0  -52($fp)
	addi $t0 $t0 1
	sw $t0  -28($fp)
	j L12
	L13:
	la $a0 L14
	li $v0 4 
	syscall 
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -120($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -120($fp)
	sw $t0,  -28($fp)
	sw $t0,  -124($fp)
	L23:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -28($fp)
	lw $t1  -12($fp)
	slt $t2, $t0, $t1
	sw $t2  -128($fp)
	lw $t0,  -128($fp)
	beq $t0, $0, L24
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -136($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -136($fp)
	sw $t0,  -32($fp)
	sw $t0,  -140($fp)
	L20:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -32($fp)
	lw $t1  -12($fp)
	slt $t2, $t0, $t1
	sw $t2  -144($fp)
	lw $t0,  -144($fp)
	beq $t0, $0, L21
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -156($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -28($fp)
	lw $t1  -156($fp)
	mul $t2, $t0, $t1
	sw $t2  -160($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -4($fp)
	lw $t2  -160($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -164($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -164($fp)
	lw $t2  -32($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -168($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -168($fp)
	sw $t0 -172($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -172($fp)
	lw $t1 0($t0)
	sw $t1 -176($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -180($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -176($fp)
	sw $t0,  -152($fp)
	sw $t0,  -184($fp)
	lw $t0  -152($fp)
	move $a0 $t0 
	li $v0 1 
	syscall 
	la $a0 L19
	li $v0 4 
	syscall 
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -32($fp)
	sw $t0  -148($fp)
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
	sw $t0  -132($fp)
	addi $t0 $t0 1
	sw $t0  -28($fp)
	j L23
	L24:
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -196($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -196($fp)
	sw $t0,  -16($fp)
	sw $t0,  -200($fp)
	L33:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -16($fp)
	lw $t1  -12($fp)
	slt $t2, $t0, $t1
	sw $t2  -204($fp)
	lw $t0,  -204($fp)
	beq $t0, $0, L34
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -212($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -212($fp)
	sw $t0,  -20($fp)
	sw $t0,  -216($fp)
	L31:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -20($fp)
	lw $t1  -12($fp)
	slt $t2, $t0, $t1
	sw $t2  -220($fp)
	lw $t0,  -220($fp)
	beq $t0, $0, L32
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -228($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -16($fp)
	lw $t1  -228($fp)
	mul $t2, $t0, $t1
	sw $t2  -232($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t2  -232($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -236($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -236($fp)
	lw $t2  -20($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -240($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -240($fp)
	sw $t0 -244($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -244($fp)
	lw $t1 0($t0)
	sw $t1 -248($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -252($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -256($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -256($fp)
	lw $t1, -252($fp)
	sw $t0, 0($t1)
	sw $t0,  -260($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -264($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -264($fp)
	sw $t0,  -24($fp)
	sw $t0,  -268($fp)
	L29:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -24($fp)
	lw $t1  -12($fp)
	slt $t2, $t0, $t1
	sw $t2  -272($fp)
	lw $t0,  -272($fp)
	beq $t0, $0, L30
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -280($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -16($fp)
	lw $t1  -280($fp)
	mul $t2, $t0, $t1
	sw $t2  -284($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t2  -284($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -288($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -288($fp)
	lw $t2  -20($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -292($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -292($fp)
	sw $t0 -296($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -296($fp)
	lw $t1 0($t0)
	sw $t1 -300($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -304($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -308($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -16($fp)
	lw $t1  -308($fp)
	mul $t2, $t0, $t1
	sw $t2  -312($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t2  -312($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -316($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -316($fp)
	lw $t2  -20($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -320($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -320($fp)
	sw $t0 -324($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -324($fp)
	lw $t1 0($t0)
	sw $t1 -328($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -332($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -336($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -16($fp)
	lw $t1  -336($fp)
	mul $t2, $t0, $t1
	sw $t2  -340($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -0($fp)
	lw $t2  -340($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -344($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -344($fp)
	lw $t2  -24($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -348($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -348($fp)
	sw $t0 -352($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -352($fp)
	lw $t1 0($t0)
	sw $t1 -356($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -360($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -364($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -364($fp)
	lw $t1  -24($fp)
	mul $t2, $t0, $t1
	sw $t2  -368($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -4($fp)
	lw $t2  -368($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -372($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -372($fp)
	lw $t2  -20($fp)
	li $t1 4
	mul $t1 $t1 $t2
	sub $t0, $t0, $t1
	sw $t0  -376($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -376($fp)
	sw $t0 -380($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -380($fp)
	lw $t1 0($t0)
	sw $t1 -384($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -388($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -356($fp)
	lw $t1  -384($fp)
	mul $t2, $t0, $t1
	sw $t2  -392($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -328($fp)
	lw $t1  -392($fp)
	add $t2, $t0, $t1
	sw $t2  -396($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -396($fp)
	lw $t1, -304($fp)
	sw $t0, 0($t1)
	sw $t0,  -400($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -24($fp)
	sw $t0  -276($fp)
	addi $t0 $t0 1
	sw $t0  -24($fp)
	j L29
	L30:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -20($fp)
	sw $t0  -224($fp)
	addi $t0 $t0 1
	sw $t0  -20($fp)
	j L31
	L32:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -16($fp)
	sw $t0  -208($fp)
	addi $t0 $t0 1
	sw $t0  -16($fp)
	j L33
	L34:
	la $a0 L35
	li $v0 4 
	syscall 
	lw $sp, 4($fp)
	lw $ra 12($fp)
	lw $fp 8($fp)
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
	lw $t0,  -100($fp)
	sw $t0,  -84($fp)
	sw $t0,  -104($fp)
	L42:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -84($fp)
	lw $t1  -96($fp)
	slt $t2, $t0, $t1
	sw $t2  -108($fp)
	lw $t0,  -108($fp)
	beq $t0, $0, L43
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -116($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -116($fp)
	sw $t0,  -88($fp)
	sw $t0,  -120($fp)
	L40:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -88($fp)
	lw $t1  -96($fp)
	slt $t2, $t0, $t1
	sw $t2  -124($fp)
	lw $t0,  -124($fp)
	beq $t0, $0, L41
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -84($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -132($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -132($fp)
	lw $t1  -88($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -136($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -140($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -144($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -144($fp)
	lw $t1, -140($fp)
	sw $t0, 0($t1)
	sw $t0,  -148($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -36($fp)
	lw $t1  -84($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -152($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -152($fp)
	lw $t1  -88($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -156($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -160($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -164($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -164($fp)
	lw $t1, -160($fp)
	sw $t0, 0($t1)
	sw $t0,  -168($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -88($fp)
	sw $t0  -128($fp)
	addi $t0 $t0 1
	sw $t0  -88($fp)
	j L40
	L41:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -84($fp)
	sw $t0  -112($fp)
	addi $t0 $t0 1
	sw $t0  -84($fp)
	j L42
	L43:
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -172($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -172($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -176($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -180($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -176($fp)
	lw $t1  -180($fp)
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
	li $t0 1
	sw $t0  -192($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -192($fp)
	lw $t1, -188($fp)
	sw $t0, 0($t1)
	sw $t0,  -196($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -200($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -200($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -204($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -208($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -204($fp)
	lw $t1  -208($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -212($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -216($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -220($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -220($fp)
	lw $t1, -216($fp)
	sw $t0, 0($t1)
	sw $t0,  -224($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -228($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -228($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -232($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -236($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -232($fp)
	lw $t1  -236($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -240($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -244($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 3
	sw $t0  -248($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -248($fp)
	lw $t1, -244($fp)
	sw $t0, 0($t1)
	sw $t0,  -252($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -256($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -256($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -260($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -264($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -260($fp)
	lw $t1  -264($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -268($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -272($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sw $t0  -276($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -276($fp)
	lw $t1, -272($fp)
	sw $t0, 0($t1)
	sw $t0,  -280($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -284($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -36($fp)
	lw $t1  -284($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -288($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -292($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -288($fp)
	lw $t1  -292($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -296($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -300($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -304($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -304($fp)
	lw $t1, -300($fp)
	sw $t0, 0($t1)
	sw $t0,  -308($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -312($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -36($fp)
	lw $t1  -312($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -316($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -320($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -316($fp)
	lw $t1  -320($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -324($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -328($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 2
	sw $t0  -332($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -332($fp)
	lw $t1, -328($fp)
	sw $t0, 0($t1)
	sw $t0,  -336($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -340($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -36($fp)
	lw $t1  -340($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -344($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -348($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -344($fp)
	lw $t1  -348($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -352($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -356($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 3
	sw $t0  -360($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -360($fp)
	lw $t1, -356($fp)
	sw $t0, 0($t1)
	sw $t0,  -364($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -368($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -36($fp)
	lw $t1  -368($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -372($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 1
	sw $t0  -376($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -372($fp)
	lw $t1  -376($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -380($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -384($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sw $t0  -388($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -388($fp)
	lw $t1, -384($fp)
	sw $t0, 0($t1)
	sw $t0,  -392($fp)
				lw $t0 -8($fp)
	sw $t0 0($sp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -36($fp)
	sw $t0 0($sp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -64($fp)
	sw $t0 0($sp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -96($fp)
	sw $t0 0($sp)
	li $t0 4
	sub $sp $sp $t0
	jal L0
	li $t0 16
	add $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -396($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -400($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -400($fp)
	sw $t0,  -84($fp)
	sw $t0,  -404($fp)
	L52:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -84($fp)
	lw $t1  -96($fp)
	slt $t2, $t0, $t1
	sw $t2  -408($fp)
	lw $t0,  -408($fp)
	beq $t0, $0, L53
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -416($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -416($fp)
	sw $t0,  -88($fp)
	sw $t0,  -420($fp)
	L49:
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -88($fp)
	lw $t1  -96($fp)
	slt $t2, $t0, $t1
	sw $t2  -424($fp)
	lw $t0,  -424($fp)
	beq $t0, $0, L50
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -64($fp)
	lw $t1  -84($fp)
	li $t2 8
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	sw $t0  -436($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -436($fp)
	lw $t1  -88($fp)
	li $t2 4
	mul $t1 $t1 $t2
	sub $t0 $t0 $t1
	lw $t2 0($t0)
	sw $t2  -440($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -444($fp)
	lw $t0  -440($fp)
	move $a0 $t0 
	li $v0 1 
	syscall 
	la $a0 L48
	li $v0 4 
	syscall 
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -88($fp)
	sw $t0  -428($fp)
	addi $t0 $t0 1
	sw $t0  -88($fp)
	j L49
	L50:
	la $a0 L51
	li $v0 4 
	syscall 
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -84($fp)
	sw $t0  -412($fp)
	addi $t0 $t0 1
	sw $t0  -84($fp)
	j L52
	L53:
	la $a0 L54
	li $v0 4 
	syscall 
	lw $sp, 4($fp)
	lw $ra 12($fp)
	lw $fp 8($fp)
	jr $ra

.data
L51: .ascii "\n"
	.byte 0
L48: .ascii " "
	.byte 0
L54: .ascii "\n"
	.byte 0
L19: .ascii " "
	.byte 0
L14: .ascii "\nMatrix B :\n\n"
	.byte 0
L35: .ascii "\nProduct Matrix :\n\n"
	.byte 0
L11: .ascii "\n"
	.byte 0
L22: .ascii "\n"
	.byte 0
L3: .ascii "\nMatrix A :\n\n"
	.byte 0
L8: .ascii " "
	.byte 0
