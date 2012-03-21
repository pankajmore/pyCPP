import ply.lex as lex
import re
linenumber = 0

tokens =  ['STRING', 'INTEGER', 'LONGINTEGER', 'HEXADECIMAL', 'DECIMALFLOAT', 'DECIMALDOUBLE', 'FLOATVAL', 'DOUBLEVAL', 'CHARACTER', 'ESCAPECHAR', 'HEXLITERAL', 'IF', 'ELSE', 'LONGHEXADECIMAL', 'IDENTIFIER', 'SIZEOF', 'PTR_OP', 'INC_OP', 'DEC_OP', 'LEFT_OP', 'RIGHT_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 'NE_OP', 'AND_OP', 'OR_OP', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN', 'AND_ASSIGN', 'XOR_ASSIGN', 'OR_ASSIGN', 'TYPE_NAME', 'TYPEDEF', 'EXTERN', 'STATIC', 'AUTO', 'REGISTER', 'CHAR', 'SHORT', 'INT', 'LONG', 'SIGNED', 'UNSIGNED', 'FLOAT', 'DOUBLE', 'CONST', 'VOLATILE', 'VOID', 'CLASS' ,'PUBLIC','PRIVATE','PROTECTED','STRUCT', 'UNION', 'ENUM', 'DOUBLE_COLON','ELLIPSIS', 'CASE', 'DEFAULT', 'SWITCH', 'WHILE', 'DO', 'FOR', 'GOTO', 'CONTINUE', 'BREAK', 'RETURN']

reserved_words = {
        'auto' : 'AUTO',
        'break': 'BREAK',
        'case':'CASE',
        'char' : 'CHAR',
        'const':'CONST',
        'continue':'CONTINUE',
        'default':'DEFAULT',
        'do' : 'DO',
        'double' : 'DOUBLE',
        'else':'ELSE',
        'enum':'ENUM',
        'extern':'EXTERN',
        'float':'FLOAT',
        'for':'FOR',
        'goto' : 'GOTO',
        'if':'IF',
        'int':'INT',
        'long':'LONG',
        'register' : 'REGISTER',
        'return' : 'RETURN',
        'short':'SHORT',
        'signed':'SIGNED',
        'sizeof':'SIZEOF',
        'static':'STATIC',
        'struct' : 'STRUCT',
        'public' : 'PUBLIC',
        'private' : 'PRIVATE',
        'protected' : 'PROTECTED',
        'class' : 'CLASS',
        'switch' : 'SWITCH',
        'typedef':'TYPEDEF',
        'union':'UNION',
        'unsigned':'UNSIGNED',
        'void':'VOID',
        'volatile':'VOLATILE',
        'while':'WHILE'
}        

literals=['[',']','(',')','{','}','=','>','<','!','~',':','+','-','*','/','&','|','^','%','.',';',',','?','#']

t_ELLIPSIS = '\.\.\.'
t_RIGHT_ASSIGN='>>=='
t_LEFT_ASSIGN='<<=='
t_ADD_ASSIGN='\+='
t_SUB_ASSIGN='\-='
t_MUL_ASSIGN='\*='
t_DIV_ASSIGN='/='
t_AND_ASSIGN='&='
t_XOR_ASSIGN='^='
t_OR_ASSIGN='\|='
t_RIGHT_OP='>>'
t_LEFT_OP='<<'
t_INC_OP='\+\+'
t_DEC_OP='\-\-'
t_PTR_OP='\->'
t_AND_OP='&&'
t_OR_OP='\|\|'
t_LE_OP='<='
t_GE_OP='>='
t_EQ_OP='=='
t_NE_OP='!='
t_DOUBLE_COLON='::'

reserved_map = { }
for r in reserved_words:
      reserved_map[r.lower()] = r


def t_IDENTIFIER(t):
        r'[a-zA-Z_\$][a-zA-Z0-9_\$]*'
        t.type=reserved_map.get(t.value,"IDENTIFIER")
        if reserved_words.has_key(t.value):
	      t.type=reserved_words[t.value]
        return t	

def t_LONGINTEGER(t):
	r'[1-9][0-9]*[lL]'
	return t	

def t_INTEGER(t):
	r'\d+'
	return t	

def t_LONGHEXADECIMAL(t):
	r'[0][xX][0-9a-fA-F]+[lL]'
	return t

def t_HEXADECIMAL(t):
	r'[0][xX][0-9a-fA-F]+'
	return t	

def t_DECIMALDOUBLE(t):
	r'(([0-9]+\.[0-9]*)([eE][-+]?[0-9]+)?[dD]?) | (([0-9]*\.[0-9]+)([eE][-+]?[0-9]+)?[dD]?)'
	return t

def t_DECIMALFLOAT(t):
        r'(([0-9]+\.[0-9]*)([eE][-+]?[0-9]+)?[fF]?) | (([0-9]*\.[0-9]+)([eE][-+]?[0-9]+)?[fF]?)'
        return t

def t_DOUBLEVAL(t):
        r'([0-9]+([eE][-+]?[0-9]+)?[dD]) | ([0-9]+([eE][-+]?[0-9]+)[dD]?)'
        return t

def t_FLOATVAL(t):
        r'[0-9]+([eE][-+]?[0-9]+)?[fF]'
        return t

def t_DEFINE(t):
	r'\#define.*'
	pass

def t_INCLUDE(t):
	r'\#include[ ]*(<)([A-Za-z_][\w_]*)(\.h)?(>)'
	pass

def t_SINGLELINECOMMENT(t):
	r'//.*'
	pass

def t_MULTILINECOMMENT(t):
	r'/\*[\w\W]*?\*/'
	pass

def t_CHARACTER(t):
	r'[\'][^\\\'\"\n][\']'
	return t	


def t_ESCAPECHAR(t):
	r'[\'][\\][nbtfrva\'\"\\?0][\']'
	return t	

def t_HEXLITERAL(t):
	r'[\'][\\][x][0-9a-fA-F]{1,3}[\']'
	return t	

def t_STRING(t):
	r'"[^\n]*?(?<!\\)"'
	return t

def t_newline(t):
      r'\n+'
      global linenumber
      linenumber = linenumber + 1
      t.lexer.lineno += t.value.count("\n")        
#[\n]			{ linenumber++; }

t_ignore = " \t\r\v\a\f"


success= True
	
def t_error(t):
      global success
#print "Line %d :" % (t.lineno,) + "LEXICAL ERROR FOUND. Illegal Character: ", t.value[0] + "\n",
      t.lexer.skip(1)
      success= False

lex.lex()

