import sys
import re
import ply.lex as lex
from ply.lex import TOKEN

##
## All the tokens recognized by the lexer
##

special_characters=('COMMA',
        'ELLIPSIS',
        'SCOPE' ,
        'COLON',
        'SEMICOLON',
        'LPAREN',
        'RPAREN',
        'LBRACKET',
        'RBRACKET',
        'LBRACE',
        'RBRACE',
        'QUESTION',
        'TILDE',
        'DOT',    
        'SINGLE_QUOTE',
        'DOUBLE_QUOTE',
        'BACK_SLASH'
        )


operators=('ASSIGN','ARROW',
        'GREATER',
        'LESS',
        'IS_EQ',
        'NOT_EQ',
        'GREATER_EQ',
        'LESS_EQ',
        'PLUS_PLUS',
        'MINUS_MINUS', 
        'PLUS',    
        'MINUS',
        'TIMES',   
        'DIV', 
        'MODULO', 'DOUBLE_AMPERSAND',
        'DOUBLE_PIPE',
        'EXCLAMATION',  'AMPERSAND',
        'PIPE',
        'CARET',
        'EQ_PLUS',
        'EQ_MINUS',
        'EQ_TIMES',
        'EQ_DIV',
        'EQ_MODULO',
        )

complex_tokens=('IDENTIFIER',
        'ILLEGAL_ID',
        'DNUMBER',
        'INUMBER',
        'ILLEGAL_DNUMBER',
        'ILLEGAL_INUMBER',
        'LIT_STR',
        'LIT_CHAR',
        'COMMENT')

##
## Reserved keywords
##

keywords={'auto': 'AUTO',
        'bool': 'BOOL',
        'break': 'BREAK',
        'case' : 'CASE', 
        'char'  : 'CHAR',
        'class' : 'CLASS',
        'continue' : 'CONTINUE',
        'default' : 'DEFAULT',
        'delete' : 'DELETE',
        'do' : 'DO',
        'double' : 'DOUBLE',
        'else' : 'ELSE',
        'enum' : 'ENUM',
        'extern' : 'EXTERN',
        'false' : 'FALSE',
        'float' : 'FLOAT',
        'for' : 'FOR',
        'if' : 'IF',
        'inline' : 'INLINE',
        'int' : 'INT',
        'new' : 'NEW',
        'operator' : 'OPERATOR',
        'private' : 'PRIVATE',
        'public' : 'PUBLIC',
        'protected' : 'PROTECTED',
        'return' : 'RETURN',
        'sizeof' : 'SIZEOF',
        'struct' : 'STRUCT',
        'switch' :'SWITCH',     
        'true' :'TRUE',
        'typename' : 'TYPENAME',
        'union' : 'UNION',
        'void' : 'VOID',
        'while' :'WHILE'
        }

tokens=special_characters+operators+complex_tokens+tuple(keywords.values())


# Each token is specified by writing a regular expression rule. 
# Each of these rules are are defined by making declarations with a 
# special prefix t_ to indicate that it defines a token.

t_ARROW = r'->'
t_ELLIPSIS = r'\.\.\.'
t_SCOPE = r'::'
t_ASSIGN = r'='
t_COMMA = r','
t_COLON = r':'
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_GREATER = r'>'
t_LESS = r'<'
t_IS_EQ = r'=='
t_NOT_EQ = r'!='
t_GREATER_EQ = r'>='
t_LESS_EQ = r'<='
t_PLUS_PLUS = r'\+\+'
t_MINUS_MINUS = r'--'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIV = r'/(?!\*)'
t_MODULO = r'%'
t_DOUBLE_AMPERSAND = r'&&'
t_DOUBLE_PIPE = r'\|\|'
t_EXCLAMATION = r'!'
t_AMPERSAND = r'&'
t_PIPE = r'\|'
t_CARET = r'\^'
t_QUESTION = r'\?'
t_TILDE = r'~'
t_EQ_PLUS = r'\+='
t_EQ_MINUS = r'-='
t_EQ_TIMES = r'\*='
t_EQ_DIV = r'/='
t_EQ_MODULO = r'%='
t_SINGLE_QUOTE = r'\''
t_DOUBLE_QUOTE= r'\"'
t_BACK_SLASH = r'\\'


