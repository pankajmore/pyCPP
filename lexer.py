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
    
    tokens=('ASSIGN',
    'COMMA',
    'COLON',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
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
    'ASTERISK',
    'QUESTION',
    'TILDE',
    'POUND',
    'DOT',
    'ELLIPSIS',
    'ARROW',
    'ARROW_STAR',
    'SHIFT_LEFT',
    'SHIFT_RIGHT',
    'EQ_PLUS',
    'EQ_MINUS',
    'EQ_TIMES',
    'EQ_DIV',
    'EQ_MODULO',
    'EQ_PIPE',
    'EQ_AMPERSAND',
    'EQ_CARET',
    'EQ_SHIFT_LEFT',
    'EQ_SHIFT_RIGHT',
    'ID',
    'FNUMBER',
    'INUMBER',
    'LIT_STR',
    'LIT_CHAR',
    'COMMENT',
    'SINGLE_QUOTE',
    'DOUBLE_QUOTE',
    'BACK_SLASH',
    'DOUBLE_POUND',
    'LT_COLON',
    'GT_COLON',
    'LT_MODULO',
    'GT_MODULO',
    'MODULO_COLON',
    'DOUBLE_MODULO_COLON',
    'DOUBLE_COLON',
    'DOT_STAR'
    )
    

    ##
    ## Operators
    ##
    
    operators={
        'and' : 'OP_AND',
 	'and_eq' : 'OP_AND_EQ',
 	'bitand' : 'OP_BITAND',
 	'bitor' : 'OP_BITOR',
 	'compl' : 'OP_COMPL',
 	'not' : 'OP_NOT',
 	'not_eq' : 'OP_NOT_EQ',
 	'or' :'OP_OR',
 	'or_eq' : 'OP_OR_EQ',
 	'xor' : 'OP_XOR',
 	'xor_eq' :'OP_XOR_EQ'
        }

    
    ##
    ## Reserved keywords
    ##
    
    keywords={'alignas' : 'ALIGNAS',
            'alignof' : 'ALIGNOF',
            'asm' : 'ASM',
            'auto': 'AUTO',
            'bool': 'BOOL',
            'break': 'BREAK',
            'case' : 'CASE', 
            'catch' : 'CATCH',
            'char'  : 'CHAR',
            'char16_t':'CHAR16_T',    
            'char32_t': 'CHAR32_T',     
            'class' : 'CLASS',
            'const' : 'CONST',
            'constexpr' : 'CONSTEXPR',     
            'const_cast' : 'CONST_CAST',
            'continue' : 'CONTINUE',
            'decltype' : 'DECLTYPE',
            'default' : 'DEFAULT',
            'delete' : 'DELETE',
            'do' : 'DO',
            'double' : 'DOUBLE',
            'dynamic_cast' : 'DYNAMIC_CAST',
            'else' : 'ELSE',
            'enum' : 'ENUM',
            'explicit' : 'EXPLICIT',
            'export' : 'EXPORT',
            'extern': 'EXTERN',
            'false' : 'FALSE',
            'float' : 'FLOAT',
            'for' : 'FOR',
            'friend' : 'FRIEND',
            'goto' : 'GOTO',
            'if' : 'IF',
            'inline' : 'INLINE',
            'int' : 'INT',
            'long' : 'LONG',
            'mutable' : 'MUTABLE',
            'namespace' : 'NAMESPACE',
            'new' : 'NEW',
            'noexcept' : 'NOEXCEPT',
            'nullptr' : 'NULLPTR',
            'operator' : 'OPERATOR',
            'private' : 'PRIVATE',
            'protected' : 'PROTECTED',
            'public' : 'PUBLIC',
            'register' : 'REGISTER',
            'reinterpret_cast' : 'REINTERPRET_CAST',
            'return' : 'RETURN',
            'short' : 'SHORT',
            'signed' : 'SIGNED',
            'sizeof' : 'SIZEOF',
            'static' : 'STATIC',
            'static_assert' :'STATIC_ASSERT',
            'static_cast':'STATIC_CAST',
            'struct':'STRUCT',
            'switch' : 'SWITCH',
            'template': 'TEMPLATE',
            'this': 'THIS',
            'thread_local' : 'THREAD_LOCAL',
            'throw' : 'THROW',
            'true' :'TRUE',
            'try' : 'TRY',
            'typedef' : 'TYPEDEF',
            'typeid' : 'TYPEID',
            'typename' : 'TYPENAME',
            'union' : 'UNION',
            'unsigned' : 'UNSIGNED',
            'using' : 'USING',
            'virtual' : 'VIRTUAL',
            'void' : 'VOID',
            'volatile' : 'VOLATILE',
            'wchar_t' : 'WCHAR_T',
            'while' :'WHILE',
            }

    tokens=tokens+tuple(keywords.values()) + tuple(operators.values())


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
    t_ASTERISK = r'\*'
    t_QUESTION = r'\?'
    t_TILDE = r'~'
    t_POUND = r'\#'
    t_ELLIPSIS = r'\.\.\.'
    t_DOT = r'\.'
    t_ARROW = r'->'
    t_ARROW_STAR = r'->\*'
    t_SHIFT_LEFT = r'<<'
    t_SHIFT_RIGHT = r'>>'
    t_EQ_PLUS = r'\+='
    t_EQ_MINUS = r'-='
    t_EQ_TIMES = r'\*='
    t_EQ_DIV = r'/='
    t_EQ_MODULO = r'%='
    t_EQ_PIPE = r'\|='
    t_EQ_AMPERSAND = r'&='
    t_EQ_CARET = r'\^='
    t_EQ_SHIFT_LEFT = r'<<='
    t_EQ_SHIFT_RIGHT = r'>>='
    t_SINGLE_QUOTE = r'\''
    t_DOUBLE_QUOTE= r'\"'
    t_BACK_SLASH = r'\\'
    t_DOUBLE_POUND = r'\#\#'
    t_LT_COLON = r'<:'
    t_GT_COLON = r':>'
    t_LT_MODULO = r'<%'
    t_GT_MODULO = r'%>'
    t_MODULO_COLON = r'%:'
    t_DOUBLE_MODULO_COLON = r'%:%:'
    t_DOUBLE_COLON = r'::'
    t_DOT_STAR = r'\.\*'
    
    
    def t_ID(self,t):
        r'[A-Za-z_][\w]*'
        if self.keywords.has_key(t.value):
            t.type=self.keywords[t.value]
        elif self.operators.has_key(t.value):
            t.type=self.operators[t.value]
        return t

    def t_FNUMBER(self,t):
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
        print "Illegal character '%s'" % t.value[0]
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