start = 'strt'

precedence =  [('nonassoc', 'STRING', 'INTEGER', 'LONGINTEGER', 'HEXADECIMAL', 'DECIMALFLOAT'), ('nonassoc', 'DECIMALDOUBLE', 'FLOATVAL', 'DOUBLEVAL', 'CHARACTER', 'ESCAPECHAR', 'HEXLITERAL'), ('nonassoc', 'IFX'), ('nonassoc', 'ELSE'), ('nonassoc', 'DOUBLE', 'FLOAT', 'INT', 'SHORT', 'STRUCT', 'UNSIGNED', 'LONG', 'SIGNED', 'VOID', 'ENUM', 'CHAR', 'UNION', ';'), ('right', 'ADD_ASSIGN', 'SUB_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'AND_ASSIGN', 'OR_ASSIGN', 'RIGHT_ASSIGN', 'LEFT_ASSIGN', 'XOR_ASSIGN'), ('right', '=', '|', '!', '^'), ('left', 'OR_OP', 'AND_OP', 'RIGHT_OP', 'LEFT_OP', 'INC_OP', 'DEC_OP', 'PTR_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 'NE_OP'), ('left', ':', '<', '>'), ('left', '+', '-'), ('left', '*', '/', '%'), ('right', '(', '[', '{'), ('left', ')', ']', '}')]

# -------------- RULES ----------------

def p_new_scope_1(t):
	'''new_scope : '''	
        pass

def p_finish_scope_1(t):
	'''finish_scope : '''
        pass

def p_identifier_1(t):
	'''identifier : IDENTIFIER'''
        #print "\nidentifier : IDENTIFIER\n"
        pass 


def p_constant_1(t):
	'''constant : INTEGER'''
        #print "\nconstant : INTEGER\n"
        pass 


def p_constant_2(t):
	'''constant : LONGINTEGER'''
        #print "\nconstant: LONGINTEGER\n"
        pass 

def p_constant_3(t):
	'''constant : HEXADECIMAL'''
#print "\nconstant: HEXADECIMAL\n"
        pass 
        
def p_constant_4(t):
        '''constant : LONGHEXADECIMAL'''
#print "\nconstant->LONGHEXADECIMAL\n"
        pass 

def p_constant_5(t):
        '''constant : DECIMALFLOAT'''
#print "\nconstant->DECIMALFLOAT\n"
        pass 

def p_constant_6(t):
        '''constant : DECIMALDOUBLE'''
#print "\nconstant->DECIMALDOUBLE\n"

def p_constant_7(t):
        '''constant : FLOATVAL'''
#print "\nconstant->FLOATVAL\n"

def p_constant_8(t):
        '''constant : DOUBLEVAL'''
#print "\nconstant->DOUBLEVAL\n"

def p_constant_9(t):
        '''constant : CHARACTER'''
#print "\nconstant:CHARACTER\n"

def p_constant_10(t):
        '''constant : ESCAPECHAR'''
#print "\nconstant:ESCAPECHAR\n"

def p_constant_11(t):
        '''constant : HEXLITERAL'''
#print "\nconstant : HEXLITERAL\n"

def p_constant_12(t):
        '''constant : STRING'''        
#print "\nconstant : STRING\n"

def p_primary_expression_1(t):
        '''primary_expression : identifier'''        
#print "\nprimary_expression : identifier\n"

def p_primary_expression_2(t):
      '''primary_expression : constant'''
#print "\nprimary_expression:constant\n"
      
def p_primary_expression_3(t):
      '''primary_expression : '(' expression ')'
      '''
#print "\nprimary_expression: '(' expression ')' \n"

def p_postfix_expression_1(t):
      '''postfix_expression : primary_expression'''
#print "\npostfix_expression: primary expression \n"
 

def p_postfix_expression_2(t):
      '''postfix_expression : postfix_expression '[' expression ']'
      '''
#print "\npostfix_expression : postfix_expression '[' expression ']'\n"

def p_postfix_expression_3(t):
      '''postfix_expression : postfix_expression '(' ')'
      '''
#print "\n postfix_expression : postfix_expression '(' ')'\n"
	

def p_postfix_expression_4(t):
      '''postfix_expression : postfix_expression '(' argument_expression_list ')'
      '''
#print "\npostfix_expression : postfix_expression'(' argument_expression_list ')' \n"

def p_postfix_expression_5(t):
      '''postfix_expression : postfix_expression '.' identifier'''
#print " postfix_expression : postfix_expression '.' identifier"

def p_postfix_expression_6(t):
      '''postfix_expression : postfix_expression PTR_OP identifier'''
#print " postfix_expression : postfix_expression PTR OP identifier"

def p_postfix_expression_7(t):
      '''postfix_expression : postfix_expression INC_OP'''
#print " postfix_expression: postfix_expression INC OP"

def p_postfix_expression_8(t):
      '''postfix_expression : postfix_expression DEC_OP'''
#print " postfix_expression: postfix_expression DEC OP"

def p_argument_expression_list_1(t):
      '''argument_expression_list : assignment_expression'''
#print "argument_expression_list -> assignment_expression"
      
def p_argument_expression_list_2(t):
      '''argument_expression_list : argument_expression_list ',' assignment_expression'''
#print "argument_expression_list -> argument_expression_list , assignment_expression\n"
			
def p_unary_expression_1(t):
      '''unary_expression : postfix_expression'''
#print "unary_expression:postfix_expression"

def p_unary_expression_2(t):
      '''unary_expression : INC_OP unary_expression'''
#print "unary_expression: INC_OP unary_expression"
      
def p_unary_expression_3(t):
      '''unary_expression : DEC_OP unary_expression'''
#print "unary_expression: DEC_OP unary_expression"

def p_unary_expression_4(t):
      '''unary_expression : unary_operator cast_expression'''
#print "unary_expression:unary_expression cast_expression"
	    
def p_unary_expression_5(t):
      '''unary_expression : SIZEOF unary_expression'''
#print "unary_expression:SIZEOF unary_expression"
		   

def p_unary_expression_6(t):
      '''unary_expression : SIZEOF '(' type_name ')'
      '''
#print "unary_expression:SIZEOF '(' type_name ')'"

def p_unary_operator_1(t):
      '''unary_operator : '&'
      '''
#print "\nunary_operator : '&'\n"

def p_unary_operator_2(t):
      '''unary_operator : '*'
      '''
#print "\nunary_operator : '*'\n"

def p_unary_operator_3(t):
      '''unary_operator : '+'
      '''
#print "\nunary_operator : '+'\n"