IDENTIFIER = r'[A-Za-z_][\w]*'
@TOKEN(IDENTIFIER)
def t_IDENTIFIER(t):
    """Match an identifier and check if it is a keyword.
    This approach greatly reduces the number of regular 
    expression rules and is likely to make things a little faster.
    """
    r'[A-Za-z_][\w]*'
    global keywords
    if keywords.has_key(t.value):
        t.type=keywords[t.value]
    return t

def t_ILLEGAL_ID(t):
    r'(?<=[\d])[A-Za-z_][\w]*'
    print "Ill_formed Identifier %s' at line number %d" % (t.value, t.lineno)

    # Match a decimal number
def t_DNUMBER(t):
    r'((\d*)\.((\d*([eE][+-]\d+))|\d+)(?=[+\-*/%(),;\s\]])|([eE][+-]\d+)(?=[+\-*/()%,;\s\]]))'
    return t

# Match an integer
def t_INUMBER(t):
    r'\d+(?=[+\-*/()%,;\s\]])'
    return t

def t_DOT(t):
    r'\.'
    return t

c1=r'[eE]([eE]*[+-]*\d*)*(?=[+\-*/()%,;\s\]])'
c2=r'([eE]+[+-]*\d*)*\.(\d*\.*[eE]*[+-]*)*(?=[+\-*/%(),;\s\]])'
c3=r'(\d*)\.((\d*([eE][+-]\d+))|\d+)([^+()\-*/%,;\s][a-zA-Z_]*)'
c4=r'([eE][+-]\d+)[^+()\-*/%,;\s][a-zA-Z_]*'
c5=r'[eE]([eE]*[+-]*\d*)*([^+\-*/()%,;\s][a-zA-Z_]*)'
c6=r'([eE]+[+-]*\d*)*\.(\d*\.*[eE]*[+-]*)*([^+\-*/%(),;\s][a-zA-Z_]*)'
Il_Dnum=r'('+c4+r'|'+c5+r'|'+c6+'|'+c1+r'|'+c2+r'|'+c3+r')'

@TOKEN(Il_Dnum)

def t_ILLEGAL_DNUMBER(t):
    print "Ill_formed Double Number '%s' at line number %d" % (t.value, t.lineno)


def t_ILLEGAL_INUMBER(t):
    r'\d+([^+\-*/()%,;\s][a-zA-Z_]*)'
    print "Ill_formed Integer Number '%s' at line number %d" % (t.value, t.lineno)

def t_LIT_CHAR(t):
    r'\'[\w\W]\''
    return t

def t_LIT_STR(t):
    r'"[^\n]*?(?<!\\)"'
    temp_str = t.value.replace(r'\\', '')
    m = re.search(r'\\[^n"]', temp_str)
    if m != None:
        print "Line %d. Unsupported character escape %s in string literal." % (t.lineno, m.group(0))
        return
    return t

# Match single line and multiline comments and 
    # increase the line number
def t_COMMENT(t):
    r'(/\*[\w\W]*?\*/)|(//[\w\W]*?\n)'
    t.lineno += t.value.count('\n')
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# The use of t_ignore provides substantially better lexing performance 
# because it is handled as a special case and is checked in a much more 
# efficient manner than the normal regular expression rules.
t_ignore = ' \t\r\f\v'

    # Called when no rule is matched
    # t.value attribute contains the rest of the input string 
    # that has not been tokenized
    # we simply print the offending character and skip ahead 
    # one character by calling t.lexer.skip(1)

def t_error(t):
    print "Illegal character '%s' at line number %d" % (t.value[0], t.lineno)
    t.lexer.skip(1)
    global success
    print "Illegal character '%s' at line number %d" % (t.value[0], t.lineno)
    t.lexer.skip(1)
    success = False

def test_lexer(lexer, string):
    lexer.input(string)
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
    	print tok


if __name__ == '__main__':
    file = open(sys.argv[1])
    lines = file.readlines()
    file.close()
    strings = ""
    for i in lines:
        strings += i
    # run lexer on input
    lexer = lex.lex()
    test_lexer(lexer, strings)
