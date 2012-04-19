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
	li $t0 4
	sub $sp $sp $t0
	li $t0 0
	sw $t0  -0($fp)
	lw $t0,  -0($fp)
	sw $t0,  -4($fp)
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
	sub $t0  $fp $t0
	sw $t0 -28($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -28($fp)
	sw $t0,  -24($fp)
	sw $t0,  -32($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -24($fp)
	lw $t1 0($t0)
	sw $t1 -36($fp)
	li $t1 4
	sub $sp $sp $t1
	sw $t0 -40($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -12($fp)
	add $t2, $t0, $t1
	sw $t2  -44($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -44($fp)
	lw $t1, -40($fp)
	sw $t0, 0($t1)
	sw $t0,  -48($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -4($fp)
	lw $t1  -8($fp)
	add $t2, $t0, $t1
	sw $t2  -52($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -52($fp)
	sw $t0,  -4($fp)
	sw $t0,  -56($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -8($fp)
	mtc1 $t0 $f8 
	cvt.s.w $f2 $f8 
	l.s $f3 -20($fp)
	mul.s $f4, $f2, $f3
	s.s $f4  -60($fp)
	li $t0 4
	sub $sp $sp $t0
	l.s $f2 -60($fp)
	s.s $f2,  -16($fp)
	s.s $f2,  -64($fp)
	li $t0 4
	sub $sp $sp $t0
	l.s $f2 -16($fp)
	l.s $f3 -20($fp)
	mul.s $f4, $f2, $f3
	s.s $f4  -68($fp)
	li $t0 4
	sub $sp $sp $t0
	l.s $f2 -68($fp)
	cvt.w.s $f2 $f2 
	mfc1 $t0 $f2 
	sw $t0 -72($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -72($fp)
	sw $t0,  -8($fp)
	sw $t0,  -76($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0 -4($fp)
	mtc1 $t0 $f2 
	cvt.s.w $f3 $f2 
	s.s $f3 -80($fp)
	li $t0 4
	sub $sp $sp $t0
	l.s $f2 -80($fp)
	lw $t0 -8($fp)
	mtc1 $t0 $f8 
	cvt.s.w $f3 $f8 
	div.s $f4, $f2, $f3
	s.s $f4  -84($fp)
	li $t0 4
	sub $sp $sp $t0
	l.s $f2 -84($fp)
	s.s $f2,  -16($fp)
	s.s $f2,  -88($fp)
	li $t0 4
	sub $sp $sp $t0
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -4($fp)
	lw $t1  -8($fp)
	slt $t2, $t0, $t1
	sw $t2  -96($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0  -8($fp)
	lw $t1  -12($fp)
	slt $t2, $t1, $t0
	sw $t2  -100($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -96($fp)
	lw $t1,  -100($fp)
	and $t2, $t0, $t1
	sw $t2,  -104($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -4($fp)
	lw $t1,  -12($fp)
	slt $t2, $t0, $t1
	slt $t3, $t1, $t0
	add $t1, $t2, $t3
	sw $t1,  -108($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -104($fp)
	lw $t1,  -108($fp)
	or $t2, $t0, $t1
	sw $t2,  -112($fp)
	lw $t0,  -112($fp)
	beq $t0, $0, L4
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -92($fp)
	sw $t0,  -12($fp)
	sw $t0,  -116($fp)
	li $t0 4
	sub $sp $sp $t0
	lw $t0,  -92($fp)
	sw $t0,  -92($fp)
	sw $t0,  -120($fp)
	L4:
	lw $sp, 4($fp)
	lw $ra 12($fp)
	lw $fp 8($fp)
	jr $ra

.data