def p_unary_operator_4(t):
      '''unary_operator : '-'
      '''
#print "\nunary_operator : '-'\n"

def p_unary_operator_5(t):
      '''unary_operator : '~'
      '''
#print "\nunary_operator : '~'\n"

def p_unary_operator_6(t):
      '''unary_operator : '!'
      '''
#print "\nunary_operator : '!'\n"

def p_cast_expression_1(t):
      '''cast_expression : unary_expression'''
#print "\ncast_expression : unary_expression\n"
      

def p_cast_expression_2(t):
      '''cast_expression : '(' type_name ')' cast_expression'''
#print "\ncast_expression -> ( type_name ) cast_expression\n"

def p_multiplicative_expression_1(t):
      '''multiplicative_expression : cast_expression'''
#print "\nmultiplicative_expression : cast_expression\n"

def p_multiplicative_expression_2(t):
      '''multiplicative_expression : multiplicative_expression '*' cast_expression'''
#print "\nmultiplicative_expression -> multiplicative_expression '*' cast_expression\n"

def p_multiplicative_expression_3(t):
      '''multiplicative_expression : multiplicative_expression '/' cast_expression'''
#print "\nmultiplicative_expression -> multiplicative_expression '/' cast_expression\n"

def p_multiplicative_expression_4(t):
      '''multiplicative_expression : multiplicative_expression '%' cast_expression'''
#print "\nmultiplicative_expression -> multiplicative_expression MOD cast_expression\n"

def p_additive_expression_1(t):
      '''additive_expression : multiplicative_expression'''
#print "\nadditive_expression : multiplicative_expression\n"
      
def p_additive_expression_2(t):
      '''additive_expression : additive_expression '+' multiplicative_expression'''
#print "\nadditive_expression : additive_expression '+' multiplicative_expression\n"

def p_additive_expression_3(t):
      '''additive_expression : additive_expression '-' multiplicative_expression'''
#print "\nadditive_expression : additive_expression '-' multiplicative_expression\n"

def p_shift_expression_1(t):
      '''shift_expression : additive_expression'''
#print "\nshift_expression : additive_expression\n"

def p_shift_expression_2(t):
      '''shift_expression : shift_expression LEFT_OP additive_expression'''
#print "\nshift_expression : shift_expression LEFT_OP additive_expression\n"

def p_shift_expression_3(t):
      '''shift_expression : shift_expression RIGHT_OP additive_expression'''
#print "\nshift_expression : shift_expression RIGHT_OP additive_expression\n"

def p_relational_expression_1(t):
      '''relational_expression : shift_expression'''
#print "\nrelational_expression : shift_expression\n"
      

def p_relational_expression_2(t):
      '''relational_expression : relational_expression '<' shift_expression'''
#print "\nrelational_expression : relational_expression '<' shift_expression\n"

def p_relational_expression_3(t):
      '''relational_expression : relational_expression '>' shift_expression'''
#print "\nrelational_expression : relational_expression '>' shift_expression\n"

def p_relational_expression_4(t):
      '''relational_expression : relational_expression LE_OP shift_expression'''
#print "\nrelational_expression : relational_expression LE_OP shift_expression\n"
	    

def p_relational_expression_5(t):
      '''relational_expression : relational_expression GE_OP shift_expression'''
#print "\nrelational_expression : relational_expression GE_OP shift_expression\n"

def p_equality_expression_1(t):
      '''equality_expression : relational_expression'''
#print "\nequality_expression : relational_expression\n"

def p_equality_expression_2(t):
      '''equality_expression : equality_expression EQ_OP relational_expression'''
#print "\nequality_expression : equality_expression EQ_OP relational_expression\n"

def p_equality_expression_3(t):
      '''equality_expression : equality_expression NE_OP relational_expression'''
#print "\nequality_expression : equality_expression NE_OP relational_expression\n"

def p_and_expression_1(t):
      '''and_expression : equality_expression'''
#print "\nand_expression : equality_expression\n"

def p_and_expression_2(t):
      '''and_expression : and_expression '&' equality_expression'''
#print "\nand_expression : and_expression '&' equality_expression\n"

def p_exclusive_or_expression_1(t):
      '''exclusive_or_expression : and_expression'''
#print "\nexclusive_or_expression : and_expression\n"

def p_exclusive_or_expression_2(t):
      '''exclusive_or_expression : exclusive_or_expression '^' and_expression'''
#print "\nexclusive_or_expression : exclusive_or_expression '^' and_expression\n"

def p_inclusive_or_expression_1(t):
      '''inclusive_or_expression : exclusive_or_expression'''
#print "\ninclusive_or_expression : exclusive_or_expression\n"

def p_inclusive_or_expression_2(t):
      '''inclusive_or_expression : inclusive_or_expression '|' exclusive_or_expression'''
#print "\ninclusive_or_expression : inclusive_or_expression '|' exclusive_or_expression\n"

def p_logical_and_expression_1(t):
      '''logical_and_expression : inclusive_or_expression'''
#print "\nlogical_and_expression : inclusive_or_expression\n"

def p_logical_and_expression_2(t):
      '''logical_and_expression : logical_and_expression AND_OP inclusive_or_expression'''
#print "\nlogical_and_expression : logical_and_expression AND_OP inclusive_or_expression\n"

def p_logical_or_expression_1(t):
      '''logical_or_expression : logical_and_expression'''
#print "\nlogical_or_expression : logical_and_expression\n"
      
def p_logical_or_expression_2(t):
      '''logical_or_expression : logical_or_expression OR_OP logical_and_expression'''
#print "\nlogical_or_expression : logical_or_expression OR_OP logical_and_expression\n"

def p_conditional_expression_1(t):
      '''conditional_expression : logical_or_expression'''
#print "\nconditional_expression : logical_or_expression\n"
      
def p_conditional_expression_2(t):
      '''conditional_expression : logical_or_expression '?' expression ':' conditional_expression'''
#print "\nconditional_expression : logical_or_expression '?' expression ':' conditional_expression\n"

def p_assignment_expression_1(t):
      '''assignment_expression : conditional_expression'''
#print "assignment_expression : conditional_expression"

def p_assignment_expression_2(t):
      '''assignment_expression : unary_expression assignment_operator assignment_expression'''
#print "assignment_expression : unary_expression assignment_operator assignment_expression"
	    
def p_equal_to_1(t):
      '''equal_to : '='
      '''
#print "equal_to : '=' "

def p_assignment_operator_1(t):
      '''assignment_operator : equal_to'''
#print "assignment_operator : equal_to"

def p_assignment_operator_2(t):
      '''assignment_operator : MUL_ASSIGN'''      
