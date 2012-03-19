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

    
    
    
lex.lex()
yacc.yacc()