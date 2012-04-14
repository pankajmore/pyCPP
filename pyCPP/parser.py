from lexer import *
import ply.yacc as yacc
from symbol import *
from copy import deepcopy
num_temporaries=0
## TODO : return type of function should match the actual function type
## {{{
success = True
size=0
class Type(object):
    def __init__(self,next):
        self.next = next
        self.name = next
        self.dim = 1
    def __eq__(self,other):
        if isinstance(other,Type):
            if (isinstance(self.next,Type) == isinstance(other.next,Type)):
                return (self.next == other.next)
            else :
                return False 
        else :
            return NotImplemented 
    def __ne__(self,other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    def __repr__(self):
	if isinstance(self.next,Type):
        	return "*" + str(self.next)
	else:
		return str(self.next)
    def size(self):
        if isinstance(self.next,Type):
            return dim*self.next.size()
        else:
            return 4


Sizes={'FLOAT':4, 'INT':4, 'CHAR':1, 'BOOL':1}
env=Environment(None)
DeclType = None
class Attribute(object):
    def __init__(self):
        self.type = None
        self.attr={}    
        self.value=None    
        self.offset = 0
        self.code=''
        self.place=''
        self.error = False
    def __repr__(self):
        return "type:"+str(self.type)+" attr:" + str(self.attr)

def initAttr(a):
    a.type=None 
    a.attr={}
    a.value=None
    a.offset= 0
    a.code=''
    a.place=''
    return a

def errorAttr(a):
    a.type=Type('ERROR')
    a.attr={}
    a.value=None
    a.offset= 0
    a.code=''
    a.place=''
    return a

def newTemp():
      global num_temporaries
      temp = "_T"+str(num_temporaries)
      num_temporaries = num_temporaries + 1
      return temp

newLabel = newTemp

def toAddr(p):
    if p.attr.has_key('symbol') and p.attr['symbol'].back>0:
        return " -"+str(p.offset)+"($gp)"
    else:
        return " -"+str(p.offset)+"($fp)"


def find_scope(p):
    if p.attr.has_key('symbol') and p.attr['symbol'].back>0:
        return " $gp"
    else:
        return " $fp"

def find_recursively(p):
    if isinstance(p,Type):
        return find_recursively(p.next)
    else:
        return p

def find_type_recursively(p):
    if isinstance(p,Type):
        return '*' + find_type_recursively(p.next)
    else:
        return p
    
def find_type(p):
    if p.attr.has_key('symbol') and p.attr['symbol'].attr.has_key('isFunction'):
        return 'FUNCTION ' + p.attr['symbol'].name+' -> ' + find_type_recursively(p.type.next)
    else:
        return find_type_recursively(p.type.next)
        
def is_primitive(p):
    if not (p.attr.has_key('symbol') and p.attr['symbol'].attr.has_key('isFunction')):
        return True
    else:
        return False

def check_compatibility_relational(p):
    if p[1].type in [Type('FLOAT'),Type('INT'),Type('CHAR')] and p[3].type in [Type('FLOAT'),Type('INT'),Type('CHAR')] and is_primitive(p[1]) and is_primitive(p[3]):
        return True
    else:
        return False   

def check_compatibility_equality(p):
    if p[1].type in [Type('FLOAT'),Type('INT'),Type('CHAR'),Type('BOOL')] and p[3].type in [Type('FLOAT'),Type('INT'),Type('CHAR'),Type('BOOL')] and is_primitive(p[1]) and is_primitive(p[3]):
        return True
    else:
        return False 

def is_integer(p):
    try:
        a = int(p.place)
        return True
    except ValueError:
        return False

precedence =  [('nonassoc', 'LIT_STR', 'INUMBER', 'DNUMBER'), ('nonassoc', 'LIT_CHAR'), ('nonassoc', 'IFX'), ('nonassoc', 'ELSE'), ('nonassoc', 'DOUBLE', 'FLOAT', 'INT', 'STRUCT', 'VOID', 'ENUM', 'CHAR', 'UNION', 'SEMICOLON'), ('left','COMMA'), ('right', 'EQ_PLUS', 'EQ_MINUS', 'EQ_TIMES', 'EQ_DIV', 'EQ_MODULO', 'ASSIGN'), ('right', 'QUESTION', 'COLON'), ('left', 'DOUBLE_PIPE'), ('left', 'DOUBLE_AMPERSAND'), ('left', 'PIPE'), ('left', 'CARET'), ('left', 'AMPERSAND'), ('left', 'IS_EQ', 'NOT_EQ'), ('left', 'LESS', 'LESS_EQ', 'GREATER', 'GREATER_EQ'), ('left', 'PLUS', 'MINUS'), ('left', 'TIMES', 'DIV', 'MODULO'), ('right', 'EXCLAMATION', 'TILDE'), ('left', 'PLUS_PLUS', 'MINUS_MINUS', 'ARROW'), ('nonassoc', 'NOPAREN'), ('right', 'LPAREN', 'LBRACKET', 'LBRACE'), ('left', 'RPAREN', 'RBRACKET', 'RBRACE'),('left','SCOPE')]
## }}}

########### Start ################

## {{{
def p_translation_unit(p):
    ''' translation_unit : 
                         | declaration_seq'''
    ##p.set_lineno(0,p.lineno(1))
    ### TODO 

#def p_empty(p):
#    ''' empty : '''
#    pass
  

#declaration-seq:
    #declaration
    #declaration-seq declaration
    
def NewScope():
    global env 
    env = Environment(env)


def PopScope():
    global env  
    env = env.prev 

def functionScope():
    NewScope()
    
def unsetFunctionScope():
    PopScope()

def p_new_scope(p):
    '''new_scope : '''
    NewScope()
    global env
    env.table.startlabel = newLabel()
    env.table.endlabel = newLabel()

    p[0]  = Attribute()
    p[0].code = env.table.startlabel + ":\n"

def p_finish_scope(p):
    '''finish_scope : '''
    global env
    p[0] = Attribute()
    p[0].code = env.table.endlabel + ":\n"
    PopScope()



def p_function_scope(p):
    '''function_scope : '''
    functionScope()
    t = env.prev.get(p[-1].attr['name'])
    if t is not None: # function declartion already seen
#HACK : p[-2] might be buggy?
        t.table = env.table # For keeping a pointer to the function symboltable
        if p[-2] is not None:
            if p[-2].type is None: # it must be a typeless declaration , assume VOID
                if t.type != Type('VOID'):
                    print ("\nFunction's type must be void since its declaration had no type\n")
            else:
                if t.type != p[-2].type:
                    print ("\nFunction's type not consistent between declaration and definition\n")
        if t.attr['numParameters'] != p[-1].attr['numParameters'] :
            print ("\nFunction overloading not supported\n")
        for i in range(t.attr['numParameters']):
            if t.attr['parameterList'][i].type != p[-1].attr['parameterList'][i].type:
                print ("\nFunction overloading by different types not supported\n")
            if t.attr['parameterList'][i].attr['name'] == None:
                print ("\nVariable name for parameter missing\n")
            # refactor the duplicate code
            # storing the formal parameters in table not the parameters during function declaration
            s = Symbol(p[-1].attr['parameterList'][i].attr['name'])
            s.type = p[-1].attr['parameterList'][i].type
            if not env.put(s):
                print ("\nError : parameter is already in the symbol table\n")

#ENHANCEMENT
    else: # function declaration has not been seen
        for i in range(p[-1].attr['numParameters']):
            s = Symbol(p[-1].attr['parameterList'][i].attr['name'])
            s.type = p[-1].attr['parameterList'][i].type
            if not env.put(s):
                print ("\nError : parameter is already in the symbol table\n")
    global size
    global oldsize
    oldsize=size
    size=0
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].code+="\tsw $fp, -4($sp)\n"
    p[0].code+="\tsw $ra, 0($sp)\n"
    p[0].code+="\tli $t0 8\n"
    p[0].code+="\tsub $sp $sp $t0\n"
    p[0].code+="\tmove $fp $sp\n"

    for i in range(len(p[-1].attr['parameterList'])):
        p[0].code += "\tsw $a" + str(i) + ", -" +str(size) + "($fp)\n"
        p[-1].attr['parameterList'][i].offset = size
        size = size + 4


def p_unset_function_scope(p):
    '''unset_function_scope : '''
    unsetFunctionScope()
    global size
    global oldsize
    size=oldsize
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].code+="\taddi $sp Ssp"+str(size)+"\n"
    p[0].code+="\taddi $sp Ssp 8\n"
    p[0].code+="\tlw $fp -4($sp)\n"
    p[0].code+="\tlw $ra 0($sp)\n"

def p_declaration_seq_1(p):
    ''' declaration_seq : declaration '''
    p.set_lineno(0,p.lineno(1))
  
def p_declaration_seq_2(p):
    ''' declaration_seq : declaration_seq declaration  '''
    p.set_lineno(0,p.lineno(1))

## }}}
#################### EXPRESSIONS ###################
## {{{
def p_literal_1(p):
    '''literal : INUMBER '''
    p[0]=Attribute()
    p[0].type=Type('INT')
    p[0].place=str(p[1])
    p.set_lineno(0,p.lineno(1))
  
def p_literal_2(p):
    ''' literal : DNUMBER '''
    p[0]=Attribute()
    p[0].type=Type('FLOAT')
    p[0].place=str(p[1])
    p.set_lineno(0,p.lineno(1))

def p_literal_3(p):
    ''' literal : LIT_CHAR '''
    p[0]=Attribute()
    p[0].type=Type('CHAR')
    p[0].place=str(p[1])
    p.set_lineno(0,p.lineno(1))

def p_literal_4(p):
    ''' literal : LIT_STR '''
    p[0]=Attribute()
    p[0].type=Type(Type('CHAR'))
    p[0].place=str(p[1])
    p.set_lineno(0,p.lineno(1))

def p_literal_5(p):
    ''' literal : TRUE '''
    p[0]=Attribute()
    p[0].type=Type('BOOL')
    p[0].place=str(p[1])
    p.set_lineno(0,p.lineno(1))

def p_literal_6(p):
    ''' literal : FALSE'''
    p[0]=Attribute()
    p[0].type=Type('BOOL')
    p[0].place=str(p[1])
    p.set_lineno(0,p.lineno(1))
  
#primary-expression:
    #literal
    #this
    #:: identifier
    #:: operator-function-id
    #:: qualified-id
    #( expression )
    #id-expression
    
def p_primary_expression_1(p):
    ''' primary_expression : literal '''
    global size
    p[0]=deepcopy(p[1])
    p[0].place=newTemp()
    p[0].attr={}
    p[0].offset=size
    p[0].code+="\tli $t0 "+p[0].place+"\n"
    p[0].code+="\tsw $t0 "+toAddr(p[0])+"\n"
    size=size+4
    p.set_lineno(0,p.lineno(1))
  
##def p_primary_expression_2(p):
##    ''' primary_expression : SCOPE IDENTIFIER '''
##    pass
##  
##def p_primary_expression_3(p):
##    ''' primary_expression : SCOPE operator_function_id '''
##    pass
##  
##def p_primary_expression_4(p):
##    ''' primary_expression : SCOPE qualified_id '''
##    pass
    
 
def p_primary_expression_5(p):
    ''' primary_expression : LPAREN expression RPAREN '''
    p[0]=deepcopy(p[2])
    p.set_lineno(0,p.lineno(1))
  
def p_primary_expression_6(p):
    ''' primary_expression : id_expression  '''
    p[0]=deepcopy(p[1])
    global env
    p[0] = Attribute()
    t = env.get(p[1].attr['name'])
    if t==None:
        p[0].type = Type("ERROR")
	print "Error in line %s : Identifier %s not defined in this scope" %(p.lineno(1), p[1].attr['name'])
    else :
        p[0].attr['symbol'] = t
	p[0].type=t.type
	p[0].offset= t.offset
	#print "Identifier reduced : ", str(t.name),str(t.type)
    p.set_lineno(0,p.lineno(1))
    
#id-expression:
    #unqualified-id
    #qualified-id
def p_id_expression_1(p):
    ''' id_expression : unqualified_id '''
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))
  
##def p_id_expression_2(p):
##    ''' id_expression : qualified_id '''
##    pass 

#unqualified-id:
    #IDENTIFIER
    #operator-function-id
    #conversion-function-id
    #~ class-name
    #template-id
def p_unqualified_id_1(p):
    ''' unqualified_id : IDENTIFIER %prec RPAREN '''
    global env
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    #t = env.get(str(p[1]))
    #if t==None:
        #t = Symbol(str(p[1]))
        #if not env.put(t):
        #    print("Error : Identifier "+str(p[1])+"already defined. Line number #"+str(p.lineno(1)))
        #    p[0].type = Type("ERROR")
    #else :
        #p[0].type = t.type
    #p[0].attr["symbol"] = t
    p[0].attr["name"] = str(p[1])
    p[0].code = ''
    p.set_lineno(0,p.lineno(1))
    
def p_unqualified_id_2(p):
    ''' unqualified_id : operator_function_id '''
    p.set_lineno(0,p.lineno(1))
    
def p_unqualified_id_3(p):
    ''' unqualified_id : conversion_function_id '''
    p.set_lineno(0,p.lineno(1))
    
def p_unqualified_id_4(p):
    ''' unqualified_id : TILDE class_name '''
    p.set_lineno(0,p.lineno(1))

#### TODO : To add production rule for templateopt as well when template is introduced. ###
#qualified-id:
    #nested-name-specifier templateopt unqualified-id

##def p_qualified_id_1(p):
##    ''' qualified_id : nested_name_specifier unqualified_id '''
##    pass 

#nested-name-specifier:
    #class-or-namespace-name :: nested-name-specifieropt
    #class-or-namespace-name :: template nested-name-specifier

##def p_nested_name_specifier(p):
##    ''' nested_name_specifier : IDENTIFIER SCOPE nested_name_specifier_opt '''
##    ## IDENTIFIER is class_name here 
##    pass

  
##def p_nested_name_specifier_opt_1(p):
##    ''' nested_name_specifier_opt : '''
##    pass
##  
##def p_nested_name_specifier_opt_2(p):
##    ''' nested_name_specifier_opt : nested_name_specifier '''
##    pass 

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
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))
  
def p_postfix_expression_2(p):
    global size
    ''' postfix_expression : postfix_expression LBRACKET expression RBRACKET '''
    p[0] = deepcopy(p[1])
    if not (isinstance(p[0].type,Type) and isinstance(p[1].type.next,Type)):
        print "Error in line %s : Cannot access index of non-array " % p.lineno(2)
        p[0]=errorAttr(p[0])
    else:
        if p[0].type ==Type('ERROR') or p[0].type==Type('CLASS') or p[0].type==Type('STRUCT') or not is_primitive(p[0]):
            if p[0]!=Type('ERROR'):
                print "Error in line %s : Unidentified type of array " % p.lineno(2)
            p[0]=errorAttr(p[0])
        else:
            if not p[3].type==Type('INT'):
                print "Error in line %s : Index of array can only be an integer " % p.lineno(2)
                p[0]=errorAttr(p[0])
            else:
                dim=p[1].type.next.size()
                p[0].offset=size
                p[0].place=newTemp()          
                p[0].type=p[1].type.next
                p[0].attr={}
                p[0].code=p[1].code+p[3].code+"\tli $t0 "+p[1].offset+"\n"
                p[0].code+="\tlw $t1 "+toAddr(p[3])+"\n"
                p[0].code+="\tli $t2 "+dim+"\n"
                p[0].code+="\tmul $t1 $t1 $t2\n"
                p[0].code+="\tadd $t0 $t0 $t1\n"
                if isinstance(p[0].type.next,Type):
                    p[0].code+="\tsub $t1"+find_scope(p[1])+" $t0\n"
                    p[0].code+="\tlw $t1 0($t1)\n"
                    p[0].code+="\tsw $t1 "+toAddr(p[0])+"\n"
                else:
                    p[0].code+="\tsw $t0 "+toAddr(p[0])+"\n"                     
                size=size+4
                
    p.set_lineno(0,p.lineno(2))
  