#print "assignment_operator : MUL_ASSIGN"

def p_assignment_operator_3(t):
      '''assignment_operator : DIV_ASSIGN'''
#print "assignment_operator : DIV_ASSIGN"

def p_assignment_operator_4(t):
      '''assignment_operator : MOD_ASSIGN'''
#print "assignment_operator : MOD_ASSIGN"

def p_assignment_operator_5(t):
      '''assignment_operator : ADD_ASSIGN'''
#print "assignment_operator : ADD_ASSIGN"

def p_assignment_operator_6(t):
      '''assignment_operator : SUB_ASSIGN'''
#print "assignment_operator : SUB_ASSIGN"

def p_assignment_operator_7(t):
      '''assignment_operator : LEFT_ASSIGN'''
#print "assignment_operator : LEFT_ASSIGN"

def p_assignment_operator_8(t):
      '''assignment_operator : RIGHT_ASSIGN'''
#print "assignment_operator : RIGHT_ASSIGN"

def p_assignment_operator_9(t):
      '''assignment_operator : AND_ASSIGN'''
#print "assignment_operator : AND_ASSIGN"

def p_assignment_operator_10(t):
      '''assignment_operator : XOR_ASSIGN'''
#print "assignment_operator : XORL_ASSIGN"

def p_assignment_operator_11(t):
      '''assignment_operator : OR_ASSIGN'''
#print "assignment_operator : OR_ASSIGN"

def p_expression_1(t):
      '''expression : assignment_expression'''
#print "expression : assignment_expression"      

def p_expression_2(t):
      '''expression : expression ',' assignment_expression'''
#print "\nexpression -> expression ',' assignment_expression\n"      

def p_constant_expression_1(t):
      '''constant_expression : conditional_expression'''
#print "\nconstant_expression -> conditional_expression\n"

def p_declaration_1(t):
      '''declaration : declaration_specifiers ';'
      '''
#print "\ndeclaration -> declaration_specifiers ';' \n"

def p_declaration_2(t):
      '''declaration : declaration_specifiers error'''
#print "\ndeclaration -> declaration_specifiers error';' \n"

def p_declaration_3(t):
      '''declaration : declaration_specifiers init_declarator_list ';'
      '''
#print "\ndeclaration -> declaration_specifiers init_declarator_list ';'\n"

def p_declaration_4(t):
      '''declaration : declaration_specifiers init_declarator_list error'''
#print "\ndeclaration -> declaration_specifiers init_declarator_list error\n"

def p_declaration_specifiers_1(t):
      '''declaration_specifiers : type_qualifier'''
#print "\ndeclaration_specifiers -> type_qualifier\n"
      
def p_declaration_specifiers_2(t):
      '''declaration_specifiers : type_specifier'''
      print "\ndeclaration_specifiers -> type_specifier\n"

def p_declaration_specifiers_3(t):
      '''declaration_specifiers : storage_class_specifier'''
#print "\ndeclaration_specifiers -> storage_class_specifier\n"

def p_declaration_specifiers_4(t):
      '''declaration_specifiers : type_qualifier type_specifier'''
#print "\ndeclaration_specifiers : type_qualifier type_specifier\n"

def p_declaration_specifiers_5(t):
      '''declaration_specifiers : type_specifier type_qualifier'''
#print "\ndeclaration_specifiers : type_specifier type_qualifier\n"

def p_declaration_specifiers_6(t):
      '''declaration_specifiers : type_specifier storage_class_specifier'''
#print "\ndeclaration_specifiers : type_specifier storage_class_specifier\n"

def p_declaration_specifiers_7(t):
      '''declaration_specifiers : storage_class_specifier type_specifier'''
#print "\ndeclaration_specifiers : storage_class_specifier type_specifier\n"

def p_declaration_specifiers_8(t):
      '''declaration_specifiers : storage_class_specifier type_qualifier'''
#print "\ndeclaration_specifiers : storage_class_specifier type_qualifier\n"

def p_declaration_specifiers_9(t):
      '''declaration_specifiers : type_qualifier storage_class_specifier'''
#print "\ndeclaration_specifiers : type_qualifier storage_class_specifier\n"

def p_declaration_specifiers_10(t):
      '''declaration_specifiers : type_qualifier type_specifier storage_class_specifier'''
#print "\ndeclaration_specifiers : type_qualifier type_specifier storage_class_specifier\n"

def p_declaration_specifiers_11(t):
      '''declaration_specifiers : type_qualifier storage_class_specifier type_specifier'''
#print "\ndeclaration_specifiers : type_qualifier storage_class_specifier type_specifier\n"

def p_declaration_specifiers_12(t):
      '''declaration_specifiers : storage_class_specifier type_specifier type_qualifier'''
#print "\ndeclaration_specifiers : storage_class_specifier type_specifier type_qualifier\n"

def p_declaration_specifiers_13(t):
      '''declaration_specifiers : storage_class_specifier type_qualifier type_specifier'''
#print "\ndeclaration_specifiers : storage_class_specifier type_qualifier type_specifier\n"

def p_declaration_specifiers_14(t):
      '''declaration_specifiers : type_specifier type_qualifier storage_class_specifier'''
#print "\ndeclaration_specifiers : type_specifier type_qualifier storage_class_specifier\n"

def p_declaration_specifiers_15(t):
      '''declaration_specifiers : type_specifier storage_class_specifier type_qualifier'''
#print "\ndeclaration_specifiers : type_specifier storage_class_specifier type_qualifier\n"

def p_init_declarator_list_1(t):
      '''init_declarator_list : init_declarator'''
#print "init_declarator_list : init_declarator"
      

def p_init_declarator_list_2(t):
      '''init_declarator_list : init_declarator_list ',' init_declarator'''
#print "init_declarator_list : init_declarator_list ',' init_declarator"
      
def p_init_declarator_1(t):
      '''init_declarator : declarator equal_to initializer'''
#print "init_declarator:declarator equal_to initializer"
	

def p_init_declarator_2(t):
      '''init_declarator : declarator'''
#print "init_declarator : declarator"
			
def p_storage_class_specifier_1(t):
      '''storage_class_specifier : TYPEDEF'''
#print "storage_class_specifier : TYPEDEF"
      
def p_storage_class_specifier_2(t):
      '''storage_class_specifier : EXTERN'''
#print "storage_class_specifier : EXTERN"

def p_storage_class_specifier_3(t):
      '''storage_class_specifier : STATIC'''
#print "storage_class_specifier : STATIC"

