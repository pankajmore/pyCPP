import lexer
import ply.yacc as yacc



#  ---------------------------------------------------------------
#  ABSTRACT SYNTAX TREE - NODES
#  ---------------------------------------------------------------

class Node:
    """Base class for all the nodes in the AST"""

# abstract out the generic methods in this class

# define new child classes for each token (non-terminal symbol) type and inherit from Node

# is it necessary to define separate nodes for Type System?



# define functions for each production rule and their attribute grammer/action

## Start 


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
                    | template_declaration 
                    | explicit_instantiation 
                    | explicit_specialization 
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

#simple-declaration:
    #decl-specifier-seqopt init-declarator-listopt ;

def p_simple_declaration(p):
    ''' simple_declaration : SEMICOLON  
                           | decl_specifier_seq init_declarator_list SEMICOLON
                           | decl_specifier_seq SEMICOLON 
                           | init_declarator_list SEMICOLON '''
    pass

#decl-specifier-seq:
    #decl-specifier-seqopt decl-specifier

def p_decl_specifier_seq(p):
    ''' decl_specifier_seq : decl_specifier 
                        | decl_specifier_seq decl_specifier '''
    pass

#decl-specifier:
    #storage-class-specifier
    #type-specifier
    #function-specifier
    #friend
    #typedef

def p_decl_specifier(p):
    ''' decl_specifier : storage_class_specifier 
                        | type_specifier 
                        | function_specifier '''
    pass

#storage-class-specifier:
    #auto
    #register
    #static
    #extern
    #mutable

def p_storage_class_specifier(p):
    ''' storage_class_specifier :'''
    pass 

#function-specifier:
    #inline
    #virtual
    #explicit

def p_function_specifier(p):
    ''' function_specifier : INLINE '''
    pass 

#type-specifier:
    #simple-type-specifier
    #class-specifier
    #enum-specifier
    #elaborated-type-specifier
    #cv-qualifier

def p_type_specifier(p):
    ''' type_specifier : simple_type_specifier 
                        | class_specifier
                        | elaborated_type_specifier
                        | cv_qualifier '''
    pass 
## HELPER 

def p_double_colon_opt(p):
    ''' double_colon_opt : 
                        | COLON COLON '''
    pass

##

#simple-type-specifier:
    #::opt nested-name-specifieropt type-name
    #::opt nested-name-specifier templateopt template-id
    #char
    #wchar_t
    #bool
    #short
    #int
    #long
    #signed
    #unsigned
    #float
    #double
    #void


def p_simple_type_specifier(p):
    ''' simple_type_specifier : double_colon_opt nested_name_specifier type_name
                            | BOOL 
                            | CHAR 
                            | INT 
                            | FLOAT 
                            | DOUBLE 
                            | VOID '''
    pass 

#type-name:
    #class-name
    #enum-name    
    #typedef-name

def p_type_name(p):
    ''' type_name : class_name ''' 
    pass 

#elaborated-type-specifier:
    #class-key ::opt nested-name-specifieropt identifier
    #enum ::opt nested-name-specifieropt identifier
    #typename ::opt nested-name-specifier identifier
    #typename ::opt nested-name-specifier templateopt template-id
def p_elaborated_type_specifier(p):
    ''' elaborated_type_specifier : class_key double_colon_opt nested_name_specifier identifier '''

#nested-name-specifier:
    #class-or-namespace-name :: nested-name-specifieropt
    #class-or-namespace-name :: template nested-name-specifier

def p_nested_name_specifier(p):
    ''' nested_name_specifier : 
                            | class_name COLON COLON nested_name_specifier '''
    pass

##### DECLARATORS #####

#init-declarator-list:
    #init-declarator
    #init-declarator-list , init-declarator
def p_init_declarator_list(p):
    ''' init_declarator_list : init_declarator 
                            | init_declarator_list , init_declarator '''
    pass 

#init-declarator:
    #declarator initializeropt
def p_init_declarator(p): 
    ''' init_declarator : declarator initializer_opt '''
    pass 

#declarator:
    #direct-declarator
    #ptr-operator declarator
def p_declarator(p):
    ''' declarator : direct_declarator 
                    | ptr_direct_declarator '''
    pass 

#direct-declarator:
    #declarator-id
    #direct-declarator ( parameter-declaration-clause ) cv-qualifier-seqopt exception-specificationopt
    #direct-declarator [ constant-expressionopt ]
    #( declarator )

def p_direct_declarator(p):
    ''' direct_declarator : declarator_id 
                    | direct_declarator LPAREN parameter_declaration_clause RPAREN cv_qualifier_seq_opt exception_specification_opt 
                    | direct_declarator LBRACKET constant_expression_opt RBRACKET 
                    | LPAREN declarator RPAREN '''
    pass 

#ptr-operator:
    #* cv-qualifier-seqopt
    #&
    #::opt nested-name-specifier * cv-qualifier-seqopt
def p_ptr_operator(p):
    ''' ptr_operator : TIMES cv_qualifier_seq_opt 
                    | AMPERSAND 
                    | double_colon_opt nested_name_specifier TIMES cv_qualifier_seq_opt '''
    pass 