def p_postfix_expression_3(p):
    ''' postfix_expression : postfix_expression LPAREN RPAREN '''
    global size
    global MaxFunctionLength
    global env
    p[0]=deepcopy(p[1])
    if not (p[1].attr.has_key('symbol') and p[1].attr['symbol'].attr.has_key('isFunction')):
        print "Error in line %s : Cannot use () on non-function %s " % (p.lineno(2),p[1].attr['symbol'].name)
        p[0]=errorAttr(p[0])
    elif p[0].type ==Type('CLASS') or p[0].type == Type('STRUCT') or p[0].type==Type('ERROR'):
        if p[0].type!=Type('ERROR'):
            print "Error in line %s : Unidentified type of function %s" % (p.lineno(2),p[1].attr['symbol'].name)
        p[0]=errorAttr(p[0])
    else:
        p[0].attr={}
        p[0].offset=size
        p[0].place=newTemp()
        size=size+4
        #t=env.get(p[0].attr['symbol'].name)
        #fsize=t.table.offset
        p[0].code+="\tjal "+p[1].place+"\n"
        if p[0].type!=Type('VOID'):
            p[0].code+='\tmove $t0 $v0\n'
        else:
            p[0].code+='\tli $t0 0'
        p[0].code+="\tsw $t0 " + toAddr(p[0])+"\n"
    p.set_lineno(0,p.lineno(2))
    
#def p_postfix_expression_4(p):
    #''' postfix_expression : simple_type_specifier LPAREN expression_list_opt RPAREN '''
    #pass
    #p.set_lineno(0,p.lineno(2))

def p_postfix_expression_4(p):
    ''' postfix_expression : postfix_expression LPAREN  expression_list RPAREN '''
    #Default arguments not supported as of now
    #Implicit type conversion not supported as of now
    p[0]=deepcopy(p[1])
    global size
    if not (p[1].attr.has_key('symbol') and p[1].attr['symbol'].attr.has_key('isFunction')):
        print "Error in line %s : Cannot use () on non-function %s " % (p.lineno(2),p[1].attr['symbol'].name)
        p[0]=errorAttr(p[0])
    elif p[0].type ==Type('CLASS') or p[0].type == Type('STRUCT') or p[0].type==Type('ERROR'):
        if p[0].type!=Type('ERROR'):
            print "Error in line %s : Unidentified type of function %s" % (p.lineno(2),p[1].attr['symbol'].name)
        p[0]=errorAttr(p[0])
    else:
        if p[1].attr['symbol'].attr['numParameters']!=p[3].attr['numParameters']:
            print "Error in line %s : Function %s requires %s arguments, given %s arguments " %( p.lineno(2), p[1].attr['symbol'].name,p[1].attr['symbol'].attr['numParameters'],p[3].attr['numParameters'])
            p[0]=errorAttr(p[0])
        else:
            tmp=0
            if p[1].attr['symbol'].attr['numParameters']>4:
                print "Error in line %s : Max 4 parameters are allowed\n" % p.lineno(2)
                tmp=1
            else:
                for i in range(p[1].attr['symbol'].attr['numParameters']):
                    if p[1].attr['symbol'].attr['parameterList'][i].type!=p[3].attr['parameterList'][i].type:
                        print "Error in line %s : Parameter %s of Function %s must be %s , given %s " %( p.lineno(2), str(i+1), p[1].attr['symbol'].name, find_type(p[1].attr['symbol'].attr['parameterList'][i]), find_type(p[3].attr['parameterList'][i]))
                        tmp=1
                    if tmp==1:
                        p[0]=errorAttr(p[0]) 
            if tmp==0:
                p[0].attr={}
                p[0].code=p[1].code
                p[0].place=newTemp()
                p[0].offset=size
                size=size+4
                for i in range(p[1].attr['symbol'].attr['numParameters']):
                    p[0].code+='\tlw $a'+str(i)+toAddr(p[1].attr['symbol'].attr['parameterList'][i])+'\n'
                p[0].code+="\tjal "+p[1].place+"\n"
                if p[0].type!=Type('VOID'):
                    p[0].code+='\tmove $t0 $v0\n'
                else:
                    p[0].code+='\tli $t0 0'
                p[0].code+="\tsw $t0 " + toAddr(p[0])+"\n"                
    p.set_lineno(0,p.lineno(2))

def p_postfix_expression_5(p):
    ''' postfix_expression : postfix_expression PLUS_PLUS '''
    global size
    p[0]=deepcopy(p[1])
    if is_primitive(p[1]) and (p[0].type==Type('FLOAT') or p[0].type==Type('INT')) :
        p[0].place=newTemp()
        p[0].offset=size
        size=size+4
        p[0].code=p[1].code
        p[0].code+="\tlw $t0 "+toAddr(p[1])+"\n"
        p[0].code+="\tsw $t0 "+toAddr(p[0])+"\n"
        p[0].code+="\taddi $t0 $t0 1\n"
        p[0].code+="\tsw $t0 "+toAddr(p[1])+"\n"
    elif is_primitive(p[1]) and isinstance(p[1].type,Type)and isinstance(p[1].type.next,Type):
        p[0].place=newTemp()
        p[0].attr={}
        p[0].offset=size
        size=size+4
        dim=p[0].type.next.size()
        p[0].code=p[1].code
        p[0].code+="\tlw $t0 "+toAddr(p[1])+"\n"
        p[0].code+="\tsw $t0 "+toAddr(p[0])+"\n"
        p[0].code+="\tli $t1 "+dim+"\n"
        p[0].code+="\tadd $t0 $t0 $t1\n"
        p[0].code+="\tsw $t0 "+toAddr(p[1])+"\n"     
    else:
        if p[1].type!=Type('ERROR'):                                                                                                     
            print 'Error in line %s : PostIncrement ++ operator can not be applied to %s' % (p.lineno(2),find_type(p[1]))
        p[0]=errorAttr(p[0])
    p.set_lineno(0,p.lineno(2))

def p_postfix_expression_6(p):
    ''' postfix_expression : postfix_expression MINUS_MINUS '''
    p[0]=deepcopy(p[1])
    global size
    if is_primitive(p[1]) and (p[0].type==Type('FLOAT') or p[0].type==Type('INT')):
        p[0].place=newTemp()
        p[0].offset=size
        size=size+4
        p[0].code=p[1].code
        p[0].code+="\tlw $t0 "+toAddr(p[1])+"\n"
        p[0].code+="\tsw $t0 "+toAddr(p[0])+"\n"
        p[0].code+="\tli $t1 1\n"
        p[0].code+="\tsub $t0 $t0 $t1\n"
        p[0].code+="\tsw $t0 "+toAddr(p[1])+"\n"
    elif is_primitive(p[1]) and isinstance(p[1].type,Type)and isinstance(p[1].type.next,Type):
        p[0].place=newTemp()
        p[0].offset=size
        size=size+4
        p[0].attr={}
        dim=p[0].type.next.size()
        p[0].code=p[1].code
        p[0].code+="\tlw $t0 "+toAddr(p[1])+"\n"
        p[0].code+="\tsw $t0 "+toAddr(p[0])+"\n"
        p[0].code+="\tli $t1 "+dim+"\n"
        p[0].code+="\tsub $t0 $t0 $t1\n"
        p[0].code+="\tsw $t0 "+toAddr(p[1])+"\n"                                                                                           
    else:
        if p[1].type!=Type('ERROR'):                                                                                                     
            print 'Error in line %s : PostDecrement -- operator can not be applied to %s' % (p.lineno(2),find_type(p[1]))
        p[0]=errorAttr(p[0])
    p.set_lineno(0,p.lineno(2))

def p_postfix_expression_7(p):
    ''' postfix_expression : postfix_expression DOT id_expression %prec IFX'''
    #p[0].offset=p[1].offset+p[3].offset
    p.set_lineno(0,p.lineno(2))
    
##def p_postfix_expression_5(p):
##    ''' postfix_expression : TYPENAME SCOPE nested_name_specifier IDENTIFIER LPAREN expression_list_opt RPAREN 
##                    | TYPENAME nested_name_specifier IDENTIFIER LPAREN expression_list_opt RPAREN 
##                    | postfix_expression PLUS_PLUS 
##                    | postfix_expression MINUS_MINUS '''
##    pass 

#expression-list:
    #assignment-expression
    #expression-list , assignment-expression
def p_expression_list_1(p):
    ''' expression_list : assignment_expression'''
    if p[1].type==Type('ERROR'):
        p[0]=errorAttr(p[0])
    else:
        p[0]=deepcopy(p[1])
        p[0].attr['parameterList']=[deepcopy(p[1])]
        p[0].attr['numParameters']=1
        p[0].type=Type('VOID')
    p.set_lineno(0,p.lineno(1))

def p_expression_list_2(p):
    ''' expression_list : expression_list COMMA assignment_expression '''
    if p[1].type==Type('ERROR') or p[3].type==Type('ERROR'):
        p[0]=errorAttr(p[0])
    else:
        p[0]=deepcopy(p[1])
        p[0].code+=p[3].code
        p[0].attr['numParameters']+=1
        p[0].attr['parameterList'].append(deepcopy(p[3]))
        p[0].code=p[1].code+'\t'+  p[3].code
    p.set_lineno(0,p.lineno(2))    

def p_expression_list_opt_1(p):
    ''' expression_list_opt : '''
    p[0]=None

def p_expression_list_opt_2(p):
    ''' expression_list_opt : expression_list '''
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))

#pseudo-destructor-name:
    #::opt nested-name-specifieropt type-name :: ~ type-name
    #::opt nested-name-specifier template template-id :: ~ type-name
    #::opt nested-name-specifieropt ~ type-name

##def p_pseudo_destructor_name(p):
##    ''' pseudo_destructor_name : SCOPE nested_name_specifier_opt type_name SCOPE TILDE type_name
##                    | nested_name_specifier_opt type_name SCOPE TILDE type_name
##                    | SCOPE nested_name_specifier_opt TILDE type_name 
##                    | nested_name_specifier_opt TILDE type_name '''
##    pass 

#unary-expression:
    #postfix-expression
    #++ cast-expression
    #-- cast-expression
    #unary-operator cast-expression
    #sizeof unary-expression
    #sizeof ( type-id )
    #new-expression
    #delete-expression
def p_unary_expression_1(p):
    ''' unary_expression : postfix_expression '''
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))
    
def p_unary_expression_2(p):
    ''' unary_expression : PLUS_PLUS cast_expression'''
    p[0]=deepcopy(p[2])
    global size
    if is_primitive(p[2]) and (p[2].type==Type('FLOAT') or p[2].type==Type('INT')):
        p[0].place=newTemp()
        p[0].attr={}
        p[0].offset=size
        size=size+4
        p[0].code=p[1].code
        p[0].code+="\tlw $t0 "+toAddr(p[1])+"\n"
        p[0].code+="\taddi $t0 $t0 1\n"
        p[0].code+="\tsw $t0 "+toAddr(p[0])+"\n"
        p[0].code+="\tsw $t0 "+toAddr(p[1])+"\n"
        
    elif is_primitive(p[2]) and isinstance(p[2].type,Type)and isinstance(p[2].type.next,Type):
        p[0].place=newTemp()
        p[0].attr={}
        p[0].offset=size
        size=size+4
        dim=p[0].type.next.size()
        p[0].code=p[1].code
        p[0].code+="\tlw $t0 "+toAddr(p[1])+"\n"
        p[0].code+="\tli $t1 "+dim+"\n"
        p[0].code+="\tadd $t0 $t0 $t1\n"
        p[0].code+="\tsw $t0 "+toAddr(p[0])+"\n"
        p[0].code+="\tsw $t0 "+toAddr(p[1])+"\n"  
    else:
        if p[2].type!=Type('ERROR'):
            print 'Error in line %s : PreIncrement ++ operator can not be applied to %s' % (p.lineno(2),find_type(p[1]))
        p[0]=errorAttr(p[0])
    pass
    p.set_lineno(0,p.lineno(1))
    

def p_unary_expression_3(p):
    ''' unary_expression : MINUS_MINUS cast_expression '''
    p[0]=deepcopy(p[2])
    global size
    if is_primitive(p[2]) and (p[2].type==Type('FLOAT') or p[2].type==Type('INT')):
        p[0].place=newTemp()
        p[0].attr={}
        p[0].offset=size
        size=size+4
        p[0].code=p[1].code
        p[0].code+="\tlw $t0 "+toAddr(p[1])+"\n"
        p[0].code+="\tli $t1 1\n"
        p[0].code+="\tsub $t0 $t0 $t1\n"
        p[0].code+="\tsw $t0 "+toAddr(p[0])+"\n"
        p[0].code+="\tsw $t0 "+toAddr(p[1])+"\n"     
    elif is_primitive(p[2]) and isinstance(p[2].type,Type)and isinstance(p[2].type.next,Type):
        p[0].place=newTemp()
        p[0].attr={}
        p[0].offset=size
        size=size+4
        dim=p[0].type.next.size()
        p[0].code=p[1].code
        p[0].code+="\tlw $t0 "+toAddr(p[1])+"\n"
        p[0].code+="\tli $t1 "+dim+"\n"
        p[0].code+="\tsub $t0 $t0 $t1\n"
        p[0].code+="\tsw $t0 "+toAddr(p[0])+"\n"
        p[0].code+="\tsw $t0 "+toAddr(p[1])+"\n"  
    else:
        if p[2].type!=Type('ERROR'):
            print 'Error in line %s : PreIncrement -- operator can not be applied to %s' % (p.lineno(2),find_type(p[1]))
        p[0]=errorAttr(p[0])
    pass
    p.set_lineno(0,p.lineno(1))

