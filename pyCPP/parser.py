import lexer
import ply.yacc as yacc
import symbol



#  ---------------------------------------------------------------
#  ABSTRACT SYNTAX TREE - NODES
#  ---------------------------------------------------------------
MaxPar=10
DEBUG  = False 

class Attribute:
    global MaxPar
      def __init__(self):
            self.id = ""
            self.type = None
            self.isArray = 0    #// True if variable is array
            self.ArrayLimit = 0 # upper limit of array (valid if DIMENSION is true)
            self.width = 0
            self.isPointer = 0
            self.qualifier = 0
            self.specifier = 0
            self.storage = 0
            self.scope = 0
            self.value=None    
            self.isFunction = 0
            self.numParameters = 0
            self.isString = 0
            self.offset = 0
            self.parameterList = [None]*MaxPar


def copyAttribute(a1):      
      i = 0
      a = Attribute()
      a.id=None
      if a1.id != None:
          a.id = a1.id

      a.type=a1.type
      a.isArray=a1.isArray
      a.ArrayLimit=a1.ArrayLimit
      a.width=a1.width
      a.isPointer=a1.isPointer
      a.qualifier=a1.qualifier
      a.specifier=a1.specifier
      a.storage=a1.storage
      a.scope=a1.scope
      a.value=a1.value
      a.isFunction=a1.isFunction
      a.isString=a1.isString
      a.offset=a1.offset
      a.numParameters=a1.numParameters
      #ParameterList      
      for i in range(a1.numParameters):
	    if a1.parameterList[i] == None:
		  break
	    a.parameterList[i] = copyAttribute(a1.parameterList[i])
      return a

def initAttr(a):
      a.id=None
      a.type=None	
      a.isArray=0		# True if variable is array
      a.ArrayLimit=0	#upper limit of array (valid if DIMENSION is true)
      a.width=0
      a.isPointer=0
      a.qualifier=0
      a.specifier=0
      a.storage=0
      a.scope=0
      a.value=None
      a.isString=0
      a.offset=0			#0 means not
      a.numParameters=0
      a.isFunction=0
      for i in range(MaxPar):      
	    a.parameterList[i]=None
      return a

def check_compatibility_relational(p):
    if p[1].type in ['FLOAT','INT'] and p[3].type in ['FLOAT','INT']:
        return True
    elif p[1].type=='CHAR' and p[3].type=='CHAR' :
        return True
    elif p[1].type=='BOOL' and p[3].type=='BOOL' :
        return True
    else:
        print "Error in line %s : Relational operator cannot be applied to %s , %s",%(p.lineno(2),p[1].type,p[3].type)
        return False               

start='translation_unit'
## Scoping rules defined 

env = Environment(None)
saveenv = None 
def NewScope():
    global env 
    env = Environment(env)

def PopScope():
    global env  
    env = env.prev 

def p_new_scope(p):
    '''new_scope : '''
    NewScope()

def p_finish_scope(p):
    '''finish_scope : '''
    PopScope()
    




# define functions for each production rule and their attribute grammer/action

########### Start ################


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

#################### EXPRESSIONS ###################
#primary-expression:
    #literal
    #this
    #:: identifier
    #:: operator-function-id
    #:: qualified-id
    #( expression )
    #id-expression

# Reduced the no. of productions for primary_expression

def p_literal_1(t):
    '''literal : INUMBER '''
    t[0]=Attribute()
    t[0].type='INT'
    t[0].value=int(t[1])

def p_literal_2(t):
    '''literal : DNUMBER '''
    t[0]=Attribute()
    t[0].type='FLOAT'
    t[0].value=float(t[1])

def p_literal_3(t):
    '''literal : LIT_CHAR '''
    t[0]=Attribute()
    t[0].type='CHAR'
    t[0].value=str(t[1])

def p_literal_4(t):
    '''literal : LIT_STRING '''
    t[0]=Attribute()
    t[0].type='CHAR'  #Need to figure out the type that should be given to string
    t[0].isArray=1
    t[0].value=t[1]
    t[0].isString=1

def p_literal_5(t):
    '''literal : TRUE '''
    t[0]=Attribute()
    t[0].type='BOOL'
    t[0].value=bool(t[1])

def p_literal_6(t):
    '''literal : FALSE '''
    t[0]=Attribute()
    t[0].type='BOOL'
    t[0].value=bool(t[1])
    
def p_primary_expression_1(p):
    ''' primary_expression : literal'''
    p[0]=copyAttribute(p[1])

def p_primary_expression_2(p):
    ''' primary_expression : identifier'''
    if p[1].type ==None:
        p[0]=Attribute()
        print 'Error in line %s : Type of identifier not defined',% p.lineno(1)
    else:
        p[0]=copyAttribute(p[1])