def p_storage_class_specifier_4(t):
      '''storage_class_specifier : AUTO'''
#print "storage_class_specifier : AUTO"

def p_storage_class_specifier_5(t):
      '''storage_class_specifier : REGISTER'''
#print "storage_class_specifier : REGISTER"

def p_type_specifier_1(t):
      '''type_specifier : VOID'''
#print "type_specifier : VOID"
				
def p_type_specifier_2(t):
      '''type_specifier : CHAR'''
#print "type_specifier : CHAR "

def p_type_specifier_3(t):
      '''type_specifier : SHORT'''
#print "type_specifier : SHORT"

def p_type_specifier_4(t):
      '''type_specifier : INT'''
#print "type_specifier : INT "

def p_type_specifier_5(t):
      '''type_specifier : LONG'''
#print "type_specifier : LONG"

def p_type_specifier_6(t):
      '''type_specifier : FLOAT'''
#print "type_specifier : FLOAT"

def p_type_specifier_7(t):
      '''type_specifier : DOUBLE'''
#print "type_specifier : DOUBLE"

def p_type_specifier_8(t):
      '''type_specifier : SIGNED'''
#print "type_specifier : SIGNED"

def p_type_specifier_9(t):
      '''type_specifier : UNSIGNED'''
#print "type_specifier : UNSIGNED"

def p_type_specifier_10(t):
      '''type_specifier : class_specifier'''
      print "type_specifier : class_specifier"

def p_type_specifier_11(t):
      '''type_specifier : enum_specifier'''
#print "type_specifier : enum_specifier"

def p_type_specifier_12(t):
      '''type_specifier : TYPE_NAME'''
#print "type_specifier : TYPE_NAME"

## classes ## 
def p_class_name(p):
    ''' class_name : identifier '''
    print "class name "
    pass


def p_class_specifier_1(p):
    ''' class_specifier : class_head '{' member_specification '}' '''
    print ''' class_specifier : class_head '{' member_specification '}' '''
    pass

def p_class_specifier_2(p):
    ''' class_specifier : class_head '{' '}' '''
    print ''' class_specifier : class_head '{' '}' '''
    pass
  
#class-head:
    #class-key identifieropt base-clauseopt
    #class-key nested-name-specifier identifier base-clauseopt
    #class-key nested-name-specifier template template-id base-clauseopt
def p_class_head(p):
    ''' class_head :  class_key identifier base_clause_opt '''
    print "class_head :  class_key identifier base_clause_opt "
    pass 


#class-key:
    #class
    #struct
    #union

def p_class_key(p):
    ''' class_key : CLASS 
                    | STRUCT '''

    print "class key "
    pass

def p_error(p):
    print("Whoa. We're hosed")
    pass

#member-specification:
    #member-declaration member-specificationopt
    #access-specifier : member-specificationopt
def p_member_specification_1(p):
    '''member_specification : member_declaration '''
    print  '''member_specification : member_declaration '''
    pass
  
def p_member_specification_2(p):
    ''' member_specification : member_declaration member_specification '''
    print ''' member_specification : member_declaration member_specification '''
    pass

def p_access_specifier(p):
    ''' access_specifier : PUBLIC 
                    | PRIVATE 
                    | PROTECTED ''' 
    print "access_specifier"
    pass 
  
def p_member_specification_3(p):
    ''' member_specification : access_specifier ':' member_specification '''
    print ''' member_specification : access_specifier ':' member_specification '''
    pass 
  
def p_member_specification_4(p):
    ''' member_specification : access_specifier ':' '''
    print ''' member_specification : access_specifier ':' '''
    pass

#member-declaration:
    #decl-specifier-seqopt member-declarator-listopt ;
    #function-definition ;opt
    #::opt nested-name-specifier templateopt unqualified-id ;
    #using-declaration
    #template-declaration
def p_member_declaration(p):
    ''' member_declaration : 
                    | decl_specifier_seq member_declarator_list ';'
                    | member_declarator_list ';' 
                    | decl_specifier_seq ';'
                    | function_definition ';'
                    | function_definition '''
    print "member_declaration"
    pass 

#member-declarator-list:
    #member-declarator
    #member-declarator-list , member-declarator

def p_member_declarator_list(p):
    ''' member_declarator_list : member_declarator 
                    | member_declarator_list ',' member_declarator '''
    pass 
def p_decl_specifier_seq(p):
    ''' decl_specifier_seq : declaration_specifiers 
                        | decl_specifier_seq declaration_specifiers '''
    pass


def p_member_declarator_list_opt(p):
    ''' member_declarator_list_opt : 
                    | member_declarator_list'''
    pass 

#member-declarator:
    #declarator pure-specifieropt
    #declarator constant-initializeropt
    #identifieropt : constant-expression
def p_member_declarator_1(p):
    ''' member_declarator : declarator '''
    pass
  
def p_member_declarator_2(p):
    ''' member_declarator : declarator '=' constant_expression '''
    pass
  
def p_member_declarator_3(p):
    ''' member_declarator : identifier ':' constant_expression '''
    pass
  
def p_member_declarator_4(p):
    ''' member_declarator : ':' constant_expression '''
    pass 
######## DERIVED CLASSES ##############

#base-clause:
    #: base-specifier-list
def p_base_clause_opt(p):
    ''' base_clause_opt : 
                    | base_specifier_list '''
    pass 

#base-specifier-list:
    #base-specifier
    #base-specifier-list , base-specifier
def p_base_specifier_list(p):
    ''' base_specifier_list : base_specifier 
                    | base_specifier_list ',' base_specifier '''
    pass 

#base-specifier:
    #::opt nested-name-specifieropt class-name
    #virtual access-specifieropt ::opt nested-name-specifieropt class-name
    #access-specifier virtualopt ::opt nested-name-specifieropt class-name
def p_base_specifier(p):
    ''' base_specifier : double_colon_opt class_name 
                    | access_specifier double_colon_opt class_name ''' 
    pass 

def p_double_colon_opt(p):
    ''' double_colon_opt : 
                        |  DOUBLE_COLON '''
    pass




#############

def p_truct_or_union_specifier_1(t):
      '''struct_or_union_specifier : struct_or_union identifier '{' struct_declaration_list '}'
      '''
#print "struct_or_union_specifier : struct_or_union identifier '{' struct_declaration_list '}'"
		   

def p_struct_or_union_specifier_2(t):
      '''struct_or_union_specifier : struct_or_union '{' struct_declaration_list '}'
      '''
#print "struct_or_union_specifier : struct_or_union '{' struct_declaration_list '}'"
		   