def p_unary_expression_4(p):
    ''' unary_expression : unary_operator cast_expression '''
    p[0]=deepcopy(p[2])
    global size
    if p[1]=='+':
        if is_primitive(p[2]) and (p[2].type==Type('FLOAT') or p[2].type==Type('INT') ):
            p[0].offset=size
            size=size+4
            p[0].place=newTemp()
            p[0].attr={}
            p[0].code=p[2].code
            p[0].code+="\tli $t0"+toAddr(p[2])+"\n"
            p[0].code+="\tsw $t0"+toAddr(p[0])+"\n"
        else:
            p[0]=errorAttr(p[0])
            if p[2].type!=Type('ERROR'):
                print 'Error in line %s : Unary + operator can not be applied to %s' % (p.lineno(1),find_type(p[2]))

    if p[1]=='-':
        if is_primitive(p[2]) and (p[2].type==Type('FLOAT') or p[2].type==Type('INT')):
            p[0].offset=size
            size=size+4
            p[0].place=newTemp()
            p[0].attr={}
            p[0].code=p[2].code
            p[0].code+="\tlw $t0"+toAddr(p[2])+"\n"
            p[0].code+="\tsub $t0 $0 $t0\n"
            p[0].code+="\tsw $t0"+toAddr(p[0])+"\n"
        else:
            p[0]=errorAttr(p[0])
            if p[2].type!=Type('ERROR'):        
                print 'Error in line %s : Unary - operator can not be applied to %s' % (p.lineno(1),find_type(p[2]))

    if p[1]=='!':
        if p[2].type==Type('BOOL') and is_primitive(p[2]):
            p[0].offset=size
            size=size+4
            p[0].place=newTemp()
            p[0].attr={}
            p[0].code=p[2].code
            p[0].code+="\tlw $t0"+toAddr(p[2])+"\n"
            p[0].code+="\tli $t1 1\n"
            p[0].code+="\tsub $t0 $t1 $t0\n"
            p[0].code+="\tsw $t0"+toAddr(p[0])+"\n"
        else:
            p[0]=errorAttr(p[0])
            if p[2].type!=Type('ERROR'):
                print 'Error in line %s : Unary ! operator can not be applied to %s' % (p.lineno(1),find_type(p[2]))
    if p[1]=='*':
        if isinstance(p[2].type,Type) and isinstance(p[2].type.next,Type):
            p[0].type=p[2].type.next
            p[0].offset=size
            size=size+4
            p[0].place=newTemp()
            p[0].attr={}
            p[0].code=p[2].code
            p[0].code+="\tlw $t0"+toAddr(p[2])+"\n"
            p[0].code+="\tsub $t1"+find_scope(p[2])+" $t0\n"
            p[0].code+="\tlw $t0 0($t1)\n"
            p[0].code+="\tsw $t0"+toAddr(p[0])+"\n"
            
        else:
            p[0]=errorAttr(p[0])
            if p[2].type!=Type('ERROR'):
                print 'Error in line %s : Unary * operator can not be applied to %s' % (p.lineno(1),find_type(p[2]))
    if p[1]=='&':
        if p[2].type in [Type('FLOAT'),Type('INT'),Type('BOOL'),Type('CHAR')] and is_primitive(p[2]):
            p[0].type=Type(p[2].type)
            p[0].offset=size
            size=size+4
            p[0].place=newTemp()
            p[0].attr={}
            p[0].code=p[2].code
            p[0].code+="\tli $t0"+p[2].offset+"\n"
            p[0].code+="\tsw $t0"+toAddr(p[0])+"\n"
        else:
            p[0]=errorAttr(p[0])
            if p[2].type!=Type('ERROR'):
                print 'Error in line %s : Unary & operator can not be applied to %s' % (p.lineno(1),find_type(p[2]))
    if p[1]=='~':
        pass #except destructor is there any other use of TILDA ~ ? If not we should discard ~ as a valid token.
    p.set_lineno(0,p.lineno(1))
        
#Will need to rewrite SIZEOF functions
  
def p_unary_expression_5(p):
    ''' unary_expression : SIZEOF unary_expression '''
    p[0]=Attribute()
    typ=find_recursively(p[2].type)    
    if is_primitive(p[2]) and typ in ['INT','FLOAT','CHAR','BOOL']:
        p[0].type='INT'
        p[0].place=newTemp()
        p[0].attr={}
        p[0].offset=size
        size+=4
        p[0].code=p[1].code
        p[0].code+="\tli $t0"+p[1].type.size()+"\n"
        p[0].code+="\tsw $t0"+toAddr(p[0])+"\n"
    else:
        p[0]=errorAttr(p[0])
        if p[2].type == Type('ERROR'):
            print "Error in line %s : SIZEOF cannot be applied to %s" %(p.lineno(1), find_type(p[2]))
    p.set_lineno(0,p.lineno(1))

def p_unary_expression_6(p):
    ''' unary_expression : SIZEOF LPAREN type_id RPAREN '''
    p[0]=Attribute()
    global size
    typ=find_recursively(p[3].type)    
    if is_primitive(p[3]) and typ in ['INT','FLOAT','CHAR','BOOL']:
        p[0].type='INT'
        p[0].place=newTemp()
        p[0].attr={}
        p[0].offset=size
        size+=4
        p[0].code=p[3].code
        p[0].code+="\tli $t0"+p[3].type.size()+"\n"
        p[0].code+="\tsw $t0"+toAddr(p[0])+"\n"
    else:
        p[0]=errorAttr(p[0])
        if p[3].type == Type('ERROR'):
            print "Error in line %s : SIZEOF cannot be applied to %s" %(p.lineno(1), find_type(p[3]))
    p.set_lineno(0,p.lineno(1))

#Will see whether to include the below  two productions in the grammer or not
def p_unary_expression_7(p):
    ''' unary_expression : new_expression'''
    p.set_lineno(0,p.lineno(1))

def p_unary_expression_8(p):
    ''' unary_expression : delete_expression'''
    p.set_lineno(0,p.lineno(1))


#unary-operator: one of
#* & + - ! ~
def p_unary_operator_1(p):
    ''' unary_operator : TIMES
    '''
    p[0] = '*'

def p_unary_operator_2(p):
    '''unary_operator : AMPERSAND
    '''
    p[0] = '&'

def p_unary_operator_3(p):
    '''unary_operator : PLUS
    '''
    p[0] = '+'
    p.set_lineno(0,p.lineno(1))

def p_unary_operator_4(p):
    '''unary_operator : MINUS 
    '''
    p[0] = '-'
    p.set_lineno(0,p.lineno(1))

def p_unary_operator_5(p):
    '''unary_expression : EXCLAMATION 
    '''
    p[0] = '!'
    p.set_lineno(0,p.lineno(1))

def p_unary_operator_6(p):
    '''unary_expression : TILDE
    '''
    p[0] = '~'
    p.set_lineno(0,p.lineno(1))


#new-expression:
    #::opt new new-placementopt new-type-id new-initializeropt
    #::opt new new-placementopt ( type-id ) new-initializeropt

def p_new_expression(p):
    ''' new_expression : NEW new_placement_opt new_type_id new_initializer_opt 
                    | NEW new_placement_opt LPAREN type_id RPAREN new_initializer_opt '''
    p.set_lineno(0,p.lineno(1))

##def p_new_expression(p):
##    ''' new_expression : SCOPE NEW new_placement_opt new_type_id new_initializer_opt 
##                    | NEW new_placement_opt new_type_id new_initializer_opt 
##                    | SCOPE NEW new_placement_opt LPAREN type_id RPAREN new_initializer_opt
##                    | NEW new_placement_opt LPAREN type_id RPAREN new_initializer_opt '''
##    pass 


#new-placement:
    #( expression-list )
def p_new_placement(p): 
    ''' new_placement : LPAREN expression_list RPAREN '''
    p.set_lineno(0,p.lineno(1))
    
def p_new_placement_opt(p):
    ''' new_placement_opt : %prec NOPAREN
                    | new_placement '''
    p.set_lineno(0,p.lineno(1))

#new-type-id:
    #type-specifier-seq new-declaratoropt
def p_new_type_id(p):
    ''' new_type_id : type_specifier_seq new_declarator_opt '''
    p.set_lineno(0,p.lineno(1)) 

#new-declarator:
    #ptr-operator new-declaratoropt
    #direct-new-declarator
def p_new_declarator_opt(p):
    ''' new_declarator_opt : %prec IFX
                    | ptr_operator new_declarator_opt 
                    | direct_new_declarator '''
    p.set_lineno(0,p.lineno(1))

#direct-new-declarator:
    #[ expression ]
    #direct-new-declarator [ constant-expression ]
def p_direct_new_declarator(p):
    ''' direct_new_declarator : LBRACKET expression RBRACKET 
                    | direct_new_declarator LBRACKET constant_expression RBRACKET '''
    p.set_lineno(0,p.lineno(1))

#new-initializer:
    #( expression-listopt )
def p_new_initializer_opt(p): 
    ''' new_initializer_opt : 
                    | LPAREN expression_list_opt RPAREN '''
    p.set_lineno(0,p.lineno(1))

#delete-expression:
    #::opt delete cast-expression
    #::opt delete [ ] cast-expression
def p_delete_expression(p):
    ''' delete_expression : DELETE cast_expression 
                    | DELETE LBRACKET RBRACKET cast_expression '''
    p.set_lineno(0,p.lineno(1))

##def p_delete_expression(p):
##    ''' delete_expression : SCOPE DELETE cast_expression 
##                    | DELETE cast_expression 
##                    | SCOPE DELETE LBRACKET RBRACKET cast_expression
##                    | DELETE LBRACKET RBRACKET cast_expression '''
##    pass 

#cast-expression:
    #unary-expression
    #( type-id ) cast-expression
def p_cast_expression_1(p):
    ''' cast_expression : unary_expression'''
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))

def p_cast_expression_2(p):
    '''cast_expression : LPAREN type_id RPAREN cast_expression '''
    p[0]=deepcopy(p[4])
    x=-1
    global size
    #TODO : Add support for type conversion with pointers i.e (int*), (char*), etc.
    if p[4].type!=p[2].type:
        if p[2].type== Type('FLOAT') and p[4].type==Type('INT') and is_primitive(p[4])and is_primitive(p[0]) :
            p[0].type=Type('FLOAT')
            p[0].offset=size
            size+=4
            p[0].place=newTemp()
            p[0].attr={}
            p[0].code=p[2].code+p[4].code
            p[0].code+="\tlw $t0"+toAddr(p[4])+"\n"
            p[0].code+="\tsw $t0"+toAddr(p[0])+"\n"
        elif p[2].type == Type('INT') and p[4].type==Type('FLOAT') and is_primitive(p[4])and is_primitive(p[0]):
            p[0].type=Type('INT')
            p[0].offset=size
            size+=4
            p[0].place=newTemp()
            p[0].attr={}
            p[0].code=p[2].code+p[4].code
            p[0].code+="\tlw $t0"+toAddr(p[4])+"\n"
            p[0].code+="\tsw $t0"+toAddr(p[0])+"\n"
        elif p[2].type == Type('INT') and p[4].type==Type('CHAR') and is_primitive(p[4])and is_primitive(p[0]):
            p[0].type=Type('INT')
            p[0].offset=size
            size+=4
            p[0].place=newTemp()
            p[0].attr={}
            p[0].code=p[2].code+p[4].code
            p[0].code+="\tlw $t0"+toAddr(p[4])+"\n"
            p[0].code+="\tsw $t0"+toAddr(p[0])+"\n"
        elif p[2].type == Type('CHAR') and (p[4].type==Type('INT') or p[4].type=='FLOAT')and is_primitive(p[4])and is_primitive(p[0]):
            p[0].type=Type('CHAR')
            p[0].offset=size
            size+=4
            p[0].place=newTemp()
            p[0].attr={}
            p[0].code=p[2].code+p[4].code
            p[0].code+="\tlw $t0"+toAddr(p[4])+"\n"
            p[0].code+="\tandi $t0 $t0 256\n"
            p[0].code+="\tsw $t0"+toAddr(p[0])+"\n"
        elif isinstance(p[2].type,Type) and isinstance(p[4].type,Type):
            if p[2].type.next==Type('VOID') or  p[4].type.next==Type('VOID'):
                x=1
            if x<0:
                print "Error in line %s : Illegal Type conversion from %s to %s " %(p.lineno(1),find_type(p[4]),find_type([2]))
            else:
                p[0].type=p[2].type
                p[0].offset=size
                size+=4
                p[0].place=newTemp()
                p[0].attr={}
                p[0].code=p[2].code+p[4].code
                p[0].code+="\tlw $t0"+toAddr(p[4])+"\n"
                p[0].code+="\tsw $t0"+toAddr(p[0])+"\n"
        else:
            p[0]=errorAttr(p[0])
            if p[2].type!=Type('ERROR') and p[4].type!=Type('ERROR'):
                print "Error in line %s : Illegal Type conversion from %s to %s " %(p.lineno(1),find_type(p[4]),find_type([2]))
    p.set_lineno(0,p.lineno(1))

#multiplicative-expression:
    #pm-expression
    #multiplicative-expression * pm-expression
    #multiplicative-expression / pm-expression
    #multiplicative-expression % pm-expression
                  
def p_multiplicative_expression_1(p):
    ''' multiplicative_expression : cast_expression'''
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))
    
def p_multiplicative_expression_2(p):
    ''' multiplicative_expression : multiplicative_expression TIMES cast_expression'''
    p[0]=deepcopy(p[1])
    if p[1].type==Type('CHAR') and p[3].type==Type('CHAR')and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('CHAR')
    if p[1].type in [Type('INT'),Type('CHAR')] and p[3].type in [Type('INT'),Type('CHAR')]and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('INT')
        p[0].code = p[1].code +'\t' + p[3].code + '\t'+ p[0].place + '=' + p[1].place + '*' + p[3].place + '\n'        
    elif p[1].type in [Type('FLOAT'),Type('INT'),Type('CHAR')] and p[3].type in [Type('FLOAT'),Type('INT'),Type('CHAR')] and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('FLOAT')
        p[0].code = p[1].code +'\t' + p[3].code + '\t'+ p[0].place + '=' + p[1].place + '*' + p[3].place + '\n'
    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print "Error in line %s : Cannot perform multiplication between %s and %s " %(p.lineno(2),find_type(p[1]),find_type(p[3]))
    if p[0].type != Type('ERROR'):
        p[0].offset = size 
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}
        p[0].code = p[1].code + p[3].code
        p[0].code += "\tlw $t0 " + toAddr(p[1]) + "\n"
        p[0].code += "\tlw $t1 " + toAddr(p[3]) + "\n"
        p[0].code += "\tmul $t2, $t0, $t1\n"
        p[0].code += "\tsw $t2 " + toAddr(p[0]) + "\n"   
    p.set_lineno(0,p.lineno(2))

def p_multiplicative_expression_3(p):
    ''' multiplicative_expression : multiplicative_expression DIV cast_expression '''
    p[0]=deepcopy(p[1])
    if p[1].type==Type('CHAR') and p[3].type==Type('CHAR')and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('CHAR')
    if p[1].type in [Type('INT'),Type('CHAR')] and p[3].type in [Type('INT'),Type('CHAR')]and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('INT')
        p[0].code = p[1].code +'\t' + p[3].code + '\t'+ p[0].place + '=' + p[1].place + '/' + p[3].place + '\n'        
    elif p[1].type in [Type('FLOAT'),Type('INT'),Type('CHAR')] and p[3].type in [Type('FLOAT'),Type('INT'),Type('CHAR')] and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('FLOAT')
        p[0].code = p[1].code +'\t' + p[3].code + '\t'+ p[0].place + '=' + p[1].place + '/' + p[3].place + '\n'
    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print "Error in line %s : Cannot perform division between %s and %s " %(p.lineno(2),find_type(p[1]),find_type(p[3]))
    if p[0].type != Type('ERROR'):
        p[0].offset = size 
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}
        p[0].code = p[1].code + p[3].code
        p[0].code += "\tlw $t0 " + toAddr(p[1]) + "\n"
        p[0].code += "\tlw $t1 " + toAddr(p[3]) + "\n"
        p[0].code += "\tdiv $t0, $t1\n"
        p[0].code += "\tmove $t2 $LO\n"
        p[0].code += "\tsw $t2 " + toAddr(p[0]) + "\n"            
    p.set_lineno(0,p.lineno(2))