def p_primary_expression_3(p):
    ''' primary_expression : LPAREN expression RPAREN '''
    p[0]=copyAttribute(p[1])

#Not included in grammer
    
#id-expression:
    #unqualified-id
    #qualified-id
def p_id_expression(p):
    ''' id_expression : unqualified_id 
                    | qualified_id '''
    pass 

#unqualified-id:
    #identifier
    #operator-function-id
    #conversion-function-id
    #~ class-name
    #template-id
def p_unqualified_id(p):
    ''' unqualified_id : identifier 
                    | operator_function_id 
                    | conversion_function_id 
                    | TILDE class_name '''
    pass 

#qualified-id:
    #nested-name-specifier templateopt unqualified-id
def p_qualified_id(p):
    ''' qualified_id : nested_name_specifier unqualified_id '''
    pass 

#nested-name-specifier:
    #class-or-namespace-name :: nested-name-specifieropt
    #class-or-namespace-name :: template nested-name-specifier
#nested-name-specifier:
    #class-or-namespace-name :: nested-name-specifieropt
    #class-or-namespace-name :: template nested-name-specifier
def p_nested_name_specifier(p):
    ''' nested_name_specifier : class_name DOUBLE_COLON nested_name_specifier_opt '''
    p[0] = [p[1]] + p[3]
def p_nested_name_specifier_opt_1(p):
    ''' nested_name_specifier_opt : '''
    p[0] = [] 
def p_nested_name_specifier_opt_2(p):
    ''' nested_name_specifier_opt : nested_name_specifier '''
    p[0] = p[1]

def find_scope(nested_specifier):
    global env 
    p = env 
    for i in nested_specifier :
        cl = p.get(i)
        p = cl.attrs["scope"]
    return p 


#postfix-expression:
    #primary-expression
    #postfix-expression [ expression ]
    #postfix-expression ( expression-listopt )
    #simple-type-specifier ( expression-listopt )
    #typename ::opt nested-name-specifier identifier ( expression-listopt )
    #typename ::opt nested-name-specifier templateopt template-id ( expression-listopt )
    #postfix-expression . templateopt ::opt id-expression
    #postfix-expression -> templateopt ::opt id-expression
    #postfix-expression . pseudo-destructor-name
    #postfix-expression -> pseudo-destructor-name
    #postfix-expression ++
    #postfix-expression --
    #dynamic_cast < type-id > ( expression )
    #static_cast < type-id > ( expression )
    #reinterpret_cast < type-id > ( expression )
    #const_cast < type-id > ( expression )
    #typeid ( expression )
    #typeid ( type-id )
def p_postfix_expression_1(p):
    ''' postfix_expression : primary_expression '''
    p[0]=copyAttribute(p[1])

def p_postfix_expression_2(p):
    ''' postfix_expression :  postfix_expression LBRACKET expression RBRACKET '''
    p[0]=copyAttribute(p[1])
    if p[0].isArray!=1:
        print "Error in line %s : Cannot access index of non-array ",% p.lineno(2)
        p[0]=initAttribute(p[0])
    else: # for now only handling 1-d arrays
        if p[0].type not in ['FLOAT','INT','CHAR','BOOL']:
            print "Error in line %s : Unidentified type of array ",% p.lineno(2)
            p[0]=initAttribute(p[0])
        else:
            if p[3].type!='INT':
                print "Error in line %s : Index of array can only be an integer ",% p.lineno(2)
                p[0]=initAttribute(p[0])
            else:
                p[0].isArray=0
                #Determine p[0].value
                # p[0].value= p[1].value[p[3].value]
                
            
def p_postfix_expression_3(p):
    ''' postfix_expression : postfix_expression LPAREN  RPAREN '''
    p[0]=copyAttribute(p[1])
    if p[1].isFunction!=1:
        print "Error in line %s : Cannot use () on non-function %s ",% (p.lineno(2),p[1].id)
        p[0]=initAttribute(p[0])
    elif p[0].type not in ['FLOAT','INT','CHAR','BOOL']:
        print "Error in line %s : Unidentified type of function %s",% (p.lineno(2),p[1].id)
        p[0]=initAttribute(p[0])
    else:
        p[0].isFunction=0
        p[0].numParameters=0

