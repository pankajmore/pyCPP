import re
import sys

import ply.lex
from ply.lex import TOKEN


class CPPLexer(object):
    """ A lexer for the C language. After building it, set the
        input text with input(), and call token() to get new 
        tokens.

        The public attribute filename can be set to an initial
        filaneme, but the lexer will update it upon #line 
        directives.
    """
    def __init__(self, error_func, type_lookup_func):
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
        self.error_func = error_func
        self.type_lookup_func = type_lookup_func
        self.filename = ''

    def build(self, **kwargs):
        """ Builds the lexer from the specification. Must be
            called after the lexer object is created. 

            This method exists separately, because the PLY
            manual warns against calling lex.lex inside
            __init__
        """
        self.lexer = ply.lex.lex(object=self, **kwargs)

    def token(self):
        g = self.lexer.token()
        return g

    ##
    ## Reserved keywords
    ##
    keywords = ()

    ##
    ## All the tokens recognized by the lexer
    ##
    tokens = keywords + (
        # Identifiers
        'ID', 