def p_multiplicative_expression_4(p):
    ''' multiplicative_expression : multiplicative_expression MODULO cast_expression '''
    p[0]=deepcopy(p[1])
    if p[1].type==Type('CHAR') and p[3].type==Type('CHAR')and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('CHAR')
    if p[1].type in [Type('INT'),Type('CHAR')] and p[3].type in [Type('INT'),Type('CHAR')]and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('INT')
        p[0].code = p[1].code +'\t' + p[3].code + '\t'+ p[0].place + '=' + p[1].place + '%' + p[3].place + '\n' 
    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print "Error in line %s : Modulo operator cannot be applied between %s and %s " %(p.lineno(2),find_type(p[1]),find_type(p[3]))
    if p[0].type != Type('ERROR'):
        p[0].offset = size 
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}
        p[0].code = p[1].code + p[3].code
        p[0].code += "\tlw $t0 " + toAddr(p[1]) + "\n"
        p[0].code += "\tlw $t1 " + toAddr(p[3]) + "\n"
        p[0].code += "\tdiv $t0, $t1\n"
        p[0].code += "\tmove $t2 $HI\n"
        p[0].code += "\tsw $t2 " + toAddr(p[0]) + "\n"
    p.set_lineno(0,p.lineno(2))

#additive-expression:
    #multiplicative-expression
    #additive-expression + multiplicative-expression
    #additive-expression - multiplicative-expression

def p_additive_expression_1(p):
    ''' additive_expression : multiplicative_expression'''
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))

def p_additive_expression_2(p):
    ''' additive_expression : additive_expression PLUS multiplicative_expression '''
    global size
    x=-1
    p[0]=deepcopy(p[1])
    if p[1].type==Type('CHAR') and p[3].type==Type('CHAR')and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('CHAR')
    elif p[1].type in [Type('INT'),Type('CHAR')] and p[3].type in [Type('INT'),Type('CHAR')]and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('INT')
    elif p[1].type in [Type('FLOAT'),Type('INT'),Type('CHAR')] and p[3].type in [Type('FLOAT'),Type('INT'),Type('CHAR')] and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('FLOAT')
    elif isinstance(p[1].type,Type) and isinstance(p[1].type.next,Type) and (p[3].type==Type('INT') or p[3].type==Type('CHAR'))and is_primitive(p[1]) and is_primitive(p[3]):
        p[0]=deepcopy(p[1])
        x=1
        y=3
    elif isinstance(p[3].type,Type) and isinstance(p[3].type.next,Type) and (p[3].type==Type('INT') or p[3].type==Type('CHAR')) and is_primitive(p[1]) and is_primitive(p[3]):
        p[0]=deepcopy(p[3])
        x=3
        y=1 
    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print "Error in line %s : Cannot perform addition between %s and %s " %(p.lineno(2),find_type(p[1]),find_type(p[3]))

    if p[0].type != Type('ERROR'):
        p[0].offset = size 
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}
        
        if x>0:
            dim=1
            if p[x].attr.has_key('dim'):
                for i in range(1,len(p[x].attr['dim'])):
                    dim=dim*p[x].attr['dim'][i]

            p[0].code = p[1].code + p[3].code
            p[0].code+="\tli $t0 "+dim+"\n"
            p[0].code+="\tli $t1 "+p[x].size+"\n"
            p[0].code+="\tmul $t1 $t1 $t0\n"
            p[0].code += "\tlw $t0 " + toAddr(p[x].offset) + "\n"
            p[0].code += "\tlw $t2 " + toAddr(p[y].offset) + "\n"
            p[0].code +="\tmul $t1 $t1 $t2\n"
            p[0].code += "\tadd $t0, $t0, $t1\n"
            p[0].code += "\tsw $t0 " + toAddr(p[0]) + "\n"
        else:
            p[0].code = p[1].code + p[3].code
            p[0].code += "\tlw $t0 " + toAddr(p[1]) + "\n"
            p[0].code += "\tlw $t1 " + toAddr(p[3]) + "\n"
            p[0].code += "\tadd $t2, $t0, $t1\n"
            p[0].code += "\tsw $t2 " + toAddr(p[0]) + "\n"

    p.set_lineno(0,p.lineno(2))
                  
def p_additive_expression_3(p):
    ''' additive_expression : additive_expression MINUS multiplicative_expression '''
    global size
    x=-1
    p[0]=deepcopy(p[1])
    if p[1].type==Type('CHAR') and p[3].type==Type('CHAR')and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('CHAR')
    elif p[1].type in [Type('INT'),Type('CHAR')] and p[3].type in [Type('INT'),Type('CHAR')]and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('INT')
    elif p[1].type in [Type('FLOAT'),Type('INT'),Type('CHAR')] and p[3].type in [Type('FLOAT'),Type('INT'),Type('CHAR')] and is_primitive(p[1])and is_primitive(p[3]):
        p[0].type=Type('FLOAT')
    elif isinstance(p[1].type,Type) and isinstance(p[1].type.next,Type) and (p[3].type==Type('INT') or p[3].type==Type('CHAR'))and is_primitive(p[1]) and is_primitive(p[3]):
        p[0]=deepcopy(p[1])
        x=1
        y=3
    elif isinstance(p[3].type,Type) and isinstance(p[3].type.next,Type) and (p[3].type==Type('INT') or p[3].type==Type('CHAR')) and is_primitive(p[1]) and is_primitive(p[3]):
        p[0]=deepcopy(p[3])
        x=3
        y=1 
    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print "Error in line %s : Cannot perform substraction between %s and %s " %(p.lineno(2),find_type(p[1]),find_type(p[3]))

    if p[0].type != Type('ERROR'):
        p[0].offset = size 
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}
        if x>0:
            dim=1
            if p[x].attr.has_key('dim'):
                for i in range(1,len(p[x].attr['dim'])):
                    dim=dim*p[x].attr['dim'][i]

            p[0].code = p[1].code + p[3].code
            p[0].code+="\tli $t0 "+dim+"\n"
            p[0].code+="\tli $t1 "+p[x].size+"\n"
            p[0].code+="\tmul $t1 $t1 $t0\n"
            p[0].code += "\tlw $t0 " + toAddr(p[x].offset) + "\n"
            p[0].code += "\tlw $t2 " + toAddr(p[y].offset) + "\n"
            p[0].code +="\tmul $t1 $t1 $t2\n"
            p[0].code += "\tsub $t0, $t0, $t1\n"
            p[0].code += "\tsw $t0 " + toAddr(p[0]) + "\n"
        else:
            p[0].code = p[1].code + p[3].code
            p[0].code += "\tlw $t0 " + toAddr(p[1]) + "\n"
            p[0].code += "\tlw $t1 " + toAddr(p[3]) + "\n"
            p[0].code += "\tsub $t2, $t0, $t1\n"
            p[0].code += "\tsw $t2 " + toAddr(p[0]) + "\n"

    p.set_lineno(0,p.lineno(2))
                      
#shift-expression:
    #additive-expression
    #shift-expression << additive-expression
    #shift-expression >> additive-expression

def p_relational_expression_1(p): 
    ''' relational_expression : additive_expression'''
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))
                  
def p_relational_expression_2(p):
    ''' relational_expression : relational_expression LESS additive_expression'''
    global size
    p[0]=deepcopy(p[1])
    if check_compatibility_relational(p):
        p[0].type=Type('BOOL')
        p[0].offset = size 
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}

    #TODO: Array handling , etc..
        p[0].code = p[1].code + p[3].code
        p[0].code += "\tlw $t0 " + toAddr(p[1]) + "\n"
        p[0].code += "\tlw $t1 " + toAddr(p[3]) + "\n"
        p[0].code += "\tslt $t2, $t0, $t1\n"
        p[0].code += "\tsw $t2 " + toAddr(p[0]) + "\n"

    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print "Error in line %s : < operator cannot be applied between %s and %s " %(p.lineno(2),find_type(p[1]),find_type(p[3]))
    p.set_lineno(0,p.lineno(2))
    
def p_relational_expression_3(p):
    ''' relational_expression : relational_expression GREATER additive_expression '''
    global size
    p[0]=deepcopy(p[1])
    if check_compatibility_relational(p):
        p[0].type=Type('BOOL')
        p[0].offset = size 
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}
    #TODO: Array handling , etc..
        p[0].code = p[1].code + p[3].code
        p[0].code += "\tlw $t0 " + toAddr(p[1]) + "\n"
        p[0].code += "\tlw $t1 " + toAddr(p[3]) + "\n"
        p[0].code += "\tslt $t2, $t1, $t0\n"
        p[0].code += "\tsw $t2 " + toAddr(p[0]) + "\n"
    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print "Error in line %s : > operator cannot be applied between %s and %s " %(p.lineno(2),find_type(p[1]),find_type(p[3]))
    p.set_lineno(0,p.lineno(2))

def p_relational_expression_4(p):
    ''' relational_expression : relational_expression LESS_EQ additive_expression '''
    global size
    p[0]=deepcopy(p[1])
    if check_compatibility_relational(p):
        p[0].type=Type('BOOL')

        p[0].offset = size
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}
        p[0].code = p[1].code + p[3].code
        p[0].code += "\tlw $t0 " + toAddr(p[1]) + "\n"
        p[0].code += "\tlw $t1 " + toAddr(p[3]) + "\n"
        p[0].code += "\tslt $t2, $t1, $t0\n"                  # t2 stores greater than result
        p[0].code += "\tli $t3 1\n"
        p[0].code += "\tsub $t3, $t3, $t2\n"                  # invert t2
        p[0].code += "\tsw $t3 " + toAddr(p[0]) + "\n" 

    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print "Error in line %s : <= operator cannot be applied between %s and %s " %(p.lineno(2),find_type(p[1]),find_type(p[3]))
    p.set_lineno(0,p.lineno(2))

def p_relational_expression_5(p):
    ''' relational_expression : relational_expression GREATER_EQ additive_expression '''
    global size
    p[0]=deepcopy(p[1])
    if check_compatibility_relational(p):
        p[0].type=Type('BOOL')
        p[0].offset = size
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}
        p[0].code = p[1].code + p[3].code
        p[0].code += "\tlw $t0 " + toAddr(p[1]) + "\n"
        p[0].code += "\tlw $t1 " + toAddr(p[3]) + "\n"
        p[0].code += "\tslt $t2, $t0, $t1\n"                  # t2 stores less than result
        p[0].code += "\tli $t3 1\n"
        p[0].code += "\tsub $t3, $t3, $t2\n"                  # invert t2
        p[0].code += "\tsw $t3 " + toAddr(p[0]) + "\n" 
    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print "Error in line %s : >= operator cannot be applied between %s and %s " %(p.lineno(2),find_type(p[1]),find_type(p[3]))
    p.set_lineno(0,p.lineno(2))

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

#equality-expression:
    #relational-expression
    #equality-expression == relational-expression
    #equality-expression != relational-expression
def p_equality_expression_1(p):
    ''' equality_expression : relational_expression '''
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))
                  
def p_equality_expression_2(p):
    ''' equality_expression : equality_expression IS_EQ relational_expression '''
    global size
    p[0]=deepcopy(p[1])
    if check_compatibility_equality(p):
        p[0].type=Type('BOOL')

        p[0].offset = size 
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}
        p[0].code = p[1].code + p[3].code
        p[0].code += "\tlw $t0, " + toAddr(p[1]) + "\n"
        p[0].code += "\tlw $t1, " + toAddr(p[3]) + "\n"
        p[0].code += "\tslt $t2, $t0, $t1\n"
        p[0].code += "\tslt $t3, $t1, $t0\n"
        p[0].code += "\tadd $t1, $t2, $t3\n"
        p[0].code += "\tli $t0, 1\n"
        p[0].code += "\tsub $t0, $t0, $t1\n"
        p[0].code += "\tsw $t0, " + toAddr(p[0]) + "\n"

    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print "Error in line %s : == operator cannot be applied between %s and %s " %(p.lineno(2),find_type(p[1]),find_type(p[3]))
    p.set_lineno(0,p.lineno(2))
    
def p_equality_expression_3(p):
    ''' equality_expression : equality_expression NOT_EQ relational_expression '''
    global size
    p[0]=deepcopy(p[1])
    if check_compatibility_equality(p):
        p[0].type=Type('BOOL')

        p[0].offset = size 
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}
        p[0].code = p[1].code + p[3].code
        p[0].code += "\tlw $t0, " + toAddr(p[1]) + "\n"
        p[0].code += "\tlw $t1, " + toAddr(p[3]) + "\n"
        p[0].code += "\tslt $t2, $t0, $t1\n"
        p[0].code += "\tslt $t3, $t1, $t0\n"
        p[0].code += "\tadd $t1, $t2, $t3\n"
        p[0].code += "\tsw $t1, " + toAddr(p[0]) + "\n"

    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print "Error in line %s : != operator cannot be applied between %s and %s " %(p.lineno(2),find_type(p[1]),find_type(p[3]))
    p.set_lineno(0,p.lineno(2))
    
#and-expression:
    #equality-expression
    #and-expression & equality-expression


#exclusive-or-expression:
    #and-expression
    #exclusive-or-expression ^ and-expression


#inclusive-or-expression:
    #exclusive-or-expression
    #inclusive-or-expression | exclusive-or-expression


#logical-and-expression:
    #inclusive-or-expression
    #logical-and-expression && inclusive-or-expression
def p_logical_and_expression_1(p):
    ''' logical_and_expression : equality_expression'''
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))


#TODO: Lookup short-circuiting and back-patching in logical expressions
def p_logical_and_expression_2(p):
    ''' logical_and_expression : logical_and_expression DOUBLE_AMPERSAND equality_expression'''
    global size 
    p[0]=deepcopy(p[1])
    if p[1].type==Type('BOOL') and p[3].type==Type('BOOL') and is_primitive(p[1])and is_primitive(p[3]) :
        p[0].type=Type('BOOL')

        p[0].offset = size 
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}
        p[0].code = p[1].code + p[3].code
        p[0].code += "\tlw $t0, " + toAddr(p[1]) + "\n"
        p[0].code += "\tlw $t1, " + toAddr(p[3]) + "\n"
        p[0].code += "\tand $t2, $t0, $t1\n"
        p[0].code += "\tsw $t2, " + toAddr(p[0]) + "\n"

    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print 'Error at line %s : && operator can only be applied to boolean operands' % p.lineno(2)
    p.set_lineno(0,p.lineno(2))            

#logical-or-expression:
    #logical-and-expression
    #logical-or-expression || logical-and-expression
def p_logical_or_expression_1(p):
    ''' logical_or_expression : logical_and_expression '''
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))

def p_logical_or_expression_2(p):
    ''' logical_or_expression : logical_or_expression DOUBLE_PIPE logical_and_expression ''' 
    global size
    p[0]=deepcopy(p[1])
    if p[1].type==Type('BOOL') and p[3].type==Type('BOOL') and is_primitive(p[1])and is_primitive(p[3]) :
        p[0].type=Type('BOOL')

        p[0].offset = size 
        size = size + 4
        p[0].place = newTemp()
        p[0].attr={}
        p[0].code = p[1].code + p[3].code
        p[0].code += "\tlw $t0, " + toAddr(p[1]) + "\n"
        p[0].code += "\tlw $t1, " + toAddr(p[3]) + "\n"
        p[0].code += "\tor $t2, $t0, $t1\n"
        p[0].code += "\tsw $t2, " + toAddr(p[0]) + "\n"


    else:
        p[0]=errorAttr(p[0])
        if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
            print 'Error at line %s : || operator can only be applied to boolean operands' % p.lineno(2)
    p.set_lineno(0,p.lineno(2))


