import sys
import re
import ply.lex as lex
from ply.lex import TOKEN

#class CPPLexer(object,error_func,type_lookup_func):
class CPPLexer(object):
    """ A lexer for the C language. After building it, set the
        input text with input(), and call token() to get new 
        tokens.

        The public attribute filename can be set to an initial
        filaneme, but the lexer will update it upon #line 
        directives.
    """
    #def __init__(self,error_func,type_lookup_func):
    def __init__(self):
        """ Create a new Lexer.

           error_func:
                An error function. Will be called with an error
                message, line and column as arguments, in case of 
                an error during lexing.

           type_lookup_func:
                A type lookup function. Given a string, it must
                return True IFF this string is a name of a type
                that was defined with a typedef earlier.
        """
        #self.error_func = error_func
        #self.type_lookup_func = type_lookup_func
        self.filename = ''

    def build(self, **kwargs):
        """ Builds the lexer from the specification. Must be
            called after the lexer object is created. 

            This method exists separately, because the PLY
            manual warns against calling lex.lex inside
            __init__
        """
        self.lexer = lex.lex(object=self, **kwargs)

    def token(self):
        g = self.lexer.token()
        return g
    


    ##
    ## All the tokens recognized by the lexer
    ##

    special_characters=('COMMA',
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
    'POUND',
    'DOT',    
    'SINGLE_QUOTE',
    'DOUBLE_QUOTE',
    'BACK_SLASH'
    )

    
    operators=('ASSIGN',
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

    complex_tokens=('ID',
    'DNUMBER',
    'INUMBER',
    'LIT_STR',
    'LIT_CHAR',
    'COMMENT')
    
    ##
    ## Reserved keywords
    ##
    
    keywords={'bool': 'BOOL',
            'break': 'BREAK',
            'case' : 'CASE', 
            'char'  : 'CHAR',
            'class' : 'CLASS',
            'continue' : 'CONTINUE',
            'default' : 'DEFAULT',
            'do' : 'DO',
            'double' : 'DOUBLE',
            'else' : 'ELSE',
            'false' : 'FALSE',
            'float' : 'FLOAT',
            'for' : 'FOR',
            'if' : 'IF',
            'inline' : 'INLINE',
            'int' : 'INT',
            'private' : 'PRIVATE',
            'public' : 'PUBLIC',
            'return' : 'RETURN',
            'switch' :'SWITCH',     
            'true' :'TRUE',
            'void' : 'VOID',
            'while' :'WHILE'
            }

    tokens=special_characters+operators+complex_tokens+tuple(keywords.values())


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
    t_POUND = r'\#'
    t_DOT = r'\.'
    t_EQ_PLUS = r'\+='
    t_EQ_MINUS = r'-='
    t_EQ_TIMES = r'\*='
    t_EQ_DIV = r'/='
    t_EQ_MODULO = r'%='
    t_SINGLE_QUOTE = r'\''
    t_DOUBLE_QUOTE= r'\"'
    t_BACK_SLASH = r'\\'

    
    
    def t_ID(self,t):
        r'[A-Za-z_][\w]*'
        if self.keywords.has_key(t.value):
            t.type=self.keywords[t.value]
        return t

    def t_DNUMBER(self,t):
        r'(\d*)((\.\d*([eE][+-]\d+)?)|([eE][+-]\d+))'
        return t

    def t_INUMBER(self,t):
        r'\d+'
        return t

    def t_LIT_CHAR(self,t):
        r'\'[\w\W]\''
        return t
    
    def t_LIT_STR(self,t):
        r'"[^\n]*?(?<!\\)"'
        temp_str = t.value.replace(r'\\', '')
        m = re.search(r'\\[^n"]', temp_str)
        if m != None:
            print "Line %d. Unsupported character escape %s in string literal." % (t.lineno, m.group(0))
            return
        return t
    
    def t_COMMENT(self,t):
        r'(/\*[\w\W]*?\*/)|(//[\w\W]*?\n)'
        t.lineno += t.value.count('\n')
        pass

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        
    t_ignore = '[ \t\r\f\v]'

    def t_error(self,t):
        print "Illegal character '%s' at line number %d" % (t.value[0], t.lineno)
        t.lexer.skip(1)


    def test(self,data):
        self.lexer.input(data)
        while True:
            tok= self.token()
            if not tok:
                break
            print tok

        
def run_lexer():

    file = open(sys.argv[1])
    lines = file.readlines()
    file.close()
    strings = ""
    for i in lines:
        strings += i
    Lexer= CPPLexer()
    Lexer.build()
    Lexer.test(strings)

if __name__ == '__main__':
    run_lexer()