def p_struct_or_union_specifier_3(t):
      '''struct_or_union_specifier : struct_or_union identifier'''
#print "struct_or_union_specifier : struct_or_union identifier"

def p_struct_or_union_1(t):
      '''struct_or_union : STRUCT'''
#print "struct_or_union : STRUCT"

def p_struct_or_union_2(t):
      '''struct_or_union : UNION'''
#print "struct_or_union : STRUCT"

def p_struct_declaration_list_1(t):
      '''struct_declaration_list : struct_declaration'''
#print "struct_declaration_list : struct_declaration"

def p_struct_declaration_list_2(t):
      '''struct_declaration_list : struct_declaration_list struct_declaration'''
#print "struct_declaration_list : struct_declaration_list struct_declaration"

def p_struct_declaration_1(t):
      '''struct_declaration : specifier_qualifier_list struct_declarator_list ';'
      '''
#print "struct_declaration_list : specifier_qualifier_list struct_declarator_list ;"


def p_specifier_qualifier_list_1(t):
      '''specifier_qualifier_list : type_specifier specifier_qualifier_list'''
#print "specifier_qualifier_list : type_specifier specifier_qualifier_list"

def p_specifier_qualifier_list_2(t):
      '''specifier_qualifier_list : type_specifier'''
#print "specifier_qualifier_list : type_specifier"
	

def p_specifier_qualifier_list_3(t):
      '''specifier_qualifier_list : type_qualifier specifier_qualifier_list'''
#print "specifier_qualifier_list : type_qualifier specifier_qualifier_list"

def p_specifier_qualifier_list_4(t):
      '''specifier_qualifier_list : type_qualifier'''
#print "specifier_qualifier_list : type_qualifier "

def p_struct_declarator_list_1(t):
      '''struct_declarator_list : struct_declarator'''
#print "struct_declarator_list : struct_declarator "

def p_struct_declarator_list_2(t):
      '''struct_declarator_list : struct_declarator_list ',' struct_declarator'''
#print "struct_declarator_list : struct_declarator_list ',' struct_declarator "

def p_struct_declarator_1(t):
      '''struct_declarator : declarator'''
#print "struct_declarator_list :  declarator "

def p_struct_declarator_2(t):
      '''struct_declarator : ':' constant_expression'''
#print "struct_declarator : ':' constant_expression "

def p_struct_declarator_3(t):
      '''struct_declarator : declarator ':' constant_expression'''
#print "struct_declarator : declarator ':' constant_expression "
      

def p_enum_specifier_1(t):
      '''enum_specifier : ENUM '{' enumerator_list '}'
      '''
#print "enum_specifier : ENUM '{' enumerator_list '}' "

def p_enum_specifier_2(t):
      '''enum_specifier : ENUM identifier '{' enumerator_list '}'
      '''
#print "enum_specifier : ENUM identifier '{' enumerator_list '}' "

def p_enum_specifier_3(t):
      '''enum_specifier : ENUM identifier'''
#print "enum_specifier : ENUM identifier"

def p_enumerator_list_1(t):
      '''enumerator_list : enumerator'''
#print "enumerator_list : enumerator"
      

def p_enumerator_list_2(t):
      '''enumerator_list : enumerator_list ',' enumerator'''
#print "enumerator_list : enumerator_list ',' enumerator"

def p_enumerator_1(t):
      '''enumerator : identifier'''
#print "enumerator : identifier"

def p_enumerator_2(t):
      '''enumerator : identifier '=' constant_expression'''
#print "enumerator : identifier '=' constant_expression"

def p_type_qualifier_1(t):
      '''type_qualifier : CONST'''
#print "type_qualifier : CONST"

def p_type_qualifier_2(t):
      '''type_qualifier : VOLATILE'''
#print "type_qualifier : VOLATILE"

def p_declarator_1(t):
      '''declarator : pointer declarator'''
#print "declarator : pointer declarator"

def p_declarator_2(t):
      '''declarator : direct_declarator'''
#print "declarator : direct_declarator"

def p_set_parameter_flag_1(t):
      '''set_parameter_flag : '''
      pass

def p_unset_parameter_flag_1(t):
      '''unset_parameter_flag : '''
      pass

def p_direct_declarator_1(t):
      '''direct_declarator : identifier'''
#print "direct_declarator : identifier"

def p_direct_declarator_2(t):
      '''direct_declarator : '(' declarator ')'
      '''
#print "direct_declarator : '(' declarator ')'"

def p_direct_declarator_3(t):
      '''direct_declarator : direct_declarator '[' constant_expression ']'
      '''
#print "direct_declarator : direct_declarator '[' constant_expression ']'"
	  
def p_direct_declarator_4(t):
      '''direct_declarator : direct_declarator '[' ']'
      '''
#print "direct_declarator : direct_declarator '[' ']'"

def p_direct_declarator_5(t):
      '''direct_declarator : direct_declarator '(' set_parameter_flag parameter_type_list unset_parameter_flag ')'
      '''
#print "direct_declarator : direct_declarator '(' set_parameter_flag parameter_type_list unset_parameter_flag ')'"
	
def p_direct_declarator_6(t):
      '''direct_declarator : direct_declarator '(' set_parameter_flag identifier_list unset_parameter_flag ')'
      '''
#print "direct_declarator : direct_declarator '(' set_parameter_flag identifier_list unset_parameter_flag ')'"
      
def p_direct_declarator_7(t):
      '''direct_declarator : direct_declarator '(' ')'
      '''
#print "direct_declarator : direct_declarator '(' ')'"

def p_pointer_1(t):
      '''pointer : '*'
      '''
#print " pointer : '*'"

def p_pointer_2(t):
      '''pointer : '*' type_qualifier_list'''
#print "pointer : '*' type_qualifier_list"

def p_pointer_3(t):
      '''pointer : '*' pointer'''
#print "pointer : '*' pointer"

def p_pointer_4(t):
      '''pointer : '*' type_qualifier_list pointer'''
#print "pointer : '*' type_qualifier_list pointer"

def p_type_qualifier_list_1(t):
      '''type_qualifier_list : type_qualifier'''
#print "type_qualifier_list : type_qualifier"

def p_type_qualifier_list_2(t):
      '''type_qualifier_list : type_qualifier_list type_qualifier'''
#print "type_qualifier_list : type_qualifier_list type_qualifier"


def p_parameter_type_list_1(t):
      '''parameter_type_list : parameter_list'''
#print "parameter_type_list : parameter_list"

def p_parameter_type_list_2(t):
      '''parameter_type_list : parameter_list ',' ELLIPSIS'''