#conditional-expression:
    #logical-or-expression
    #logical-or-expression ? expression : assignment-expression
                  
def p_conditional_expression_1(p):
    ''' conditional_expression : logical_or_expression '''
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))
            
def p_conditional_expression_2(p):
    ''' conditional_expression : logical_or_expression QUESTION expression COLON assignment_expression '''
    p[0]=deepcopy(p[1])
    global size 
    p[0].offset = size 
    size += 4
    p[0].place = newTemp()
    p[0].attr={}
    p[0].code = p[1].code + p[3].code + p[5].code 
    p[0].code += "\tlw $t0, " + toAddr(p[1]) + "\n"
    p[0].code += "\tlw $t1, " + toAddr(p[3]) + "\n"
    p[0].code += "\tlw $t2, " + toAddr(p[5]) + "\n"
    p[0].code += "\tmovn $t3, $t1, $t0 " + "\n"
    p[0].code += "\tmovz $t3, $t2, $t0 " + "\n"
    p[0].code += "\tsw $t3, " +toAddr(p[0]) + "\n"
    if p[1].type==Type('BOOL') and is_primitive(p[1]):
        #have to choose statement based on conditional evaluation
        pass
    else:
        if p[1].type!=Type(Type('ERROR')) and p[3].type!=Type(Type('ERROR')) and p[5].type!=Type(Type('ERROR')):
            print 'Error at line %s : ? ternary operator can only be applied to boolean operands' % p.lineno(2)
        p[0]=errorAttribute(p[0])
    p.set_lineno(0,p.lineno(2))
        
#assignment-expression:
    #conditional-expression
    #logical-or-expression assignment-operator assignment-expression
    #throw-expression

def p_assignment_expression_1(p):
    ''' assignment_expression : conditional_expression '''
    p[0] = deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))


def check_implicit_1(p,q):
    if not is_primitive(p) or not is_primitive(q):
       return False
    elif p.type ==q.type:
        return True
    elif p.type == Type('FLOAT') and (q.type== Type('INT') or q.type== Type('CHAR')):
        return True
    elif p.type == Type('INT') and  q.type== Type('CHAR'):
        return True
    else:
        return False
    
def check_implicit_2(p,q):
    if not is_primitive(p) or not is_primitive(q):
       return False
    elif p.type in [Type('FLOAT'),Type('INT'),Type('CHAR')] and p.type ==q.type:
        return True
    elif p.type == Type('FLOAT') and (q.type== Type('INT') or q.type== Type('CHAR')):
        return True
    elif p.type == Type('INT') and  q.type== Type('CHAR'):
        return True
    else:
        return False


#How to check for L-value???
def p_assignment_expression_2(p):
    ''' assignment_expression : logical_or_expression assignment_operator assignment_expression '''                  ## Error handling not included 
    p[0] = Attribute()
    p[0].type=p[1].type
    global size
    p[0].place=newTemp()
    p[0].attr={}
    p[0].offset = size 
    size += 4
    p[0].code = p[1].code + p[3].code 
        
    if p[2]=='=':
        if check_implicit_1(p[1],p[3]):
            p[0].code += "\tlw $t0, " + toAddr(p[3]) + "\n"
            p[0].code += "\tsw $t0, " + toAddr(p[1]) + "\n"
            p[0].code += "\tsw $t0, " + toAddr(p[0]) + "\n"

        else:
            if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
                print 'Error in line %s : Incompatible assignment operation. Cannot assign %s to %s ' % (p.lineno(2),find_type(p[3]),find_type(p[1])) 
            p[0]=errorAttr(p[0])
            p[1].type=Type('ERROR')
            
    else:
        if p[2]=='*=':
            if check_implicit_2(p[1],p[3]):
                p[0].code += "\tlw $t0, " + toAddr(p[3]) + "\n"
                p[0].code += "\tlw $t1, " + toAddr(p[1]) + "\n"
                p[1].code += "\tmul $t2, $t1, $t0" + "\n"
                p[0].code += "\tsw $t2, " + toAddr(p[1]) + "\n"
                p[0].code += "\tsw $t2, " + toAddr(p[0]) + "\n"
            else:
                if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
                    print 'Error in line %s : Cannot apply %s to %s' %(p.lineno(2),p[2],find_type(p[1]))
                p[0]=errorAttr(p[0])
                p[1].type=Type('ERROR')
        if p[2]=='/=':
            if check_implicit_2(p[1],p[3]):
                p[0].code += "\tlw $t0, " + toAddr(p[3]) + "\n"
                p[0].code += "\tlw $t1, " + toAddr(p[1]) + "\n"
                p[1].code += "\tdiv $t1, $t0" + "\n"
                p[0].code += "\tsw $lo, " + toAddr(p[1]) + "\n"
                p[0].code += "\tsw $lo, " + toAddr(p[0]) + "\n"
            else:
                if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
                    print 'Error in line %s : Cannot apply %s to %s' %(p.lineno(2),p[2],find_type(p[1]))
                p[0]=errorAttr(p[0])
                p[1].type=Type('ERROR')

        if p[2]=='+=':
            if check_implicit_2(p[1],p[3]):
                p[0].code += "\tlw $t0, " + toAddr(p[3]) + "\n"
                p[0].code += "\tlw $t1, " + toAddr(p[1]) + "\n"
                p[1].code += "\tadd $t2, $t1, $t0" + "\n"
                p[0].code += "\tsw $t2, " + toAddr(p[1]) + "\n"
                p[0].code += "\tsw $t2, " + toAddr(p[0]) + "\n"
                pass                                                                  
            elif isinstance(p[1].type,Type) and isinstance(p[1].type.next,Type) and (p[3].type=='INT' or p[3].type=='CHAR') and is_primitive(p[3]):
                p[0].offset = size 
                size = size + 4
                p[0].place = newTemp()
                dim=p[1].type.next.size()
                p[0].code = p[1].code + p[3].code
                p[0].code += "\tlw $t0 " + toAddr(p[1]) + "\n"
                p[0].code += "\tlw $t1 " + toAddr(p[3]) + "\n"
                p[0].code+="\tli $t2 "+dim+"\n"
                p[0].code +="\tmul $t1 $t0 $t2\n"
                p[0].code += "\tadd $t0 $t0 $t1\n"
                p[0].code += "\tsw $t0 " + toAddr(p[0]) + "\n"          
            else:
                if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
                    print 'Error in line %s : Cannot apply += to %s' %(p.lineno(2),find_type(p[1]))        
                p[0]=errorAttr(p[0])
                p[1].type=Type('ERROR')                    

        if p[2]=='-=':
            if check_implicit_2(p[1],p[3]):
                p[0].code += "\tlw $t0, " + toAddr(p[3]) + "\n"
                p[0].code += "\tlw $t1, " + toAddr(p[1]) + "\n"
                p[1].code += "\tsub $t2, $t1, $t0" + "\n"
                p[0].code += "\tsw $t2, " + toAddr(p[1]) + "\n"
                p[0].code += "\tsw $t2, " + toAddr(p[0]) + "\n"
                pass                                                                  
            elif isinstance(p[1].type,Type) and isinstance(p[1].type.next,Type) and (p[3].type=='INT' or p[3].type=='CHAR') and is_primitive(p[3]):
                p[0].offset = size 
                size = size + 4
                p[0].place = newTemp()
                dim=p[1].type.next.size()
                p[0].code = p[1].code + p[3].code
                p[0].code += "\tlw $t0 " + toAddr(p[1]) + "\n"
                p[0].code += "\tlw $t1 " + toAddr(p[3]) + "\n"
                p[0].code+="\tli $t2 "+dim+"\n"
                p[0].code +="\tmul $t1 $t0 $t2\n"
                p[0].code += "\tsub $t0 $t0 $t1\n"
                p[0].code += "\tsw $t0 " + toAddr(p[0]) + "\n"
            else:
                if p[1].type!=Type('ERROR') and p[3].type!=Type('ERROR'):
                    print 'Error in line %s : Cannot apply -= to %s' %(p.lineno(2),find_type(p[1]))        
                p[0]=errorAttr(p[0])
                p[1].type=Type('ERROR')                    
    p.set_lineno(0,p.lineno(2))
                                              
#assignment-operator: one of
#= *= /= %= += -= >>= <<= &= ^= |=                                                         ## Add these to operators and add them here 
def p_assignment_operator(p):
    ''' assignment_operator : ASSIGN 
                    | EQ_TIMES
                    | EQ_DIV 
                    | EQ_MODULO
                    | EQ_PLUS
                    | EQ_MINUS '''
    p[0]=p[1]
    p.set_lineno(0,p.lineno(1))


#expression:
    #assignment-expression
    #expression , assignment-expression

def p_expression_1(p):
    ''' expression : assignment_expression '''                
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))

def p_expression_2(p):
    ''' expression : expression COMMA assignment_expression '''
    p[0]=deepcopy(p[1])
    if p[1].type==Type('ERROR') or p[2].type==Type('ERROR'):
        p[0].type=Type('ERROR')
    else:
        p[0].code=p[1].code+p[3].code
        p[0].type=Type('VOID')
    p.set_lineno(0,p.lineno(2))

#constant-expression:
    #conditional-expression
def p_constant_expression(p):
    ''' constant_expression : conditional_expression ''' 
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))

def p_constant_expression_opt_1(p):
    ''' constant_expression_opt : '''
    p[0]=None

def p_constant_expression_opt_2(p):
    ''' constant_expression_opt : constant_expression '''
    p[0]=deepcopy(p[1])
    p.set_lineno(0,p.lineno(1))
## }}}

####################################################

#################### STATEMENTS ####################

## {{{
#statement:
    #labeled-statement
    #expression-statement
    #compound-statement
    #selection-statement
    #iteration-statement
    #jump-statement
    #declaration-statement
    #try-block
def p_statement_1(p):
    ''' statement : labeled_statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    pass 
def p_statement_2(p):
    ''' statement : expression_statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    pass 
def p_statement_3(p):
    ''' statement : compound_statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    pass 
def p_statement_4(p):
    ''' statement : selection_statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    pass 
def p_statement_5(p):
    ''' statement : iteration_statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    pass 
def p_statement_6(p):
    ''' statement : jump_statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    pass 
def p_statement_7(p):
    ''' statement : declaration_statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    pass 

#labeled-statement:
    #identifier : statement
    #case constant-expression : statement
    #default : statement
def p_labeled_statement_1(p):
    ''' labeled_statement : IDENTIFIER COLON statement ''' 
    p.set_lineno(0,p.lineno(1))
    global env 
    t = Symbol(p[1])
    t.attr["islabel"] = True 
    if not env.put(t):
        print("Error : Identifier " + str(p[1]) + "already defined" + " line no  " + str(p.lineno(1)))
    p[0] = deepcopy(p[3])
    pass 
def p_labeled_statement_2(p):
    ''' labeled_statement : CASE constant_expression COLON statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0].type = p[4].type 
    pass 
def p_labeled_statement_3(p):
    ''' labeled_statement : DEFAULT COLON statement ''' 
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[3])
    pass 

#expression-statement:
    #expressionopt ;
def p_expression_statement_1(p):
    ''' expression_statement : SEMICOLON ''' 
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0].type = Type("VOID")
    pass 
def p_expression_statement_2(p):
    ''' expression_statement : expression SEMICOLON '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[1].type == Type("ERROR"):
        p[0].type = Type("ERROR")
    else:
        p[0].type = Type("VOID") 
    pass 

#compound-statement:
    #{ statement-seqopt }
def p_compound_statement_1(p):
    ''' compound_statement : LBRACE RBRACE '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0].type = Type("VOID")

    p[0].code = "" # empty code needed to pass

def p_compound_statement_2(p):
    ''' compound_statement : LBRACE new_scope statement_seq finish_scope RBRACE '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[3])
    if p[3].type == Type("ERROR"):
        p[0].type = Type("ERROR")
    else :
        p[0].type = Type("VOID")


#statement-seq:
    #statement
    #statement-seq statement
def p_statement_seq_1(p):
    ''' statement_seq : statement ''' 
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    if p[1].type == Type("ERROR"):
        p[0].type = Type("ERROR")
    else :
        p[0].type = Type("VOID")
    

def p_statement_seq_2(p):
    ''' statement_seq : statement_seq statement'''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    if p[1].type == Type("VOID") and p[2].type == Type("VOID"):
        p[0].type = Type("VOID")
    else :
        p[0].type = Type("ERROR")

    p[0].code = p[1].code + p[2].code

#selection-statement:
    #if ( condition ) statement
    #if ( condition ) statement else statement
    #switch ( condition ) statement
def p_selection_statement_1(p):
    ''' selection_statement : IF LPAREN condition RPAREN statement %prec IFX '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[3].type == Type("BOOL"):
        if p[5].type == Type("ERROR"):
            p[0].type = Type("ERROR")
        else :
            p[0].type = Type("VOID")
    else :
        if p[3].type != Type("ERROR"):
            print("Type error at" + str(p.lineno(3)))
        p[0].type = Type("ERROR")

    #code generation
    safter = newLabel()
    p[0].code = p[3].code 
    p[0].code += "\tlw $t0, " + toAddr(p[3]) + "\n"
    p[0].code += "\tbeq $t0, $0, " + safter + "\n"
    p[0].code += p[5].code
    p[0].code += "\t" + safter + ":\n"

def p_selection_statement_2(p):
    ''' selection_statement : IF LPAREN condition RPAREN statement ELSE statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[3].type == Type("BOOL"):
        if p[5].type == Type("VOID") and p[7].type == Type("VOID"):
            p[0].type = Type("VOID")
        else :
            p[0].type = Type("ERROR")
    else :
        if p[3].type != Type("ERROR"):
            print("Type error at" + str(p.lineno(3)))
        p[0].type = Type("ERROR")

    #code generation
    selse = newLabel()
    safter = newLabel()
    p[0].code = p[3].code 
    p[0].code += "\tlw $t0, " + toAddr(p[3]) + "\n"
    p[0].code += "\tbeq $t0, $0 " + selse + "\n"
    p[0].code += p[5].code
    p[0].code += "\tj " + safter + "\n"
    p[0].code += "\t" + selse + ":\n"
    p[0].code += p[7].code
    p[0].code += "\t" + safter + ":\n"

def p_selection_statement_3(p):
    ''' selection_statement : SWITCH LPAREN condition RPAREN statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[3].type == Type("BOOL"):
        if p[5].type == Type("ERROR"):
            p[0].type = Type("ERROR")
        else :
            p[0].type = Type("VOID")
    else :
        if p[3].type != Type("ERROR"):
            print("Type error at" + str(p.lineno(3)))
        p[0].type = Type("ERROR")
    pass 

#condition:
    #expression
    #type-specifier-seq declarator = assignment-expression
def p_condition_1(p):
    ''' condition : expression ''' 
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[1].type != Type("ERROR"):
        p[0].type = Type("BOOL")
    else :
        p[0].type = Type("ERROR")
    pass 