def p_postfix_expression_4(p):
    ''' postfix_expression : postfix_expression LPAREN  expression_list RPAREN '''
    #Default arguments not supported as of now
    #Implicit type conversion not supported as of now
    p[0]=copyAttribute(p[1])
    if p[1].isFunction!=1:
        print "Error in line %s : Cannot use () on non-function %s ",% (p.lineno(2),p[1].id)
        p[0]=initAttribute(p[0])
    else:
        p[0].isFunction=0
        if p[1].numParameters!=p[3].numParameters:
            print "Error in line %s : Function %s requires %s arguments, given %s arguments ",%( p.lineno(2), p[1].id,p[1].numParameters,p[3].numParameters)
            p[0]=initAttribute(p[0])
        else:
            tmp=0
            for i in range(p[0].numParameters):
                if p[1].parameterList[i].type!=p[3].parameterList[i].type:
                    print "Error in line %s : Parameter %s of Function %s must be %s , given %s ",%( p.lineno(2), str(i+1), p[1].id, find_type(p[1].parameterList[i]), find_type(p[3].parameterList[i]))
                    tmp=1
                if tmp==1:
                    p[0]=initAttribute(p[0]) 
        p[0].numParameters=0
        
def p_postfix_expression_5(p):
    ''' postfix_expression : postfix_expression DOT identifier'''
    

def p_postfix_expression_6(p): 
    ''' postfix_expression : postfix_expression ARROW identifier'''

def p_postfix_expression_7(p):
    ''' postfix_expression : postfix_expression PLUS_PLUS '''

def p_postfix_expression_8(p):
    ''' postfix_expression : postfix_expression MINUS_MINUS '''

#expression-list:
    #assignment-expression
    #expression-list , assignment-expression
def p_expression_list(p):
    ''' expression_list : assignment_expression 
                    | expression_list COMMA assignment_expression '''
    pass 

#The production rules for expression_list_opt have beeen directly substitued
def p_expression_list_opt(p):
    ''' expression_list_opt :
                    | expression_list '''
    pass 

#pseudo-destructor-name:
    #::opt nested-name-specifieropt type-name :: ~ type-name
    #::opt nested-name-specifier template template-id :: ~ type-name
    #::opt nested-name-specifieropt ~ type-name
def p_pseudo_destructor_name(p):
    ''' pseudo_destructor_name : double_colon_opt nested_name_specifier_opt type_name COLON COLON TILDE type_name
                    | double_colon_opt nested_name_specifier_opt TILDE type_name '''
    pass 

#unary-expression:
    #postfix-expression
    #++ cast-expression
    #-- cast-expression
    #unary-operator cast-expression
    #sizeof unary-expression
    #sizeof ( type-id )
    #new-expression
    #delete-expression
def p_unary_expression(p):
    ''' unary_expression : postfix_expression 
                    | PLUS_PLUS cast_expression 
                    | MINUS_MINUS cast_expression 
                    | unary_operator cast_expression 
                    | SIZEOF unary_expression 
                    | SIZEOF LPAREN type_id RPAREN 
                    | new_expression 
                    | delete_expression '''
    if len(t)==3:
        if t[1]=='++':
            pass
        elif t[1]=='--':
            pass
        elif t[1]==
    pass

#unary-operator: one of
#* & + - ! ~
def p_unary_operator(p):
    ''' unary_operator : TIMES 
                    | AMPERSAND 
                    | PLUS 
                    | MINUS 
                    | EXCLAMATION 
                    | TILDE '''
    pass 

#new-expression:
    #::opt new new-placementopt new-type-id new-initializeropt
    #::opt new new-placementopt ( type-id ) new-initializeropt
def p_new_expression(p):
    ''' new_expression : double_colon_opt NEW new_placement_opt new_type_id new_initializer_opt 
                    | double_colon_opt NEW new_placement_opt LPAREN type_id RPAREN new_initializer_opt '''
    pass 

#new-placement:
    #( expression-list )
def p_new_placement(p): 
    ''' new_placement : LPAREN expression_list RPAREN '''
    pass 
def p_new_placement_opt(p):
    ''' new_placement_opt : 
                    | new_placement '''
    pass 

#new-type-id:
    #type-specifier-seq new-declaratoropt
def p_new_type_id(p):
    ''' new_type_id : type_specifier_seq new_declarator_opt '''
    pass 

#new-declarator:
    #ptr-operator new-declaratoropt
    #direct-new-declarator
def p_new_declarator_opt(p):
    ''' new_declarator_opt : 
                    | ptr_operator new_declarator_opt 
                    | direct_new_declarator '''
    pass 

#direct-new-declarator:
    #[ expression ]
    #direct-new-declarator [ constant-expression ]
def p_direct_new_declarator(p):
    ''' direct_new_declarator : LBRACKET expression RBRACKET 
                    | direct_new_declarator LBRACKET constant_expression RBRACKET '''
    pass 

#new-initializer:
    #( expression-listopt )
def p_new_initializer_opt(p): 
    ''' new_initializer_opt : 
                    | LPAREN expression_list_opt RPAREN '''
    pass 

#delete-expression:
    #::opt delete cast-expression
    #::opt delete [ ] cast-expression
def p_delete_expression(p):
    ''' delete_expression : double_colon_opt DELETE cast_expression 
                    | double_colon_opt DELETE LBRACKET RBRACKET cast_expression '''
    pass 

