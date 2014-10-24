"""A much stricter language

typeclass Any implements () extends ()

function capacity(container : Container) : Int {
    declare x : Int
    declare y : Float
    
    x = 2 * size(container)
    y = to_Float()
    return size(container)
}

"""

from ply import lex, yacc

literals = '(){}[]:;=+-*/'
keywords = ('function','return')
t_NAME = r'(?!\d)\w+'
t_INT = r'(?:\+|\-)\d+(?!\.)'
t_FLOAT = r'(?:\+|\-)\d+\.\d*'
tokens = ('NAME', 'INT', 'FLOAT') + tuple(keyword.upper() for keyword in keywords)

def p_type_name(p):
    "type : NAME"