def p_condition_2(p):
    ''' condition : type_specifier_seq declarator ASSIGN assignment_expression '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[1].type==p[4].type and p[1].type is not None and p[4].type is not None:
        p[0].type=Type('BOOL')
    else:
        p[0].type=Type('ERROR')

#iteration-statement:
    #while ( condition ) statement
    #do statement while ( expression ) ;
    #for ( for-init-statement conditionopt ; expressionopt ) statement
def p_iteration_statement_1(p):
    ''' iteration_statement : WHILE LPAREN condition RPAREN statement ''' 
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[3].type == Type("BOOL"):
        if p[5].type == Type("ERROR"):
            p[0].type = Type("ERROR")
        else :
            p[0].type = Type("VOID")
    else :
        if p[3].type != Type("ERROR"):
            print("Type error at" + str(p.lineno(3)))
        p[0].type = Type("ERROR")

    #code generation
    sbegin = newLabel()
    safter = newLabel()
    p[0].code = "\t" + sbegin + ":\n"
    p[0].code += p[3].code 
    p[0].code += "\tlw $t0, " + toAddr(p[3]) + "\n"
    p[0].code += "\tbeq $t0, $0, " + safter + "\n"
    p[0].code += p[5].code 
    p[0].code += "\tj " + sbegin + "\n"
    p[0].code += "\t" + safter + ":\n"

# Not needed, similar to while
def p_iteration_statement_2(p):
    ''' iteration_statement : DO statement WHILE LPAREN condition RPAREN SEMICOLON '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[5].type == Type("BOOL"):
        if p[2].type == Type("ERROR"):
            p[0].type = Type("ERROR")
        else :
            p[0].type = Type("VOID")
    else :
        if p[5].type != Type("ERROR"):
            print("Type error at" + str(p.lineno(5)))
        p[0].type = Type("ERROR")
    pass 

def p_iteration_statement_3(p):
    ''' iteration_statement : FOR LPAREN for_init_statement condition SEMICOLON expression RPAREN statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[4].type == Type("BOOL"):
        if p[8].type == Type("ERROR"):
            p[0].type = Type("ERROR")
        else :
            p[0].type = Type("VOID")
    else :
        if p[4].type != Type("ERROR"):
            print("Type error at" + str(p.lineno(4)))
        p[0].type = Type("ERROR")

    #code generation
    sbegin = newLabel()
    safter = newLabel()
    p[0].code = p[3].code
    p[0].code += "\t" + sbegin + ":\n"
    p[0].code += p[4].code 
    p[0].code += "\tlw $t0, " + toAddr(p[4]) + "\n"
    p[0].code += "\tbeq $t0, $0, " + safter + "\n"
    p[0].code += p[8].code 
    p[0].code += p[6].code
    p[0].code += "\tj " + sbegin + "\n"
    p[0].code += "\t" + safter + ":\n"

def p_iteration_statement_4(p):
    ''' iteration_statement : FOR LPAREN for_init_statement condition SEMICOLON RPAREN statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[4].type == Type("BOOL"):
        if p[7].type == Type("ERROR"):
            p[0].type = Type("ERROR")
        else :
            p[0].type = Type("VOID")
    else :
        if p[4].type != Type("ERROR"):
            print("Type error at" + str(p.lineno(4)))
        p[0].type = Type("ERROR")
    
    #code generation
    sbegin = newLabel()
    safter = newLabel()
    p[0].code = p[3].code
    p[0].code += "\t" + sbegin + ":\n"
    p[0].code += p[4].code 
    p[0].code += "\tlw $t0, " + toAddr(p[4]) + "\n"
    p[0].code += "\tbeq $t0, $0, " + safter + "\n"
    p[0].code += p[7].code 
    p[0].code += "\tj " + sbegin + "\n"
    p[0].code += "\t" + safter + ":\n"

def p_iteration_statement_5(p):
    ''' iteration_statement : FOR LPAREN for_init_statement SEMICOLON expression RPAREN statement'''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[7].type == Type("ERROR"):
        p[0].type = Type("ERROR")
    else :
        p[0].type = Type("VOID")
    
    #code generation
    sbegin = newLabel()
    #safter = newLabel() - safter not required in this case
    p[0].code = p[3].code
    p[0].code += "\t" + sbegin + ":\n"
    p[0].code += p[7].code 
    p[0].code += p[5].code
    p[0].code += "\tj " + sbegin + "\n"
    #p[0].code += "\t" + safter + ":\n"

def p_iteration_statement_6(p):
    ''' iteration_statement : FOR LPAREN for_init_statement SEMICOLON RPAREN statement '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[1].type == Type("ERROR"):
        p[0].type = Type("ERROR")
    else :
        p[0].type = Type("VOID")

    #code generation
    sbegin = newLabel()
    #safter = newLabel() - safter not required in this case
    p[0].code = p[3].code
    p[0].code += "\t" + sbegin + ":\n"
    p[0].code += p[6].code 
    p[0].code += "\tj " + sbegin + "\n"
    #p[0].code += "\t" + safter + ":\n"


#for-init-statement:
    #expression-statement
    #simple-declaration
def p_for_init_statement_1(p):
    ''' for_init_statement : expression_statement ''' 
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0].type = Type("VOID")
    
    p[0].code = p[1].code

# need to support a different scope system - currently buggy
def p_for_init_statement_2(p):
    ''' for_init_statement : simple_declaration '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0].type = Type("VOID") 

    p[0].code = p[1].code

#jump-statement:
    #break ;
    #continue ;
    #return expressionopt ;
    #goto identifier ;
def p_jump_statement_1(p):
    ''' jump_statement : BREAK ''' 
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0].type = Type("VOID") 
    global env
    p[0].code = "\tj " + env.table.endlabel + "\n"

def p_jump_statement_2(p):
    ''' jump_statement : CONTINUE '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0].type = Type("VOID") 
    global env
    p[0].code = "\tj " + env.table.startlabel + "\n"

def p_jump_statement_3(p):
    ''' jump_statement : RETURN expression SEMICOLON '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0].type = Type("VOID") 
    pass 
def p_jump_statement_4(p):
    ''' jump_statement : RETURN SEMICOLON '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0].type = Type("VOID") 
    pass 

#declaration-statement:
    #block-declaration
def p_declaration_statement(p):
    ''' declaration_statement : block_declaration '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    if p[1].type == Type("ERROR"):
        p[0].type = Type("ERROR")
    else :
        p[0].type = Type("VOID")
    pass
## }}}

####################################################

#################### DECLARATIONS ##################

## {{{
#declaration:
    #block-declaration
    #function-definition
    #template-declaration
    #explicit-instantiation
    #explicit-specialization
    #linkage-specification
    #namespace-definition

def p_declaration_1(p):
    ''' declaration : block_declaration '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
      
def p_declaration_2(p):
    ''' declaration : function_definition '''
    p.set_lineno(0,p.lineno(1))
    p[0]= deepcopy(p[1])
    

### TODO : Commenting this rule as rule corresponding to namespace_definition has not been added anywhere. Have to add later.###
#def p_declaration_4(p):
#    ''' declaration : namespace_definition '''
#    pass

#block-declaration:
    #simple-declaration
    #asm-definition
    #namespace-alias-definition
    #using-declaration
    #using-directive

def p_block_declaration_1(p):
    ''' block_declaration : simple_declaration '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    
#simple-declaration:
    #decl-specifier-seqopt init-declarator-listopt ;

def p_simple_declaration_1(p):
    ''' simple_declaration : decl_specifier_seq init_declarator_list SEMICOLON '''
    p.set_lineno(0,p.lineno(1))
    global env
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = p[1].type
    p[0].attr["init_declarator_list"] = deepcopy(p[2].attr["init_declarator_list"])
    p[0].attr["declaration"] = 1
    p[0].code = p[2].code
    if p[1].type == Type("ERROR") :
        p[0].type = Type("ERROR")
#    elif p[0].type != Type("ERROR") :
#        for t in p[0].attr["init_declarator_list"] :
#            t1 = Symbol(t.attr["name"])
#            t1.type = p[0].type
#            if t.attr.has_key("isFunction"):
#                t1.attr["isFunction"] = 1
#                #t1.isfunction = 1
#                t1.attr["parameterList"] = deepcopy(t.attr["parameterList"])
#            elif t.attr.has_key("isArray"):
#                t1.attr["isArray"]=1
#                #t1.isArray = 1
#                t1.attr["width"] = t.attr["width"]
#            if t.attr["initialized"] == 1:
#                t1.attr["initializer"] = deepcopy(t.attr["initializer"])
#                t1.attr["initialized"] =1
#            if t.type != Type("ERROR") :
#                if not env.put(t1):
#                    print("ERROR: Identifier " + t.name + "already defined. At line number "+ str(p.lineno(2)))
#                    t.type = Type("ERROR")
#            else :
#                t.type = Type("ERROR")
    
def p_simple_declaration_2(p):
    ''' simple_declaration : IDENTIFIER init_declarator_list SEMICOLON %prec INUMBER '''
    p.set_lineno(0,p.lineno(1))

    global env
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    t = env.get(str(p[1]))
    if (t == None):
        print("Error : decl_specifier " + str(p[1]) + "is not defined.")
        p[0].type = Type("ERROR")
    p[0].type = t.type
    p[0].attr["init_declarator_list"] = deepcopy(p[2].attr["init_declarator_list"])
    p[0].attr["declaration"] = 1
    p[0].code = p[2].code
    #if p[1].type == Type("ERROR") :
    #    p[0].type = Type("ERROR")
#    if p[0].type != Type("ERROR") :
#        for t in p[0].attr["init_declarator_list"] :
#            t1 = Symbol(t.attr["name"])
#            t1.type = p[0].type
#            if t.attr.has_key("isFunction"):
#                t1.attr["isFunction"] = 1
                #t1.isfunction = 1
#                t1.attr["parameterList"] = deepcopy(t.attr["parameterList"])
#            elif t.attr.has_key("isArray"):
#                t1.attr["isArray"]=1
                #t1.isArray = 1
#                t1.attr["width"] = t.attr["width"]
#            if t.attr["initialized"] == 1:
#                t1.attr["initializer"] = deepcopy(t.attr["initializer"])
#                t1.attr["initialized"] =1
#            if t.type != Type("ERROR") :
#                if not env.put(t1):
#                    print("ERROR: Identifier " + t.name + "already defined. At line number "+ str(p.lineno(2)))
#                    t.type = Type("ERROR")
#            else :
#                t.type = Type("ERROR")
                    
def p_simple_declaration_3(p):
    ''' simple_declaration : decl_specifier_seq SEMICOLON '''
    p.set_lineno(0,p.lineno(1))
                           #| init_declarator_list SEMICOLON '''
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = p[1].type
    p[0].attr["declaration"] = 1
    p[0].code = ''
    if p[1].type == Type("ERROR") :
        p[0].type = Type("ERROR")
        
    
#def p_mark_type(p):
#    ''' mark_type : %prec INUMBER'''
#    global DeclType
#    global env
#    t = env.get(str(p[-1]))
#    if t==None:
#        p[0] = "ERROR"
#        print "Symbol None"
#        #DeclType = Type("ERROR")
#    elif t.type == Type("CLASS"):
#        DeclType = Type(str(p[-1]))
#    else :
        #print "In else "
#        p[0] = "ERROR"
#        DeclType = Type("ERROR")
#decl-specifier-seq:
    #decl-specifier-seqopt decl-specifier

def p_decl_specifier_seq_1(p):
    ''' decl_specifier_seq : decl_specifier '''
    p.set_lineno(0,p.lineno(1))
    global DeclType
    DeclType = deepcopy(p[1].type)
    p[0] = deepcopy(p[1])
    
#def p_decl_specifier_seq_2(p):
#    ''' decl_specifier_seq : decl_specifier_seq decl_specifier '''
#    p[0] = Attribute()
#    p[0] = initAttr(p[0])
#    p[0].type = 
#    pass

#decl-specifier:
    #storage-class-specifier
    #type-specifier
    #function-specifier
    #friend
    #typedef

def p_decl_specifier_1(p):
    ''' decl_specifier : storage_class_specifier '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    
def p_decl_specifier_2(p):
    ''' decl_specifier : type_specifier '''
    p.set_lineno(0,p.lineno(1))
    
    p[0] = deepcopy(p[1])
    
def p_decl_specifier_3(p):
    ''' decl_specifier : function_specifier '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    
#storage-class-specifier:
    #auto
    #register
    #static
    #extern
    #mutable

def p_storage_class_specifier_1(p):
    ''' storage_class_specifier : AUTO'''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = Type("AUTO")
    
def p_storage_class_specifier_2(p):
    ''' storage_class_specifier : EXTERN '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = Type("EXTERN")
    
#function-specifier:
    #inline
    #virtual
    #explicit

def p_function_specifier(p):
    ''' function_specifier : INLINE '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = Type("INLINE")
    
#type-specifier:
    #simple-type-specifier
    #class-specifier
    #enum-specifier
    #elaborated-type-specifier
    #cv-qualifier

def p_type_specifier_1(p):
    ''' type_specifier : simple_type_specifier '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    
def p_type_specifier_2(p):
    ''' type_specifier : class_specifier '''
                        #| elaborated_type_specifier '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
 
## HELPER 

#def p_double_colon_opt(p):
#    ''' double_colon_opt : 
#                        | SCOPE '''
#    pass

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


##def p_simple_type_specifier_1(p):
##    ''' simple_type_specifier : IDENTIFIER 
##                                | nested_name_specifier class_name  '''
##    ## IDENTIFIER is class name here 
##    pass

#def p_simple_type_specifier_1(p):
    #''' simple_type_specifier : IDENTIFIER  '''
    ### IDENTIFIER is class name here 
    #pass

def p_simple_type_specifier_2(p):
    ''' simple_type_specifier : BOOL '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = Type("BOOL")

def p_simple_type_specifier_3(p):
    ''' simple_type_specifier : CHAR '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = Type("CHAR")

def p_simple_type_specifier_4(p):
    ''' simple_type_specifier : INT '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = Type("INT")

def p_simple_type_specifier_5(p):
    ''' simple_type_specifier : FLOAT '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = Type("FLOAT")

def p_simple_type_specifier_6(p):
    ''' simple_type_specifier : DOUBLE '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = Type("DOUBLE")

def p_simple_type_specifier_7(p):
    ''' simple_type_specifier : VOID '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = Type("VOID")

#type-name:
    #class-name
    #enum-name    
    #typedef-name

def p_type_name_1(p):
    ''' type_name : class_name ''' 
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])

#elaborated-type-specifier:
    #class-key ::opt nested-name-specifieropt identifier
    #enum ::opt nested-name-specifieropt identifier
    #typename ::opt nested-name-specifier identifier
    #typename ::opt nested-name-specifier templateopt template-id
def p_elaborated_type_specifier(p):
    ''' elaborated_type_specifier : class_key IDENTIFIER'''
    p.set_lineno(0,p.lineno(1))
    global env
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = p[1].type
    t = Symbol(str(p[2]))
    t.type = p[1].type
    t.attr["class_id"] = 1
    if not env.put(t) :
        print("Error : Identifier " + str(p[2]) + "already defined" + " line no  " + str(p.lineno(2)))
        p[0].type = Type("ERROR")
    p[0].attr["symbol"] = t
    


##def p_elaborated_type_specifier(p):
##    ''' elaborated_type_specifier : class_key IDENTIFIER
##                                  | class_key SCOPE nested_name_specifier IDENTIFIER
##                                  | class_key IDENTIFIER
##                                  | class_key nested_name_specifier IDENTIFIER '''
##    pass