#cast-expression:
    #unary-expression
    #( type-id ) cast-expression
def p_cast_expression_1(p):
    ''' cast_expression : unary_expression'''
    p[0]=copyAttribute(p[1])


def p_cast_expression_2(p):
    '''cast_expression : LPAREN type_id RPAREN cast_expression '''
        p[0]=copyAttribute(p[4])
        #TODO : Add support for type conversion with pointers i.e (int*), (char*), etc.
        if p[4].type=p[2].type:
            if p[2].value == 'FLOAT' and p[4].type=='INT':
                p[0].type='FLOAT'
                p[0].value=float(p[4].value)
            elif p[2].value == 'INT' and p[4].type=='FLOAT':
                p[4.type='INT'
                p[0].value=int(p[4].value)
            elif p[2].value == 'INT' and p[4].type=='CHAR':
                p[4].type='INT'
                p[0].value=ord(p[4].value)
            elif p[2].value == 'CHAR' and p[4].type=='INT':
                if p[4].value>=0 and p[4].value<=255:
                    p[4].type='CHAR'
                    p[0].value=chr(p[4].value)
                else:
                    print "Error in line %s : Cannot typecasting INT outside the range 0-255 to CHAR",% p.lineno(1)
                    
            else:
                print "Error in line %s : Illegal Type conversion from %s to %s ",%(p.lineno(1),p[4]['type'],p[2]['value'])
            
        
    pass 

#pm-expression not included in grammer

#pm-expression:
    #cast-expression
    #pm-expression .* cast-expression
    #pm-expression ->* cast-expression
def p_pm_expression(p):
    ''' pm_expression : cast_expression 
                    | pm_expression DOT TIMES cast_expression
                    | pm_expression ARROW TIMES cast_expression '''                        ### Add .* and ->* to operators and change here 
    pass 

#multiplicative-expression:
    #pm-expression
    #multiplicative-expression * pm-expression
    #multiplicative-expression / pm-expression
    #multiplicative-expression % pm-expression

#not including pm-expression in the grammer


#TODO : add support for pointers in mutiplicative, additive,etc. expression
                  
def p_multiplicative_expression_1(p):
    ''' multiplicative_expression : cast_expression'''
    p[0]=copyAttribute(p[1])
    pass
def p_multiplicative_expression_2(p):
    ''' multiplicative_expression : multiplicative_expression TIMES cast_expression'''
    p[1]=copyAttribute(p[1])
    if p[1].type=='INT' and p[3].type=='INT':
        p[0].type='INT'
        p[1].value=p[1].value * p[3].value
    elif p[1].type in ['FLOAT','INT'] and p[1].type in ['FLOAT','INT']:
        p[0].type='FLOAT'
        p[1].value=p[1].value * p[3].value
    pass
def p_multiplicative_expression_3(p):
    ''' multiplicative_expression : multiplicative_expression DIV cast_expression '''
    p[1]=copyAttribute(p[1])
    if p[1].type=='INT' and p[3].type=='INT':
        p[0].type='INT'
        p[1].value=p[1].value / p[3].value
    elif p[1].type in ['FLOAT','INT'] and p[1].type in ['FLOAT','INT']:
        p[0].type='FLOAT'
        p[1].value=p[1].value / p[3].value
    
    pass                  
def p_multiplicative_expression_4(p)
    ''' multiplicative_expression : multiplicative_expression MODULO cast_expression '''
    p[1]=copyAttribute(p[1])
    if p[1].type=='INT' and p[3].type=='INT':
        p[0].type='INT'
        p[1].value=p[1].value % p[3].value
    elif p[1].type in ['FLOAT','INT'] and p[1].type in ['FLOAT','INT']:
        print 'Error in lino %s : Modulo operator can only be applied on integers',% p.lineno(2)
    pass 

#additive-expression:
    #multiplicative-expression
    #additive-expression + multiplicative-expression
    #additive-expression - multiplicative-expression
def p_additive_expression_1(p):
    ''' additive_expression : multiplicative_expression'''
    p[0]=copyAttribute(p[1])
    pass

def p_additive_expression_2(p):
    ''' additive_expression : additive_expression PLUS multiplicative_expression '''
    p[1]=copyAttribute(p[1])
    if p[1].type=='INT' and p[3].type=='INT':
        p[0].type='INT'
        p[1].value=p[1].value + p[3].value
    elif p[1].type in ['FLOAT','INT'] and p[1].type in ['FLOAT','INT']:
        p[0].type='FLOAT'
        p[1].value=p[1].value + p[3].value    
    pass
                  
def p_additive_expression_3(p):
    ''' additive_expression : additive_expression MINUS multiplicative_expression '''
    p[1]=copyAttribute(p[1])
    if p[1].type=='INT' and p[3].type=='INT':
        p[0].type='INT'
        p[1].value=p[1].value - p[3].value
    elif p[1].type in ['FLOAT','INT'] and p[1].type in ['FLOAT','INT']:
        p[0].type='FLOAT'
        p[1].value=p[1].value - p[3].value    
    pass
                  

#shift expressions not included in grammer
                  
#shift-expression:
    #additive-expression
    #shift-expression << additive-expression
    #shift-expression >> additive-expression
def p_shift_expression(p):
    ''' shift_expression : additive_expression 
                    | shift_expression LESS LESS additive_expression 
                    | shift_expression GREATER GREATER additive_expression '''                         #### ADD shift operators and change here 
    pass 

#relational-expression:
    #shift-expression
    #relational-expression
    #relational-expression
    #relational-expression
    #relational-expression
    #< shift-expression
    #> shift-expression
    #<= shift-expression
    #>= shift-expression

def p_relational_expression_1(p): 
    ''' relational_expression : additive_expression'''
    p[0]=copyAttribute(p[1])
    pass
def p_relational_expression_2(p):
    ''' relational_expression : relational_expression LESS additive_expression'''
    p[0]=copyAttribute(p[1])
    if check_compatibility_relational(p):
        p[0].type='BOOL'
        p[0].value=p[1].value<=p[3].value
    else:
        p[0]=initAttribute(p[0])  

def p_relational_expression_3(p):
    ''' relational_expression : relational_expression GREATER additive_expression '''
    p[0]=copyAttribute(p[1])
    if check_compatibility_relational(p):
        p[0].type='BOOL'
        p[0].value=p[1].value>p[3].value
    else:
        p[0]=initAttribute(p[0])
    
def p_relational_expression_4(p):
    ''' relational_expression : relational_expression LESS_EQ additive_expression '''
    p[0]=copyAttribute(p[1])
    if check_compatibility_relational(p):
        p[0].type='BOOL'
        p[0].value=p[1].value<=p[3].value
    else:
        p[0]=initAttribute(p[0]) 

def p_relational_expression_5(p):
    ''' relational_expression : relational_expression GREATER_EQ additive_expression '''
    p[0]=copyAttribute(p[1])    
    if check_compatibility_relational(p):
        p[0].type='BOOL'
        p[0].value=p[1].value>=p[3].value
    else:
        p[0]=initAttribute(p[0])

#equality-expression:
    #relational-expression
    #equality-expression == relational-expression
    #equality-expression != relational-expression
def p_equality_expression_1(p):
    ''' equality_expression : relational_expression '''
    p[0]=copyAttribute(p[1])
                  
def p_equality_expression_2(p):
    ''' equality_expression : equality_expression IS_EQ relational_expression '''
    p[0]=copyAttribute(p[1])
    if check_compatibility_relational(p):
        p[0].type='BOOL'
        p[0].value= (p[1].value==p[3].value)
    else:
        p[0]=initAttribute(p[0])
        
                  
def p_equality_expression_3(p):
    ''' equality_expression : equality_expression NOT_EQ relational_expression '''
    p[0]=copyAttribute(p[1])
    if check_compatibility_relational(p):
        p[0].type='BOOL'
        p[0].value= (p[1].value!=p[3].value)
    else:        
        p[0]=initAttribute(p[0])
                  
#and-expression:
    #equality-expression
    #and-expression & equality-expression
def p_and_expression(p):
    ''' and_expression : equality_expression
                        | and_expression AMPERSAND equality_expression '''
    pass

#exclusive-or-expression:
    #and-expression
    #exclusive-or-expression ^ and-expression
def p_exclusive_or_expression(p):
    ''' exclusive_or_expression : and_expression 
                    | exclusive_or_expression CARET and_expression '''
    pass 

#inclusive-or-expression:
    #exclusive-or-expression
    #inclusive-or-expression | exclusive-or-expression
def p_inclusive_or_expression(p):
    ''' inclusive_or_expression : exclusive_or_expression 
                    | inclusive_or_expression PIPE exclusive_or_expression '''
    pass 

#logical-and-expression:
    #inclusive-or-expression
    #logical-and-expression && inclusive-or-expression
def p_logical_and_expression_1(p):
    ''' logical_and_expression : equality_expression'''
    p[0]=copyAttribute(p[1])
                        
def p_logical_and_expression_1(p):
    ''' logical_and_expression : logical_and_expression DOUBLE_AMPERSAND equality_expression'''
    p[0]=copyAttribute(p[1])
    if p[1].type=='BOOL' and p[3].type=='BOOL':
        p[0].type='BOOL'
        p[0].value=p[1].value and p[3].value
    else:
        p[0]=initAttribute(p[0])
        print 'Error at line %s : && operator can only be applied to boolean operands',% p.lineno(2)

#logical-or-expression:
    #logical-and-expression
    #logical-or-expression || logical-and-expression
def p_logical_or_expression_1(p):
    ''' logical_or_expression : logical_and_expression '''
    p[0]=copyAttribute(p[1])

def p_logical_or_expression_2(p):
''' logical_or_expression : logical_or_expression DOUBLE_PIPE logical_and_expression ''' 
    p[0]=copyAttribute(p[1])
    if p[1].type=='BOOL' and p[3].type=='BOOL':
        p[0].type='BOOL'
        p[0].value=p[1].value or p[3].value
    else:
        p[0]=initAttribute(p[0])
        print 'Error at line %s : || operator can only be applied to boolean operands',% p.lineno(2)

#conditional-expression:
    #logical-or-expression
    #logical-or-expression ? expression : assignment-expression
def conditional_expression_1(p):
    ''' conditional_expression : logical_or_expression '''
    p[0]=copyAttribute(p[1])
            
def conditional_expression_1(p):
    ''' conditional_expression : logical_or_expression QUESTION expression COLON assignment_expression '''
    p[0]=copyAttribute(p[1])
    if p[1].type=='BOOL':
        if p[1].value==True:
            p[0]=copyAttribute(p[3])
        elif p[1].value=False:
            p[1]=copyAttribute(p[5])
    else:
        print 'Error at line %s : ? ternary operator can only be applied to boolean operands',% p.lineno(2)
        p[0]=initAttribute(p[0])

#assignment-expression:
    #conditional-expression
    #logical-or-expression assignment-operator assignment-expression
    #throw-expression
def p_assignment_expression(p):
    ''' assignment_expression : conditional_expression 
                    | logical_or_expression assignment_operator assignment_expression '''                  ## Error handling not included 
    pass 

#assignment-operator: one of
#= *= /= %= += -= >>= <<= &= ^= |=                                                         ## Add these to operators and add them here 
def p_assignment_operator(p):
    ''' assignment_operator : ASSIGN 
                    | EQ_TIMES
                    | EQ_DIV 
                    | EQ_MODULO
                    | EQ_PLUS
                    | EQ_MINUS '''
    pass 

#expression:
    #assignment-expression
    #expression , assignment-expression
def p_expression(p):
    ''' expression : assignment_expression 
                    | expression COMMA assignment_expression '''
    pass 

#constant-expression:
    #conditional-expression
def p_constant_expression(p):
    ''' constant_expression : conditional_expression ''' 
    pass 

def p_constant_expression_opt:
    ''' constant_expression_opt : 
                    | constant_expression '''
    pass 

####################################################

#################### STATEMENTS ####################

#statement:
    #labeled-statement
    #expression-statement
    #compound-statement
    #selection-statement
    #iteration-statement
    #jump-statement
    #declaration-statement
    #try-block
def p_statement(p):
    ''' statement : labeled_statement
                | expression_statement
                | compound_statement 
                | selection_statement
                | iteration_statement
                | jump_statement
                | declaration_statement '''
    pass 

#labeled-statement:
    #identifier : statement
    #case constant-expression : statement
    #default : statement
def p_labeled_statement(p):
    ''' labeled_statement : identifier COLON statement 
                | CASE constant_expression COLON statement 
                | DEFAULT COLON statement ''' 
    pass 

#expression-statement:
    #expressionopt ;
def p_expression_statement(p):
    ''' expression_statement : SEMICOLON 
                    | expression SEMICOLON '''
    pass 

#compound-statement:
    #{ statement-seqopt }
def p_compound_statement(p):
    ''' compound_statement : LBRACE statement_seq RBRACE 
                    | LBRACE RBRACE '''
    pass 

#statement-seq:
    #statement
    #statement-seq statement
def p_statement_seq(p):
    ''' statement_seq : statement 
                | LBRACE statement_seq RBRACE 
                | LBRACE RBRACE '''
    pass 

#selection-statement:
    #if ( condition ) statement
    #if ( condition ) statement else statement
    #switch ( condition ) statement
def p_selection_statement(p):
    ''' selection_statement : IF LPAREN condition RPAREN statement 
                    | IF LPAREN condition RPAREN statement ELSE statement 
                    | SWITCH LPAREN condition RPAREN statement '''
    pass 

#condition:
    #expression
    #type-specifier-seq declarator = assignment-expression
def p_condition(p):
    ''' condition : expression 
                | type_specifier_seq declarator ASSIGN assignment_expression '''
    pass 

#iteration-statement:
    #while ( condition ) statement
    #do statement while ( expression ) ;
    #for ( for-init-statement conditionopt ; expressionopt ) statement
def p_iteration_statement(p):
    ''' iteration_statement : WHILE LPAREN condition RPAREN statement 
                    | DO statement WHILE LPAREN condition RPAREN SEMICOLON 
                    | FOR LPAREN for_init_statement condition SEMICOLON expression RPAREN statement
                    | FOR LPAREN for_init_statement condition SEMICOLON RPAREN statement
                    | FOR LPAREN for_init_statement SEMICOLON expression RPAREN statement
                    | FOR LPAREN for_init_statement SEMICOLON RPAREN statement '''
    pass 

#for-init-statement:
    #expression-statement
    #simple-declaration
def p_for_init_statement(p):
    ''' for_init_statement : expression_statement 
                    | simple_declaration '''
    pass 

#jump-statement:
    #break ;
    #continue ;
    #return expressionopt ;
    #goto identifier ;
def p_jump_statement(p):
    ''' jump_statement : BREAK 
                    | CONTINUE 
                    | RETURN expression SEMICOLON 
                    | RETURN SEMICOLON '''
    pass 

#declaration-statement:
    #block-declaration
def p_declaration_statement(p):
    ''' declaration_statement : block_declaration '''
    pass

####################################################


#################### DECLARATIONS ##################
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
    ''' simple_type_specifier : double_colon_opt nested_name_specifier_opt type_name
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
    ''' elaborated_type_specifier : class_key double_colon_opt nested_name_specifier_opt identifier '''


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
                    | double_colon_opt nested_name_specifier_opt type_name '''

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

#class-name:
    #identifier
    #template-id
def p_class_name(p):
    ''' class_name : identifier '''
    p[0] = p[1]

#class-specifier:
    #class-head { member-specificationopt }
def p_class_specifier(p):
    ''' class_specifier : new_scope class_head LBRACE member_specification_opt RBRACE finish_scope'''
    global env 
    x.attrs["methods"]=p[4] 
    if not env.put(x):
        if DEBUG :
            print( str(p[2].value) ++ "already declared" )

#class-head:
    #class-key identifieropt base-clauseopt
    #class-key nested-name-specifier identifier base-clauseopt
    #class-key nested-name-specifier template template-id base-clauseopt
def p_class_head_1(p):
    ''' class_head : class_key identifier base_clause_opt '''
    global env 
    x = Symbol(p[2])
    x.type = p[1].type
    x.attrs["inherits"] = p[3]
    x.attrs["scope"] = env 
    p[0]=x 
    

def p_class_head_2(p):
    ''' class_head : class_key nested_name_specifier identifier base_clause_opt '''
    x = Symbol(p[3].value)
    x.type = p[1].type
    x.attrs["inherits"] = p[4]
    x.attrs["scope"] = find_scope(p[2]) 
    p[0]=x 


#class-key:
    #class
    #struct
    #union

def p_class_key(p):
    global env 
    ''' class_key : STRUCT '''
    p[0] = "STRUCT" 

def p_class_key(p):
    ''' class_key : CLASS ''' 
    p[0] = "CLASS"

def p_error(p):
    print("Whoa. We're hosed")

#member-specification:
    #member-declaration member-specificationopt
    #access-specifier : member-specificationopt
def p_member_specification_opt_1(p):
    '''member_specification_opt : member_declaration member_specification_opt ''' 
    pass 
def p_member_specification_opt_2(p):
    '''member_specification_opt : access_specifier COLON member_specification_opt '''
    pass 

#member-declaration:
    #decl-specifier-seqopt member-declarator-listopt ;
    #function-definition ;opt
    #::opt nested-name-specifier templateopt unqualified-id ;
    #using-declaration
    #template-declaration
def p_member_declaration(p):
    ''' member_declaration : decl_specifier_seq member_declarator_list_opt SEMICOLON 
                    | member_declarator_list_opt
                    | function_definition SEMICOLON
                    | function_definition 
                    | double_colon_opt nested_name_specifier unqualified_id SEMICOLON '''
    pass 

#member-declarator-list:
    #member-declarator
    #member-declarator-list , member-declarator

def p_member_declarator_list(p):
    ''' member_declarator_list : member_declarator 
                    | member_declarator_list , member_declarator '''
    pass 

def p_member_declarator_list_opt(p):
    ''' member_declarator_list_opt : 
                    | member_declarator_list'''
    pass 

#member-declarator:
    #declarator pure-specifieropt
    #declarator constant-initializeropt
    #identifieropt : constant-expression
def p_member_declarator(p):
    ''' member_declarator : declarator pure_specifier_opt 
                    | declarator constant_initializer_opt 
                    | identifier COLON constant_expression
                    | COLON constant_expression '''
    pass 

#pure-specifier:
    #= 0
def p_pure_specifier_opt(p):
    ''' pure_specifier_opt : 
                    | ASSIGN ZERO  '''                                            ### ZERO Not defined .. I want to match it to 0 which is not in the tokens 
    pass 

#constant-initializer:
    #= constant-expression
def p_consatnt_initializer_opt(p):
    ''' constant_initializer_opt : 
                    | ASSIGN constant_expression '''
    pass 

######## DERIVED CLASSES ##############

#base-clause:
    #: base-specifier-list
def p_base_clause_opt_1(p):
    ''' base_clause_opt : ''' 
    p[0] = []

def p_base_clause_opt_2(p):
    ''' base_clause_opt : COLON base_specifier_list '''
    p[0] = p[2]

#base-specifier-list:
    #base-specifier
    #base-specifier-list , base-specifier
def p_base_specifier_list_1(p):
    ''' base_specifier_list : base_specifier ''' 
    p[0] = [p[1]]
def p_base_specifier_list_2(p):
    ''' base_specifier_list : base_specifier_list COMMA base_specifier '''
    p[0] = p[1] + [p[3]]

#base-specifier:
    #::opt nested-name-specifieropt class-name
    #virtual access-specifieropt ::opt nested-name-specifieropt class-name
    #access-specifier virtualopt ::opt nested-name-specifieropt class-name
def p_base_specifier_1(p):
    ''' base_specifier : double_colon_opt nested_name_specifier_opt class_name ''' 
    env = p[2]
    p[0] = env.get(p[3])

def p_base_specifier_2(p):
    ''' base_specifier : access_specifier double_colon_opt nested_name_specifier_opt class_name ''' 
    env = p[3]
    p[0] = env.get(p[4])

#access-specifier:
    #private
    #protected
    #public
def p_access_specifier_1(p):
    ''' access_specifier : PUBLIC ''' 
    p[0] = "PUBLIC"
def p_access_specifier_2(p):
    ''' access_specifier : PRIVATE '''
    p[0] = "PRIVATE"
def p_access_specifier_3(p):
    ''' access_specifier : PROTECTED ''' 
    p[0] = "PROTECTED"


############# SPECIAL MEMBER FUNCTIONS ################

#conversion-function-id:
    #operator conversion-type-id
def p_conversion_function_id(p):
    ''' conversion_function_id : OPERATOR conversion_type_id '''
    pass 

#conversion-type-id:
    #type-specifier-seq conversion-declaratoropt
def p_conversion_type_id(p):
    ''' conversion_type_id : type_specifier_seq conversion_declarator_opt '''
    pass 

#conversion-declarator:
    #ptr-operator conversion-declaratoropt
def p_conversion_declarator_opt(p):
    ''' conversion_declarator_opt : 
                    | ptr_operator conversion_declarator_opt '''
    pass 

#ctor-initializer:
    #: mem-initializer-list
def p_ctor_initializer_opt(p):
    ''' ctor_initializer_opt : 
                    | mem_initializer_list'''
    pass 

#mem-initializer-list:
    #mem-initializer
    #mem-initializer , mem-initializer-list
def p_mem_initializer_list(p):
    ''' mem_initializer_list : mem_initializer
                    | mem_initializer , mem_initializer_list '''
    pass 

#mem-initializer:
    #mem-initializer-id ( expression-listopt )
def p_mem_initializer(p):
    ''' mem_initializer : mem_initializer_id LPAREN expression_list RPAREN 
                    | mem_initializer_id LPAREN RPAREN '''
    pass 

#mem-initializer-id:
    #::opt nested-name-specifieropt class-name
    #identifier
def p_mem_initializer_id(p):
    ''' mem_initializer_id : double_colon_opt nested_name_specifier_opt class_name 
                    | double_colon_opt class_name 
                    | identifier '''
    pass 


######### OVERLOADING ###########
#operator-function-id:
    #operator operator
def p_operator_function_id : 
    ''' operator_function_id : OPERATOR operator '''
    pass 

def p_operator(p):
    ''' operator : PLUS 
                | MINUS 
                | TIMES 
                | DIV 
                | MODULO 
                | CARET 
                | AMPERSAND 
                | PIPE 
                | TILDE 
                | EXCLAMATION 
                | ASSIGN 
                | LESS 
                | GREATER 
                | EQ_PLUS
                | EQ_MINUS 
                | EQ_TIMES
                | EQ_DIV 
                | EQ_MODULO                                             
                | ARROW 
                | IS_EQ 
                | NOT_EQ
                | LESS_EQ
                | GREATER_EQ
                | DOUBLE_AMPERSAND 
                | DOUBLE_PIPE
                | PLUS_PLUS 
                | MINUS_MINUS 
                | COMMA 
                | LPAREN RPAREN 
                | LBRACKET RBRACKET  '''
    pass

                  

########### TEMPLATES ################

######################################

########### EXCEPTION HANDLING #######

###################################### 

########### PREPROCESSING DIRECTIVES ###

########################################