#cv-qualifier-seq:
    #cv-qualifier cv-qualifier-seqopt
def p_cv_qualifier_seq_opt(p):
    ''' cv_qualifier_seq_opt : 
                            | cv_qualifier cv_qualifier_seq_opt '''
    pass 

#cv-qualifier:
    #const
    #volatile

def p_cv_qualifier(p):
    ''' cv_qualifier : '''
    pass 

#declarator-id:
    #::opt id-expression
    #::opt nested-name-specifieropt type-name
def p_declarator_id(p):
    ''' declarator_id : double_colon_opt id_expression 
                    | double_colon_opt type_name
                    | double_colon_opt nested_name_specifier type_name '''

#type-id:
    #type-specifier-seq abstract-declaratoropt
def p_type_id(p):
    ''' type_id : type_specifier_seq abstract_declarator_opt '''
    pass

#type-specifier-seq:
    #type-specifier type-specifier-seqopt
def p_type_specifier_seq(p):
    ''' type_specifier_seq : type_specifier 
                    | type_specifier type_specifier_seq '''
    pass 

#abstract-declarator:
    #ptr-operator abstract-declaratoropt
    #direct-abstract-declarator
def p_abstract_declarator(p):
    ''' abstract_declarator : ptr_operator abstract_declarator_opt
                    | direct_abstract_declarator '''
    pass

def p_abstract_declarator_opt(p):
    ''' abstract_declarator_opt : 
                    | abstract_declarator '''
    pass

#direct-abstract-declarator:
    #direct-abstract-declaratoropt ( parameter-declaration-clause ) cv-qualifier-seqopt exception-specificationopt
    #direct-abstract-declaratoropt [ constant-expressionopt ]
    #( abstract-declarator )
def p_direct_abstract_declarator(p):
    ''' direct_abstract_declarator : direct_abstract_declarator_opt LPAREN parameter_declaration_clause RPAREN cv_qualifier_seq_opt exception_specification_opt 
                    | direct_abstract_declarator_opt LBRACKET constant_expression_opt RBRACKET 
                    | LPAREN abstract_declarator RPAREN '''
    pass 

def p_direct_abstract_declarator_opt(p):
    ''' direct_abstract_declarator_opt : 
                    | direct_abstract_declarator '''
    pass 

#parameter-declaration-clause:
    #parameter-declaration-listopt ...opt
    #parameter-declaration-list , ...
def p_parameter_declaration_clause(p):
    ''' parameter_declaration_clause : 
                    | parameter_declaration_list 
                    | parameter_declaration_list DOT DOT DOT 
                    | DOT DOT DOT 
                    | parameter_declaration_list COMMA DOT DOT DOT '''
    pass 

#parameter-declaration-list:
    #parameter-declaration
    #parameter-declaration-list , parameter-declaration
def p_parameter_declaration_list(p):
    ''' parameter_declaration_list : parameter_declaration 
                    | parameter_declaration_list COMMA parameter_declaration '''
    pass 

#parameter-declaration:
    #decl-specifier-seq declarator
    #decl-specifier-seq declarator = assignment-expression
    #decl-specifier-seq abstract-declaratoropt
    #decl-specifier-seq abstract-declaratoropt = assignment-expression

def p_parameter_declaration(p):
    ''' parameter_declaration : decl_specifier_seq declarator 
                    | decl_specifier_seq declarator ASSIGN assignment_expression 
                    | decl_specifier_seq abstract_declarator_opt 
                    | decl_specifier_seq abstract_declarator_opt = assignment_expression ''' 
    pass

#function-definition:
    #decl-specifier-seqopt declarator ctor-initializeropt function-body
    #decl-specifier-seqopt declarator function-try-block
def p_function_definition(p):
    ''' function_definition : declarator ctor_initializer_opt function_body 
                    | decl_specifier_seq  declarator ctor_initializer_opt function_body 
                    | declarator function_try_block 
                    | decl_specifier_seq declarator function_try_block '''
    pass

#function-body:
    #compound-statement
def p_function_body(p):
    ''' function_body : compound_statement ''' 
    pass

#initializer:
    #= initializer-clause
    #( expression-list )

def p_initializer_opt(p):
    ''' initializer_opt:
                    | initializer_clause 
                    | LPAREN expression_list RPAREN ''' 

#initializer-clause:
    #assignment-expression
    #{ initializer-list ,opt }
    #{ }
def p_initializer_clause(p):
    ''' initializer_clause : assignment_expression 
                    | LBRACE initializer_list RBRACE 
                    | LBRACE RBRACE '''
    pass 

#initializer-list:
    #initializer-clause
    #initializer-list , initializer-clause
def p_initializer_list(p):
    ''' initializer_list : initializer_clause
                    | initializer_list COMMA initializer_clause ''' 
    pass 


##### CLASSES #####     


#class-key:
    #class
    #struct
    #union

def p_class_key(p):
    ''' class_key : CLASS 
                    | STRUCT '''
    pass

def p_error(p):
    print("Whoa. We're hosed")

yacc.yacc(method='LALR')