#print "parameter_type_list : parameter_list ',' ELLIPSIS"

def p_parameter_list_1(t):
      '''parameter_list : parameter_declaration'''
#print "parameter_list : parameter_declaration"
     
def p_parameter_list_2(t):
      '''parameter_list : parameter_list ',' parameter_declaration'''
#print "parameter_list : parameter_list ',' parameter_declaration"

def p_parameter_declaration_1(t):
      '''parameter_declaration : declaration_specifiers declarator'''
#print "parameter_declaration : declaration_specifiers declarator"
      
def p_parameter_declaration_2(t):
      '''parameter_declaration : declaration_specifiers abstract_declarator'''
#print "parameter_declaration : declaration_specifiers abstract_declarator"

def p_parameter_declaration_3(t):
      '''parameter_declaration : declaration_specifiers'''
#print "parameter_declaration : declaration_specifiers"

def p_identifier_list_1(t):
      '''identifier_list : identifier'''
#print "parameter_declaration : declaration_specifiers"
	      
def p_identifier_list_2(t):
      '''identifier_list : identifier_list ',' identifier'''
#print "identifier_list : identifier_list ',' identifier"

def p_type_name_1(t):
      '''type_name : specifier_qualifier_list'''
#print "type_name : specifier_qualifier_list"

def p_type_name_2(t):
      '''type_name : specifier_qualifier_list abstract_declarator'''
#print "type_name : specifier_qualifier_list abstract_declarator"

def p_abstract_declarator_1(t):
      '''abstract_declarator : pointer'''
#print "abstract_declarator : pointer"

def p_abstract_declarator_2(t):
      '''abstract_declarator : direct_abstract_declarator'''
#print "abstract_declarator : direct_abstract_declarator"

def p_abstract_declarator_3(t):
      '''abstract_declarator : pointer direct_abstract_declarator'''
#print "abstract_declarator : pointer direct_abstract_declarator"

def p_direct_abstract_declarator_1(t):
      '''direct_abstract_declarator : '(' abstract_declarator ')'
      '''
#print "direct_abstract_declarator : '(' abstract_declarator ')'"

def p_direct_abstract_declarator_2(t):
      '''direct_abstract_declarator : '[' ']'
      '''
#print "abstract_declarator : pointer direct_abstract_declarator"

def p_direct_abstract_declarator_3(t):
      '''direct_abstract_declarator : '[' constant_expression ']'
      '''
#print "direct_abstract_declarator : '[' constant_expression ']'"

def p_direct_abstract_declarator_4(t):
      '''direct_abstract_declarator : direct_abstract_declarator '[' ']'
      '''
#print "direct_abstract_declarator : direct_abstract_declarator '[' ']'"

def p_direct_abstract_declarator_5(t):
      '''direct_abstract_declarator : direct_abstract_declarator '[' constant_expression ']'
      '''
#print "direct_abstract_declarator : direct_abstract_declarator '[' constant_expression ']'"

def p_direct_abstract_declarator_6(t):
      '''direct_abstract_declarator : '(' ')'
      '''
#print "direct_abstract_declarator : '(' ')'"

def p_direct_abstract_declarator_7(t):
      '''direct_abstract_declarator : '(' parameter_type_list ')'
      '''
#print "direct_abstract_declarator : '(' parameter_type_list ')'"
      

def p_direct_abstract_declarator_8(t):
      '''direct_abstract_declarator : direct_abstract_declarator '(' ')'
      '''
#print "direct_abstract_declarator : direct_abstract_declarator '(' ')'"
            

def p_direct_abstract_declarator_9(t):
      '''direct_abstract_declarator : direct_abstract_declarator '(' parameter_type_list ')'
      '''
#print "direct_abstract_declarator : direct_abstract_declarator '(' parameter_type_list ')'"

def p_initializer_1(t):
      '''initializer : assignment_expression'''
#print "initializer : assignment_expression"

def p_initializer_2(t):
      '''initializer : '{' initializer_list '}'
      '''
#print "initializer : '{' initializer_list '}'"

def p_initializer_3(t):
      '''initializer : '{' initializer_list ',' '}'
      '''
#print "initializer : '{' initializer_list ',' '}'"

def p_initializer_list_1(t):
      '''initializer_list : initializer'''
#print "initializer_list : initializer"

def p_initializer_list_2(t):
      '''initializer_list : initializer_list ',' initializer'''
#print "initializer_list : initializer_list ',' initializer"

def p_statement_1(t):
      '''statement : labeled_statement'''
#print "\nstatement : labeled_statement\n"

def p_statement_2(t):
      '''statement : compound_statement'''
#print "\nstatement : compound_statement\n"

def p_statement_3(t):
      '''statement : expression_statement'''
#print "\nstatement : expression_statement\n"

def p_statement_4(t):
      '''statement : selection_statement'''
#print "\nstatement : selection_statement\n"

def p_statement_5(t):
      '''statement : iteration_statement'''
#print "\nstatement : iteration_statement\n"

def p_statement_6(t):
      '''statement : jump_statement'''
#print "\nstatement : jump_statement\n"

def p_labeled_statement_1(t):
      '''labeled_statement : identifier ':' statement'''
#print "\nlabeled_statement : identifier ':' statement\n"

def p_labeled_statement_2(t):
      '''labeled_statement : CASE constant_expression ':' statement'''
#print "\nlabeled_statement -> CASE constant_expression ':' statement\n"

def p_labeled_statement_3(t):
      '''labeled_statement : DEFAULT ':' statement'''
#print "\nlabeled_statement : DEFAULT ':' statement\n"

def p_compound_statement_1(t):
      '''compound_statement : '{' '}'
      '''
#print "\ncompound_statement : '{' '}'\n"

def p_compound_statement_2(t):
      '''compound_statement : '{' new_scope compound_statement_list finish_scope '}'
      '''
#print "\ncompound_statement : '{' new_scope compound_statement_list finish_scope '}'\n"

def p_compound_statement_3(t):
      '''compound_statement : '{' new_scope compound_declaration_list finish_scope '}'
      '''
#print "\ncompound_statement : '{' new_scope compound_declaration_list finish_scope '}'\n"

def p_compound_statement_list_1(t):
      '''compound_statement_list : declaration_list'''
#print "\ncompound_statement_list : declaration_list\n"

def p_compound_statement_list_2(t):
      '''compound_statement_list : declaration_list compound_declaration_list'''
#print "\ncompound_statement_list : declaration_list compound_declaration_list\n"

def p_compound_declaration_list_1(t):
      '''compound_declaration_list : statement_list'''