#linkage_specialization : 
    #extern string-literal { declaration_seq_opt }
    #extern string-literal declaration
#def p_linkage_specialization_1(p):
#    ''' linkage_specialization : EXTERN LIT_STR LBRACE declaration_seq RBRACE 
#                               | EXTERN LIT_STR LBRACE RBRACE '''
#    pass
  
#def p_linkage_specialization_2(p):
#    ''' linkage_specialization : EXTERN LIT_STR declaration '''
#    pass
## }}}
  
##### DECLARATORS #####

## {{{
#init-declarator-list:
    #init-declarator
    #init-declarator-list , init-declarator
def p_init_declarator_list_1(p):
    ''' init_declarator_list : init_declarator '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].attr["init_declarator_list"] = [deepcopy(p[1])]
    p[0].type = p[1].type
    p[0].code = p[1].code
    
def p_init_declarator_list_2(p):
    ''' init_declarator_list : init_declarator_list COMMA mark_1 init_declarator '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    #for key in p[3].attr["init_declarator_list"]:
     #   p[0].attr["init_declarator_list"].append(deepcopy(key))
    p[0].attr["init_declarator_list"].append(deepcopy(p[4]))
    #if p[3].type == Type("ERROR"):
    #    p[0].type = Type("ERROR")
    p[0].code +=p[4].code

#init-declarator:
    #declarator initializeropt
def p_mark_1(p):
    ''' mark_1 : '''
    p[0] = deepcopy(p[-2])
    
def p_init_declarator(p): 
    ''' init_declarator : declarator initializer_opt'''
    p.set_lineno(0,p.lineno(1))
    #p[0] = Attribute()
    #p[0] = initAttr(p[0])
    p[0] = deepcopy(p[1])
    global DeclType
    global env
    global size
    #p[0].code+=p[2].code
    p[0].offset = size
    if not p[1].type == Type("ERROR") or not p[2].type == Type("ERROR"):
        t = Symbol(p[1].attr["name"])
        #entering type for symbol t
        if isinstance(p[-1],Attribute) :
            t.type = p[-1].type
            p[0].type = p[-1].type
        else :
            t1 = env.get(str(p[-1]))
            if t1 == None:
                print("ERROR : Type " + str(p[-1]) + "doesnot exist. At line number : " + str(p.lineno(-1)))
            elif t1.type == Type("CLASS"):
                t.type = Type(str(p[-1]))
                p[0].type = t.type
            else :
                p[0].type = Type("ERROR")
        #t.type = deepcopy(DeclType)
        typ = p[1].type
        while (isinstance(typ,Type)):
            t.type = Type(t.type)
            typ = typ.next
        t.attr = deepcopy(p[1].attr)
        if not env.put(t):
            print("ERROR: Identifier "+t.name+" already defined. At line number : "+str(p.lineno(1)))
            #t.type = Type("ERROR")
            p[0].type = Type("ERROR")
        #Declaring the offset of the symbol and its size
        if p[1].attr.has_key("isFunction") :
            pass
        elif p[1].attr.has_key("isArray"):
            if isinstance(p[1].type, Type) and p[1].type != Type("ERROR"):
                print "ERROR!! Line number : "+ str(p.lineno(0)) + " Invalid declaration"
                p[0].type = Type("ERROR")
            else:
                l = len(p[1].attr["width"])
                while l>0:
                    l=l-1
                    t.type = Type(t.type)
                    t.type.dim = p[1].attr["width"][l]
                t.offset = size
                p[0].offset = size
                size = size+t.type.size()
        else:
            t.offset = size
            p[0].offset = size
            size = size + t.type.size()
        
        if p[2] == None :
            pass
        elif p[2].type == Type("ASSIGN"):
            p[0].code+=p[2].code
            init = p[2].attr["initializer"]
            if p[1].attr.has_key("isFunction"):
                print "ERROR!! Line number : "+str(p.lineno(0))+"Invalid intialization to function."
                p[0].type = Type("ERROR")
            elif p[1].attr.has_key("isArray") and init.attr.has_key("isArray"):
                l = t.type.size()/4
                if l == 0 and init.attr["num_element"] == 0:
                    print "ERROR!! Line number : "+str(p.lineno(0))+" Invalid array declaration and initialization"
                    p[0].type = Type("ERROR")
                elif l == 0 and init.attr["num_element"] != 0 :
                    typ = t.type.next
                    ltyp = typ.size()/4
                    if ltyp == 0:
                        print "ERROR!! Line number : "+str(p.lineno(0))+" Multi-dimensional array '"+str(p[1].attr["name"])+"' must have bounds for all dimensions except the first"
                        p[0].type = Type("ERROR")
                    else :
                        q1 = init.attr["num_element"]/ltyp
                        if ltyp*q1 == init.attr["num_element"]:
                            t.type.dim = q1
                        else:
                            t.type.dim = q1+1
                        i = 0
                        p[0].code+="\tli $t0 "+ p[0].offset + "\n"
                        p[0].code+="\tsub $t0 $fp $t0 \n"
                        p[0].code+="\tli $t2 4 \n"
                        while i < init.attr["num_element"]:
                            p[0].code+= "\tlw $t1, " + toAddr(init.attr["initializer_clause"][i]) + "\n"
                            p[0].code+= "\tsw $t1 0($t0) \n"
                            p[0].code+= "\tsub $t0 $t0 $t2 \n"
                            i+=1
                elif l >= init.attr["num_element"]:
                    i = 0
                    p[0].code+="\tli $t0 "+ p[0].offset + "\n"
                    p[0].code+="\tsub $t0 $fp $t0 \n"
                    p[0].code+="\tli $t2 4 \n"
                    while i < init.attr["num_element"]:
                        p[0].code+= "\tlw $t1, " + toAddr(init.attr["initializer_clause"][i]) + "\n"
                        p[0].code+= "\tsw $t1 0($t0) \n"
                        p[0].code+= "\tsub $t0 $t0 $t2 \n"
                        i+=1
                else :
                    print "ERROR!! Line number : "+str(p.lineno(0))+" Index out of range"
                    p[0].type = Type("ERROR")
                size = p[0].offset + t.type.size()    
            elif p[1].attr.has_key("isArray") or init.attr.has_key("isArray"):
                print "ERROR!! Line number : "+str(p.lineno(0))+ "Invalid initialization"
                p[0].type = Type("ERROR")
            else :
                init = p[2].attr["initializer"]
                if check_implicit_1(p[0],init):
                    p[0].code+= "\tlw $t0, "+ toAddr(init.attr["initializer_clause"][0])+ "\n"
                    p[0].code+= "\tsw $t0, "+ toAddr(p[0]) + "\n"
                else:
                    print "ERROR : Line number : "+ str(p.lineno(2)) + " Incompatible types " + str(t.type) + " and " + str(init.type)    
                    p[0].type = Type("ERROR")
#declarator:
    #direct-declarator
    #ptr-operator declarator
def p_declarator_1(p):
    ''' declarator : direct_declarator %prec NOPAREN'''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
  
def p_declarator_2(p):
    ''' declarator : ptr_operator declarator '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[2])
    if p[1]=='*' :
        p[0].type = Type(p[2].type)
    elif p[1] == '&' :
        p[0].type = Type("ERROR")

#direct-declarator:
    #declarator-id
    #direct-declarator ( parameter-declaration-clause ) cv-qualifier-seqopt exception-specificationopt
    #direct-declarator [ constant-expressionopt ]
    #( declarator )
def p_direct_declarator_1(p):
    ''' direct_declarator : declarator_id '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])

# function declaration rule
def p_direct_declarator_2(p):
    ''' direct_declarator : direct_declarator LPAREN parameter_declaration_clause RPAREN '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    #p[0].code+=p[3].code
    p[0].attr['isFunction'] = 1
    if p[3]==None:
        p[0].attr["parameterList"] = []
        p[0].attr["numParameters"] = 0
    else :
        p[0].code+=p[3].code
        p[0].attr["parameterList"] = deepcopy(p[3].attr["parameterList"])
        p[0].attr["numParameters"] = p[3].attr["numParameters"]
        if p[3].type == Type("ERROR"):
            p[0].type = Type("ERROR")

#array declaration rule  
def p_direct_declarator_3(p):
    ''' direct_declarator : direct_declarator LBRACKET constant_expression_opt RBRACKET '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    if not p[0].attr.has_key("isArray"):
        p[0].attr["isArray"]=1
        if p[3] == None:
            p[0].attr["width"] = [0]
        elif p[3].type == Type("INT") and is_primitive(p[3]) and is_integer(p[3]):
            p[0].attr["width"] = [int(p[3].place)]
            p[0].code+=p[3].code
        elif p[3].type == Type("ERROR"):
            p[0].type = Type("ERROR")
        else:
            print "ERROR!! Line number : "+str(p.lineno(0))+" Invalid array declaration"
    else:
        if p[3] == None:
            p[0].attr["width"].append(0)
        elif p[3].type == Type("INT") and is_primitive(p[3]) and is_integer(p[3]):
            p[0].attr["width"].append(p[3].place)
            p[0].code+=p[3].code
        elif p[3].type == Type("ERROR"):
            p[0].type = Type("ERROR")
        else:
            print "ERROR!! Line number : "+str(p.lineno(0))+" Invalid array declaration"
  
def p_direct_declarator_4(p):
    ''' direct_declarator : LPAREN declarator RPAREN '''
    p.set_lineno(0,p.lineno(1))
    pass 

#ptr-operator:
    #* cv-qualifier-seqopt
    #&
    #::opt nested-name-specifier * cv-qualifier-seqopt

##def p_ptr_operator(p):
##    ''' ptr_operator : TIMES 
##                    | AMPERSAND 
##                    | SCOPE nested_name_specifier TIMES
##                    | nested_name_specifier TIMES '''
##    pass 


def p_ptr_operator_1(p):
    ''' ptr_operator : TIMES '''
    p.set_lineno(0,p.lineno(1))
    p[0] = '*'

def p_ptr_operator_2(p):
    ''' ptr_operator : AMPERSAND '''
    p.set_lineno(0,p.lineno(1))
    p[0] = '&'

#cv-qualifier-seq:
    #cv-qualifier cv-qualifier-seqopt
def p_cv_qualifier_seq_opt(p):
    ''' cv_qualifier_seq_opt : '''
    p[0] = None

#cv-qualifier:
    #const
    #volatile

#def p_cv_qualifier(p):
    #''' cv_qualifier : '''
    #pass 

#declarator-id:
    #::opt id-expression
    #::opt nested-name-specifieropt type-name

def p_declarator_id(p):
    ''' declarator_id : id_expression '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])


##def p_declarator_id(p):
##    ''' declarator_id : SCOPE id_expression 
##                    | id_expression '''
##    pass 

                    #| SCOPE nested_name_specifier class_name
                    #| SCOPE class_name 
                    #| class_name
                    #| nested_name_specifier class_name  '''

#type-id:
    #type-specifier-seq abstract-declaratoropt
def p_type_id(p):
    ''' type_id : type_specifier_seq abstract_declarator_opt '''
    p[0]=Attribute()
    p[0].type=p[1].type
    p.set_lineno(0,p.lineno(1))
    pass

#type-specifier-seq:
    #type-specifier type-specifier-seqopt
def p_type_specifier_seq_1(p):
    ''' type_specifier_seq : type_specifier '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])

def p_type_specifier_seq_2(p):
    ''' type_specifier_seq : type_specifier type_specifier_seq '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    p[0].type= Type(p[2].type)
    if p[2].type == Type("ERROR"):
        p[0].type = Type("ERROR")

#abstract-declarator:
    #ptr-operator abstract-declaratoropt
    #direct-abstract-declarator
def p_abstract_declarator_1(p):
    ''' abstract_declarator : ptr_operator abstract_declarator_opt '''
    p.set_lineno(0,p.lineno(1))
    pass

def p_abstract_declarator_2(p):
    ''' abstract_declarator : direct_abstract_declarator '''
    p.set_lineno(0,p.lineno(1))
    pass

def p_abstract_declarator_opt_1(p):
    ''' abstract_declarator_opt : '''
    p[0] = None
    
def p_abstract_declarator_opt_2(p):
    ''' abstract_declarator_opt : abstract_declarator '''
    p.set_lineno(0,p.lineno(1))
    pass

#direct-abstract-declarator:
    #direct-abstract-declaratoropt ( parameter-declaration-clause ) cv-qualifier-seqopt exception-specificationopt
    #direct-abstract-declaratoropt [ constant-expressionopt ]
    #( abstract-declarator )
def p_direct_abstract_declarator_1(p):
    ''' direct_abstract_declarator : direct_abstract_declarator LPAREN parameter_declaration_clause RPAREN cv_qualifier_seq_opt '''
    p.set_lineno(0,p.lineno(1))
    pass

def p_direct_abstract_declarator_2(p):
    ''' direct_abstract_declarator : LPAREN parameter_declaration_clause RPAREN cv_qualifier_seq_opt '''
    p.set_lineno(0,p.lineno(1))
    pass

def p_direct_abstract_declarator_3(p):
    ''' direct_abstract_declarator : direct_abstract_declarator_opt LBRACKET constant_expression_opt RBRACKET '''
    p.set_lineno(0,p.lineno(1))
    pass

def p_direct_abstract_declarator_4(p):
    ''' direct_abstract_declarator : LPAREN abstract_declarator RPAREN '''
    p.set_lineno(0,p.lineno(1))
    pass 

def p_direct_abstract_declarator_opt_1(p):
    ''' direct_abstract_declarator_opt : '''
    p[0] = None
    
def p_direct_abstract_declarator_opt_2(p):
    ''' direct_abstract_declarator_opt : direct_abstract_declarator '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1]) 

#parameter-declaration-clause:
    #parameter-declaration-listopt ...opt
    #parameter-declaration-list , ...
def p_parameter_declaration_clause_1(p):
    ''' parameter_declaration_clause : '''
    p[0] = None

def p_parameter_declaration_clause_2(p):
    ''' parameter_declaration_clause : parameter_declaration_list '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])

def p_parameter_declaration_clause_3(p):
    ''' parameter_declaration_clause : parameter_declaration_list ELLIPSIS '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])

def p_parameter_declaration_clause_4(p):
    ''' parameter_declaration_clause : parameter_declaration_list COMMA ELLIPSIS '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])

#parameter-declaration-list:
    #parameter-declaration
    #parameter-declaration-list , parameter-declaration
def p_parameter_declaration_list_1(p):
    ''' parameter_declaration_list : parameter_declaration '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].attr['parameterList'] = [deepcopy(p[1])]
    p[0].attr['numParameters'] = 1
    p[0].code = p[1].code


def p_parameter_declaration_list_2(p):
    ''' parameter_declaration_list : parameter_declaration_list COMMA parameter_declaration '''
    p.set_lineno(0,p.lineno(2))
    p[0] = deepcopy(p[1])
    p[0].attr['parameterList'].append(deepcopy(p[3]))
    p[0].attr['numParameters'] += 1
    p[0].code+=p[3].code

#parameter-declaration:
    #decl-specifier-seq declarator
    #decl-specifier-seq declarator = assignment-expression
    #decl-specifier-seq abstract-declaratoropt
    #decl-specifier-seq abstract-declaratoropt = assignment-expression

def p_parameter_declaration_1(p):
    ''' parameter_declaration : decl_specifier_seq declarator '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[2])
    p[0].type = p[1].type
    #p[0].specifier = p[1].specifier
    #p[0].qualifier = p[1].qualifier
    if (p[2].attr.has_key('isFunction') and p[2].attr['isFunction'] == 1):
        print "\nError : Functions as arguments to functions not supported\n"

