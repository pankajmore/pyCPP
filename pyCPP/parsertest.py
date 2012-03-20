from lexer import *
import ply.yacc as yacc



#  ---------------------------------------------------------------
#  ABSTRACT SYNTAX TREE - NODES
#  ---------------------------------------------------------------


# abstract out the generic methods in this class

# define new child classes for each token (non-terminal symbol) type and inherit from Node

# is it necessary to define separate nodes for Type System?



# define functions for each production rule and their attribute grammer/action

########### Start ################
def p_identifier_1(t):
    '''identifier : IDENTIFIER'''
    pass

def p_translation_unit(p):
    ''' translation_unit : declaration_seq_opt '''
    pass
    ### TODO 

#declaration-seq:
    #declaration
    #declaration-seq declaration
def p_declaration_seq_opt(p):
    ''' declaration_seq_opt : empty
                           | declaration_seq_opt declaration  '''
    pass

def p_empty(p):
    ''' empty : '''
    pass

#declaration:
    #block-declaration
    #function-definition
    #template-declaration
    #explicit-instantiation
    #explicit-specialization
    #linkage-specification
    #namespace-definition

def p_declaration(p):
    ''' declaration : block_declaration 
                    | function_definition 
                    | linkage_specialization 
                    | namespace_definition '''
    pass

#block-declaration:
    #simple-declaration
    #asm-definition
    #namespace-alias-definition
    #using-declaration
    #using-directive

def p_block_declaration(p):
    ''' block-declaration : simple_declaration '''
    pass
    
    
lex.lex()
yacc.yacc()