#print "\ncompound_declaration_list : statement_list\n"

def p_compound_declaration_list_2(t):
      '''compound_declaration_list : statement_list compound_statement_list'''
#print "\ncompound_declaration_list : statement_list compound_statement_list\n"

def p_declaration_list_1(t):
      '''declaration_list : declaration'''
#print "\ndeclaration_list : declaration\n"

def p_declaration_list_2(t):
      '''declaration_list : declaration_list declaration'''
#print "\ndeclaration_list : declaration_list declaration\n"

def p_statement_list_1(t):
      '''statement_list : statement'''
#print "\nstatement_list : statement\n"

def p_statement_list_2(t):
      '''statement_list : statement_list statement'''
#print "\nstatement_list : statement_list statement\n"

def p_expression_statement_1(t):
      '''expression_statement : ';'
      '''
#print "\nexpression_statement : ';'\n"

def p_expression_statement_2(t):
      '''expression_statement : expression ';'
      '''
#print "\nexpression_statement : expression ';'\n"

def p_expression_statement_3(t):
      '''expression_statement : expression error'''
#print "\nexpression_statement : expression error\n"

def p_get_labels_1(t):
      '''get_labels : '''
#print "\nget_labels : \n"

def p_release_labels_1(t):
      '''release_labels : '''
#print "\nrelease_labels : \n"
      

def p_switch_label_1(t):
      '''switch_label : '''
#print "\nswitch_label : \n"
      
def p_release_switch_label_1(t):
      '''release_switch_label : '''
#print "\nrelease_switch_label : \n"
      
def p_selection_statement_1(t):
      '''selection_statement : IF '(' expression ')' statement %prec IFX'''
#print "\nselection_statement : IF '(' expression ')' statement %prec IFX\n"
      

def p_selection_statement_2(t):
      '''selection_statement : IF '(' expression ')' statement ELSE statement'''
#print "\nselection_statement : IF '(' expression ')' statement ELSE statement\n"

def p_selection_statement_3(t):
      '''selection_statement : SWITCH get_labels '(' expression ')' switch_label statement release_switch_label release_labels'''
#print "\nselection_statement : SWITCH get_labels '(' expression ')' switch_label statement release_switch_label release_labels\n"

def p_iteration_statement_1(t):
      '''iteration_statement : WHILE get_labels '(' expression ')' statement release_labels'''
#print "\niteration_statement : WHILE get_labels '(' expression ')' statement release_labels\n"

def p_iteration_statement_2(t):
      '''iteration_statement : DO get_labels statement WHILE '(' expression ')' ';' release_labels'''
#print "\niteration_statement : DO get_labels statement WHILE '(' expression ')' ';' release_labels\n"

def p_iteration_statement_3(t):
      '''iteration_statement : FOR get_labels '(' expression_statement expression_statement _embed0_iteration_statement ')' statement release_labels'''
#print "\niteration_statement : FOR get_labels '(' expression_statement expression_statement _embed0_iteration_statement ')' statement release_labels\n"

def p_iteration_statement_4(t):
      '''iteration_statement : FOR get_labels '(' expression_statement expression_statement expression _embed1_iteration_statement ')' statement release_labels'''
#print "\niteration_statement : FOR get_labels '(' expression_statement expression_statement expression _embed1_iteration_statement ')' statement release_labels\n"

def p__embed0_iteration_statement(t):
      '''_embed0_iteration_statement : '''
#print "\n_embed0_iteration_statement : \n"

def p__embed1_iteration_statement(t):
      '''_embed1_iteration_statement : '''
#print "\n_embed1_iteration_statement : \n"

def p_jump_statement_1(t):
      '''jump_statement : GOTO identifier ';'
      '''
#print "\njump_statement : GOTO identifier ';'\n"


def p_jump_statement_2(t):
      '''jump_statement : CONTINUE ';'
      '''
#print "\njump_statement : CONTINUE ';'\n"

def p_jump_statement_3(t):
      '''jump_statement : BREAK ';'
      '''
#print "\njump_statement : BREAK ';'\n"

def p_jump_statement_4(t):
      '''jump_statement : RETURN ';'
      '''
#print "\njump_statement : RETURN ';'\n"

def p_jump_statement_5(t):
      '''jump_statement : RETURN expression ';'
      '''
#print "\njump_statement : RETURN expression ';'\n"

def p_strt_1(t):
      '''strt : strt1'''
#print "strt : strt1"

def p_strt1_1(t):
      '''strt1 : external_declaration'''
#print "\nstrt1 : external_declaration\n"

def p_strt1_2(t):
      '''strt1 : strt1 external_declaration'''
#print "\nstrt1 : strt1 external_declaration\n"

def p_external_declaration_1(t):
      '''external_declaration : function_definition'''
#print "\nexternal_declaration : function_definition\n"

def p_external_declaration_2(t):
      '''external_declaration : declaration'''
#print "\nexternal_declaration : declaration\n"
      

def p_function_scope_1(t):
      '''function_scope : '''      
#print "\nfunction_scope : \n"            

def p_unset_function_scope_1(t):
      '''unset_function_scope : '''
#print "\nunset_function_scope : \n"


def p_function_definition_1(t):
      '''function_definition : declaration_specifiers declarator declaration_list function_scope get_labels compound_statement release_labels unset_function_scope'''
#print "\nfunction_definition : declaration_specifiers declarator declaration_list function_scope get_labels compound_statement release_labels unset_function_scope\n"
      
def p_function_definition_2(t):
      '''function_definition : declaration_specifiers declarator function_scope get_labels compound_statement release_labels unset_function_scope'''
#print "\nfunction_definition : declaration_specifiers declarator function_scope get_labels compound_statement release_labels unset_function_scope\n"
			      
def p_function_definition_3(t):
      '''function_definition : declarator declaration_list function_scope get_labels compound_statement release_labels unset_function_scope'''
#print "\nfunction_definition : declarator declaration_list function_scope get_labels compound_statement release_labels unset_function_scope\n"
      
def p_function_definition_4(t):
      '''function_definition : declarator function_scope get_labels compound_statement release_labels unset_function_scope'''
#print "\nfunction_definition : declarator function_scope get_labels compound_statement release_labels unset_function_scope\n"
      
# -------------- RULES END ----------------
import ply.yacc as yacc
yacc.yacc()
import sys

#file = open('sample.cpp','r')
try:
	f1 = open(sys.argv[1])
	yacc.parse(f1.read())
	if success:
            print 'Compilation Successful with No Error !!!'
except IOError:
    print 'Could not open file:',  sys.argv[1]