def p_parameter_declaration_2(p):
    ''' parameter_declaration : decl_specifier_seq declarator ASSIGN assignment_expression '''
    p.set_lineno(0,p.lineno(1))
    print "Assignments in formal parameters not supported"

def p_parameter_declaration_3(p):
    ''' parameter_declaration : decl_specifier_seq abstract_declarator_opt '''
    p[0] = deepcopy(p[2])
    p[0].type = p[1].type
    #p[0].specifier = p[1].specifier

def p_parameter_declaration_4(p):
    ''' parameter_declaration : decl_specifier_seq abstract_declarator_opt ASSIGN assignment_expression ''' 
    print "Assignments in formal parameters not supported"

#function-definition:
    #decl-specifier-seqopt declarator ctor-initializeropt function-body
    #decl-specifier-seqopt declarator function-try-block

def p_function_definition_1(p):
    ''' function_definition : declarator function_scope function_body unset_function_scope'''
    global size
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    #p[0].specifier = 1
    #code generation
    p[0].code+=p[1].code+p[2].code+p[3].code
    p[0].code+="\tjr $ra\n"




  
def p_function_definition_2(p):
    ''' function_definition : decl_specifier_seq  declarator function_scope function_body unset_function_scope'''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    
    #p[0].specifier = 1
    #code generation

#### TODO : Comment out this rule after adding the exception handling for function_try_block and adding try keyword ###
#def p_function_definition_3(p):
#    ''' function_definition : declarator function_try_block 
#                    | decl_specifier_seq declarator function_try_block '''
#    pass

#function-body:
    #compound-statement
def p_function_body(p):
    ''' function_body : compound_statement ''' 
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])

#initializer:
    #= initializer-clause
    #( expression-list )

def p_initializer_opt_1(p):
    ''' initializer_opt : '''
    p[0] = None
    
def p_initializer_opt_2(p):
    ''' initializer_opt : ASSIGN initializer_clause '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].type = Type("ASSIGN")
    p[0].attr["initializer"] = deepcopy(p[2])
    p[0].code = p[2].code
    if p[2].type == Type("ERROR"):
        p[0].type = Type("ERROR")

#### Rule to be used for assigning object of classes which constructor. ###
def p_initializer_opt_3(p):
    ''' initializer_opt : LPAREN expression_list RPAREN ''' 
    p.set_lineno(0,p.lineno(1))
    p[0] = "LPAREN"
    

#initializer-clause:
    #assignment-expression
    #{ initializer-list ,opt }
    #{ }
def p_initializer_clause_1(p):
    ''' initializer_clause : assignment_expression '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].attr["initializer_clause"] = [deepcopy(p[1])]
    p[0].type = p[1].type
    p[0].code = p[1].code
    if p[1].type == Type("ERROR"):
        p[0].type = Type("ERROR")

def p_initializer_clause_2(p):
    ''' initializer_clause : LBRACE initializer_list RBRACE '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].attr["isArray"] = 1
    p[0].attr["initializer_clause"] = deepcopy(p[2].attr["initializer_clause"])
    p[0].attr["num_element"] = p[2].attr["num_element"]
    p[0].type = p[2].type
    p[0].code = p[2].code
    if p[2].type == Type("ERROR"):
        p[0].type = Type("ERROR")

def p_initializer_clause_3(p):
    ''' initializer_clause : LBRACE RBRACE '''
    p.set_lineno(0,p.lineno(1))
    p[0] = Attribute()
    p[0] = initAttr(p[0])
    p[0].attr["isArray"] = 1
    p[0].attr["initializer_clause"] = []
    p[0].attr["num_element"] = 0
    p[0].code = ''

#initializer-list:
    #initializer-clause
    #initializer-list , initializer-clause
def p_initializer_list_1(p):
    ''' initializer_list : initializer_clause '''
    p.set_lineno(0,p.lineno(1))
    p[0] = deepcopy(p[1])
    
def p_initializer_list_2(p):
    ''' initializer_list : initializer_list COMMA initializer_clause ''' 
    p.set_lineno(0,p.lineno(2))
    p[0] = deepcopy(p[1])
    if p[1].type == p[3].type :
        p[0].attr["initializer_clause"].append(deepcopy(p[3].attr["initializer_clause"]))
        p[0].code+=p[3].code
        if p[3].attr.has_key("isArray"):
            p[0].attr["num_element"]+=p[3].attr["num_element"]
        else:
            p[0].attr["num_element"]+=1
    else :
        print "ERROR!! Line number : "+str(p.lineno(0))+" Conflicting data type "
        p[0].type = Type("ERROR")
## }}}

##### CLASSES #####     

## {{{
#class-name:
    #identifier
    #template-id
def p_class_name(p):
    ''' class_name : IDENTIFIER '''
    p[0] = Attribute()
    global env 
    val = env.get(p[1])
    p[0].attr["symbol"] = val 
    if val is not None:
        if val.type == Type("CLASS") :
            p[0].type = Type("CLASS")
        else :
            print ("Error : Line no " +str(p.lineno(1)) + str(p[1]) + " should be class")
            p[0].type = Type("ERROR")
    else : 
        print ("Error : Line no " +str(p.lineno(1))+ str(p[1]) + " not defined ")
        p[0].type = Type("ERROR")
    
#class-specifier:
    #class-head { member-specificationopt }
def p_class_specifier_1(p):
    ''' class_specifier : new_scope class_head LBRACE member_specification RBRACE finish_scope'''
    p[0] = Attribute()
    p[0].type = Type(p[2].name)
    pass

def p_class_specifier_2(p):
    ''' class_specifier : new_scope class_head LBRACE RBRACE finish_scope'''
    p[0] = Attribute()
    p[0].type = Type(p[2].name)
    pass
  
#class-head:
    #class-key identifieropt base-clauseopt
    #class-key nested-name-specifier identifier base-clauseopt
    #class-key nested-name-specifier template template-id base-clauseopt
def p_class_head(p):
    ''' class_head : class_key IDENTIFIER base_clause_opt '''
    global env
    cl = Symbol(p[2])
    cl.type = p[1].type 
    cl.attr["inherits"] = p[3]
    table = env.table
    temp = SymbolTable()
    for s in cl.attr["inherits"]:
        temp = temp.combine(s)
    cl.attr["scope"] = env.table 
    env.prev.put(cl)
    p[0] = cl 

##def p_class_head(p):
##    ''' class_head : class_key base_clause_opt 
##                    | class_key IDENTIFIER base_clause_opt 
##                    | class_key nested_name_specifier IDENTIFIER base_clause_opt '''
##    pass 

#class-key:
    #class
    #struct
    #union

def p_class_key_1(p):
    ''' class_key : CLASS '''
    p[0] = Attribute()
    p[0].type = Type("CLASS")
    

def p_class_key_2(p):
    ''' class_key : STRUCT '''
    p[0] = Attribute()
    p[0].type = Type("STRUCT")

def p_error(p):
    global success
    success = False
    print("Whoa. We're hosed")
    print("Syntax error at token " + str(p))
    #print("Syntax error at token " + str() + " of value " + str(p.value) + " at line number " + str(p.lineno))

#member-specification:
    #member-declaration member-specificationopt
    #access-specifier : member-specificationopt
def p_member_specification_1(p):
    '''member_specification : member_declaration '''

    pass
  
def p_member_specification_2(p):
    ''' member_specification : member_declaration member_specification '''
    pass
  
def p_member_specification_3(p):
    ''' member_specification : access_specifier COLON member_specification '''
    pass 
  
def p_member_specification_4(p):
    ''' member_specification : access_specifier COLON '''
    pass

#member-declaration:
    #decl-specifier-seqopt member-declarator-listopt ;
    #function-definition ;opt
    #::opt nested-name-specifier templateopt unqualified-id ;
    #using-declaration
    #template-declaration
def p_member_declaration_1(p):
    ''' member_declaration : decl_specifier_seq member_declarator_list SEMICOLON ''' 
def p_member_declaration_2(p):
    ''' member_declaration : decl_specifier_seq SEMICOLON '''
def p_member_declaration_3(p):
    ''' member_declaration : member_declarator_list SEMICOLON '''
def p_member_declaration_4(p):
    ''' member_declaration : SEMICOLON '''
def p_member_declaration_5(p):
    ''' member_declaration : function_definition SEMICOLON '''
def p_member_declaration_6(p):
    ''' member_declaration : function_definition '''


##def p_member_declaration(p):
##    ''' member_declaration : decl_specifier_seq member_declarator_list SEMICOLON 
##          | decl_specifier_seq SEMICOLON
##                    | member_declarator_list SEMICOLON
##          | SEMICOLON
##                    | function_definition SEMICOLON
##                    | function_definition 
##                    | SCOPE nested_name_specifier unqualified_id SEMICOLON 
##                    | nested_name_specifier unqualified_id SEMICOLON '''
##    pass 

#member-declarator-list:
    #member-declarator
    #member-declarator-list , member-declarator

def p_member_declarator_list(p):
    ''' member_declarator_list : member_declarator 
                    | member_declarator_list COMMA member_declarator '''
    pass 



#member-declarator:
    #declarator pure-specifieropt
    #declarator constant-initializeropt
    #identifieropt : constant-expression
def p_member_declarator_1(p):
    ''' member_declarator : declarator '''
    pass
  
def p_member_declarator_2(p):
    ''' member_declarator : declarator constant_initializer '''
    pass
  
def p_member_declarator_3(p):
    ''' member_declarator : IDENTIFIER COLON constant_expression '''
    pass
  
def p_member_declarator_4(p):
    ''' member_declarator : COLON constant_expression '''
    pass 

# TODO: fix this rule , no token for ZERO
#pure-specifier:
    #= 0
#def p_pure_specifier_opt(p):
    #''' pure_specifier_opt : 
                    #| ASSIGN ZERO  '''                                            ### ZERO Not defined .. I want to match it to 0 which is not in the tokens 
    #pass 

#constant-initializer:
    #= constant-expression
def p_constant_initializer(p):
    ''' constant_initializer : ASSIGN constant_expression '''
    pass 
## }}}

######## DERIVED CLASSES ##############

## {{{
#base-clause:
    #: base-specifier-list
def p_base_clause_opt_1(p):
    ''' base_clause_opt : '''
    p[0] = []
def p_base_clause_opt_2(p):
    ''' base_clause_opt : COLON base_specifier_list '''
    p.set_lineno(0,p.lineno(1))
    p[0] = p[2]


#base-specifier-list:
    #base-specifier
    #base-specifier-list , base-specifier
def p_base_specifier_list_1(p):
    ''' base_specifier_list : base_specifier_list COMMA base_specifier '''
    p.set_lineno(0,p.lineno(1))
    p[0] = p[1] + p[3]
    pass 
def p_base_specifier_list_2(p):
    ''' base_specifier_list : base_specifier ''' 
    p.set_lineno(0,p.lineno(1))
    p[0] = [p[1]]
    pass 

#base-specifier:
    #::opt nested-name-specifieropt class-name
    #virtual access-specifieropt ::opt nested-name-specifieropt class-name
    #access-specifier virtualopt ::opt nested-name-specifieropt class-name
def p_base_specifier_1(p):
    ''' base_specifier : class_name '''
    global env 
    p.set_lineno(0,p.lineno(1))
    if env.get(p[1]):
        p[0] = copy(env.get(p[1]).attr['scope'])
    else :
        print("Identifier" + str(p[1]) + "not defined")
    pass 
def p_base_specifier_2(p):
    ''' base_specifier : access_specifier class_name '''
    p.set_lineno(0,p.lineno(1))
    global env 
    if env.get(p[2]):
        p[0] = copy(env.get(p[2]).attr['scope'])
    else :
        print("Identifier" + str(p[2]) + "not defined")
    pass

##def p_base_specifier(p):
##    ''' base_specifier : SCOPE class_name 
##                    | SCOPE nested_name_specifier class_name
##                    | nested_name_specifier class_name
##                    | class_name
##                    | access_specifier SCOPE nested_name_specifier_opt class_name 
##                    | access_specifier nested_name_specifier_opt class_name'''
##    pass 


#access-specifier:
    #private
    #protected
    #public
def p_access_specifier_1(p):
    ''' access_specifier : PUBLIC 
                    | PRIVATE 
                    | PROTECTED ''' 
    p.set_lineno(0,p.lineno(1))
    pass 
## }}}

############# SPECIAL MEMBER FUNCTIONS ################

## {{{
#conversion-function-id:
    #operator conversion-type-id
def p_conversion_function_id(p):
    ''' conversion_function_id : OPERATOR conversion_type_id '''
    p.set_lineno(0,p.lineno(1))
    pass 

#conversion-type-id:
    #type-specifier-seq conversion-declaratoropt
def p_conversion_type_id_1(p):
    ''' conversion_type_id : type_specifier_seq %prec NOPAREN'''
    p.set_lineno(0,p.lineno(1))
    pass

def p_conversion_type_id_2(p):
    ''' conversion_type_id : type_specifier_seq conversion_declarator %prec LPAREN'''
    p.set_lineno(0,p.lineno(1))
    pass 

#conversion-declarator:
    #ptr-operator conversion-declaratoropt
def p_conversion_declarator_1(p):
    ''' conversion_declarator : ptr_operator %prec NOPAREN '''
    p.set_lineno(0,p.lineno(1))
    pass 
def p_conversion_declarator_2(p):
    ''' conversion_declarator : ptr_operator conversion_declarator %prec LPAREN'''
    p.set_lineno(0,p.lineno(1))
    pass 

#ctor-initializer:
    #: mem-initializer-list
def p_ctor_initializer_opt(p):
    ''' ctor_initializer_opt : 
                    | COLON mem_initializer_list'''
    pass 

#mem-initializer-list:
    #mem-initializer
    #mem-initializer , mem-initializer-list
def p_mem_initializer_list(p):
    ''' mem_initializer_list : mem_initializer
                    | mem_initializer COMMA mem_initializer_list '''
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
    ''' mem_initializer_id : class_name 
                    | IDENTIFIER '''
    p.set_lineno(0,p.lineno(1))
    pass 


##def p_mem_initializer_id(p):
##    ''' mem_initializer_id : SCOPE nested_name_specifier_opt class_name 
##                    | nested_name_specifier_opt class_name  
##                    | IDENTIFIER '''
##    pass 
### }}}

######### OVERLOADING ###########

## {{{
#operator-function-id:
    #operator operator
def p_operator_function_id(p) : 
    ''' operator_function_id : OPERATOR operator '''
    p.set_lineno(0,p.lineno(1))

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
    p.set_lineno(0,p.lineno(1))
    pass 
### }}}

########### TEMPLATES ################

######################################

########### EXCEPTION HANDLING #######

###################################### 

########### PREPROCESSING DIRECTIVES ###

########################################

lex.lex()
yacc.yacc(start='translation_unit',write_tables=1,method="LALR")

try:
    f1 = open(sys.argv[1])
    yacc.parse(f1.read(),debug=0)
    if success:
        print 'Compilation Successful with No Error !!!'
    else:
        print "Syntax error while parsing"
except IOError:
    print 'Could not open file:',  sys.argv[1]


